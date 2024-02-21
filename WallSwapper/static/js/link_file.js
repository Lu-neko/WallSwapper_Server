const body = document.querySelector("body");
const show = document.querySelector("#show");
const set = document.querySelector("#set");
const result = document.querySelector("#result");

const validTypes = ["image/png", "image/jpeg"]

let blob;

body.ondrop = (event) => {
    event.preventDefault();
    if (event.dataTransfer.items) {
        [...event.dataTransfer.items].forEach((item, i) => {
            if (item.kind === "file") {
                const file = item.getAsFile();
                if (validTypes.includes(file.type)){
                    blob = file;
                }
            }
        });
    }

    if (blob){
        let url = URL.createObjectURL(blob);
        show.src = url;
        show.style.display = "inline";
        set.style.display = "inline";
        result.textContent = "";
    }
}

body.ondragover = (event) => {
    event.preventDefault();
}

set.onclick = async (event) => {
    if (!blob) return;
    
    const formData = new FormData();
    let location = window.location.href.split("/");
    formData.append("url", location[location.length-1])
    formData.append("image", blob);

    const response = await fetch(window.location.origin + "/api/link/set_image", {
        method: "POST",
        body: formData,
    });
    if (response.status == 200){
        result.textContent = "Success!"
    } else {
        result.textContent = "Error.."
    }
}