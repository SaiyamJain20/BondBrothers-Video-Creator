var uploadButton = document.getElementById('uploadButton');
var fileInput = document.getElementById('profileUpload');
var imageContainer = document.getElementById("imageContainer");
var musicContainer = document.getElementById("musicContainer");
// var sortBySelect = document.getElementById("sortBy");

function loadImages(imageSet) {
    imageContainer.innerHTML = '';
    imageContainer.style.display = 'grid';
    imageSet.forEach(function (image) {
        var anchor = document.createElement("a");
        anchor.href = "data:image/jpeg;base64," + image.data;
        anchor.target = "_blank";

        var img = document.createElement("img");
        img.src = "data:image/jpeg;base64," + image.data;
        img.alt = image.name;

        var div = document.createElement("div");
        div.classList.add("image-item");

        var label = document.createElement('label');
        label.textContent = image.name;

        anchor.appendChild(img);
        div.appendChild(anchor);
        div.appendChild(label);
        imageContainer.appendChild(div);
    });
}

function loadAudio(audioSet) {
    musicContainer.innerHTML = '';
    audioSet.forEach(function (audio) {
        var cell = document.createElement("div");
        cell.classList.add('audioCell');

        var name = document.createElement("label");
        name.classList.add('audioName');
        name.setAttribute('for', 'audio:' + audio.name)
        name.textContent = "" + audio.name;

        var controls = document.createElement("audio");
        controls.setAttribute('controls', '');

        var clip = document.createElement("source");
        clip.setAttribute('src', "data:audio/mpeg;base64," + audio.data);

        controls.appendChild(clip);
        cell.appendChild(name);
        cell.appendChild(controls);
        musicContainer.appendChild(cell);
    });
}

window.onload = function () {
    setLoader(imageContainer)
    fetch('/getUploadedImages')
        .then(response => response.json())
        .then(images => {
            loadImages(images);
        })
        .catch(error => console.error('Error fetching images:', error));

    setLoader(musicContainer)
    fetch('/getUploadedAudio')
        .then(response => response.json())
        .then(audios => {
            loadAudio(audios);
        })
        .catch(error => console.error('Error fetching images:', error));
}

function setLoader(parentTag) {
    parentTag.innerHTML = "";
    parentTag.style.display = 'flex';
    parentTag.style.justifyContent = 'center';
    parentTag.style.alignItems = 'center';
    let loaderImg = document.createElement('img');
    loaderImg.src = '../static/Images/loader1.gif';
    parentTag.appendChild(loaderImg);
}

uploadButton.addEventListener('click', function () {
    let imgElement = document.getElementById('profilePic');

    if (fileInput.files.length === 0) {
        console.log('No file selected');
        return;
    }

    const formData = new FormData();
    for (const file of fileInput.files) {
        formData.append('image', file);
    }

    imgElement.src = '../static/Images/loader1.gif';
    fetch('/profileUpload', {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            const encodedImage = data[0].data;
            imgElement.src = 'data:image/jpeg;base64,' + encodedImage;
        })
        .catch(error => {
            console.error('Error uploading image:', error);
        });
});

function deleteAllImages() {
    fetch('/deleteAllImagesofUser')
        .then(response => response.json())
        .then(
            imageContainer.innerHTML = ''
        )
        .catch(error => console.error('Error fetching images:', error));
}

function deleteAllAudios() {
    fetch('/deleteAllAudiosofUser')
        .then(response => response.json())
        .then(
            musicContainer.innerHTML = ''
        )
        .catch(error => console.error('Error fetching images:', error));
}