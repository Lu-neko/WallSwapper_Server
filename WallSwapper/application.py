from flask import Flask, request, send_file, make_response, Blueprint, render_template
import os
import hashlib
from datetime import datetime, timedelta

from .database.interactions import get_user, url_set_image, create_link, create_user, connect_user, friend_set_image, delete_link

file_folder = __name__.split(".")[0] + "/files/"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 20 * 1000 * 1000

@app.route("/set_image/<url>")
def set_image(url):
    return render_template("link_file.html")

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/create_account", methods=["POST"])
def create_account():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return "", 400

    result = create_user(username, password)

    if not result:
        return "", 400

    return result.token

@api.route("/connect", methods=["POST"])
def connect():
    username = request.json.get("username")
    password = request.json.get("password")

    if not username or not password:
        return "", 400

    result = connect_user(username, password)

    if not result:
        return "", 401

    return result.token

@api.route("/update", methods=["POST"])
def update():
    if not "token" in request.json:
        return "", 400
    token = request.json["token"]
    user = get_user(token)

    if not user:
        return "", 400

    if not user.image:
        return "", 204

    return user.image, 200

@api.route("/images/<filename>")
def image(filename):
    if filename in os.listdir(file_folder):
        return send_file(f"files/{filename}", mimetype='image')
    return "", 404

@api.route("/link/set_image", methods=["POST"])
def link_set_image():
    if not "url" in request.form:
        return "", 400

    url = request.form["url"]

    if "image" not in request.files:
        return "", 400

    file = request.files["image"]

    if file.filename == '':
        return "", 400

    BUF_SIZE = 2048
    md5 = hashlib.md5()

    while True:
        data = file.read(BUF_SIZE)
        if not data:
            break
        md5.update(data)

    if file.tell() > 16777216:
        return "", 413

    file.seek(0)

    if not url_set_image(url, md5.hexdigest()):
        return "", 400

    file.save(file_folder + md5.hexdigest())

    return "", 200

@api.route("/friendship/set_image", methods=["POST"])
def friendship_set_image():
    token = request.json.get("token")
    target_id = request.json.get("target_id")

    if not token or not target_id:
        return "", 400

    if "image" not in request.files:
        return "", 400

    file = request.files["image"]

    if file.filename == '':
        return "", 400

    BUF_SIZE = 2048
    md5 = hashlib.md5()

    while True:
        if file.tell() > 16777216:
            return "", 413
        data = file.read(BUF_SIZE)
        if not data:
            break
        md5.update(data)

    file.seek(0)

    if not friend_set_image(token, target_id, md5.hexdigest()):
        return "", 400

    file.save(file_folder + md5.hexdigest())

    return "", 200

@api.route("/create_link", methods=["POST"])
def api_create_link():
    if not "token" in request.json:
        return "", 401

    token = request.json["token"]

    uses = request.json.get("uses")
    expiration = request.json.get("expiration")

    if uses:
        if not uses.isdecimal():
            return "", 400

        uses = int(uses)

        if uses < 1 or uses > 999:
            return "", 400

    if expiration:
        if not expiration.isdecimal():
            return "", 400

        expiration = datetime.fromtimestamp(int(expiration))

        if expiration < datetime.now() or expiration > datetime.now() + timedelta(days=60):
            return "", 400

    result = create_link(token, uses, expiration)

    if result == None:
        return "", 400

    if not result:
        return "", 403

    return result.url

@api.route("/delete_link", methods=["POST"])
def api_delete_link():
    token = request.json.get("token")
    url = request.json.get("url")

    if not token or not url:
        return "", 400

    result = delete_link(token, url)

    if not result:
        return "", 403

    return "", 200

app.register_blueprint(api)