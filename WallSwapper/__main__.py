from .application import app

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--create_db", action="store_true")

args = parser.parse_args()

if args.create_db:
    from .database.create_db import create_db
    create_db()
    exit(0)

from .application import app

app.run()