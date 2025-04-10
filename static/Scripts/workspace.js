var imageContainer = document.getElementById("imageContainer");
var musicContainer = document.getElementById("musicContainer");
var sortBySelect = document.getElementById("sortBy");
var searchInput = document.getElementById("searchInput");

function loadImages(imageSet) {
    if (imageContainer) {
        while (imageContainer.firstChild) {
            imageContainer.removeChild(imageContainer.firstChild);
        }
        imageContainer.style.display = 'grid';
        imageSet.forEach(function (image) {
            var img = document.createElement("img");
            img.src = "data:image/jpeg;base64," + image.data;
            img.alt = image.name;

            var div = document.createElement("div");
            div.classList.add("image-item");

            var selectButton = document.createElement("i");
            selectButton.classList.add("bi", "bi-check-circle", "close-button");

            img.addEventListener('click', () => {
                toggleImage(image, selectButton);
            });

            var label = document.createElement('label');
            label.textContent = image.name;

            div.appendChild(img);
            div.appendChild(selectButton);
            div.appendChild(label);
            imageContainer.appendChild(div);
        });
    } else {
        console.error("Image container not found.");
    }
}

function loadAudio(audioSet) {
    audioSet.forEach(function (audio) {
        var cell = document.createElement("div");
        cell.classList.add('audioCell');

        var check = document.createElement('input');
        check.type = 'checkbox';
        check.id = 'audio:' + audio.name;
        
        var name = document.createElement("label");
        name.classList.add('audioName');
        name.setAttribute('for', 'audio:'+audio.name)
        name.textContent = "" + audio.name;
        
        var controls = document.createElement("audio");
        controls.setAttribute('controls', '');

        var clip = document.createElement("source");
        clip.setAttribute('src', "data:audio/mpeg;base64," + audio.data);

        check.addEventListener('click', () => {
            toggleAudio(audio);
        });

        controls.appendChild(clip);
        cell.appendChild(check);
        cell.appendChild(name);
        cell.appendChild(controls);
        musicContainer.appendChild(cell);
    });
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

window.onload = function () {
    setLoader(imageContainer)
    fetch('/getUploadedImages')
        .then(response => response.json())
        .then(images => {
            loadImages(images);
        })
        .catch(error => console.error('Error fetching images:', error));

    fetch('/getPreloadedAudio')
        .then(response => response.json())
        .then(audios => {
            loadAudio(audios);
        })
        .catch(error => console.error('Error fetching images:', error));

    fetch('/getUploadedAudio')
        .then(response => response.json())
        .then(audios => {
            loadAudio(audios);
        })
        .catch(error => console.error('Error fetching images:', error));
    emptyImages();
}

searchInput.addEventListener("keypress", function (event) {
    if (event.key === 'Enter') {
        imageContainer.innerHTML = ""
        setLoader(imageContainer)
        event.preventDefault();
        var searchValue = searchInput.value;
        console.log("Search value:", searchValue);

        fetch('/searchBy', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ search: searchValue })
        })
            .then(response => response.json())
            .then(images => {
                loadImages(images);
            })
            .catch(error => console.error('Error fetching images:', error));
    }
});

sortBySelect.addEventListener("change", function () {
    console.log(sortBySelect.value);
    imageContainer.innerHTML = ""
    setLoader(imageContainer)
    var selectedValue = sortBySelect.value;
    if (selectedValue == "file_name") {
        fetch('/getSortedImageName')
            .then(response => response.json())
            .then(images => {
                loadImages(images);
            })
            .catch(error => console.error('Error fetching sorted images:', error));
    }
    if (selectedValue == "uploaded_at") {
        fetch('/getSortedImageDate')
            .then(response => response.json())
            .then(images => {
                loadImages(images);
            })
            .catch(error => console.error('Error fetching sorted images:', error));
    }
    if (selectedValue == "file_size") {
        fetch('/getSortedImageFileSize')
            .then(response => response.json())
            .then(images => {
                loadImages(images);
            })
            .catch(error => console.error('Error fetching sorted images:', error));
    }
});

function toggleImage(image, selectButton) {
    fetch('/toggle-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: image })
    })
        .then(response => {
            if (response.ok) {
                response.json().then(data => {
                    if (data.selected) {
                        selectButton.classList.remove('bi-check-circle');
                        selectButton.classList.add('bi-check-circle-fill');
                    } else {
                        selectButton.classList.remove('bi-check-circle-fill');
                        selectButton.classList.add('bi-check-circle');
                    }
                });
            } else {
                console.error('Failed to toggle selected status for image.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function toggleAudio(audio) {
    fetch('/toggle-audio', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ audio :audio })
    })
        .then(response => {
            if (response.ok) {
                console.log('Audio select/deselect successfull');
            } else {
                console.error('Failed to toggle selected status for audio.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function emptyImages() {
    fetch('/empty-selected', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to remove all images from selection.');
        }
    })
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error.message);
    });
}

var clear = document.getElementById("imageClear");
clear.addEventListener('click', clearSelection);

function clearSelection() {
    emptyImages();
    var checks = imageContainer.querySelectorAll('.bi.close-button.bi-check-circle-fill');
    checks.forEach(element => {
        element.classList.add('bi-check-circle');
        element.classList.remove('bi-check-circle-fill');
    });
    checks = musicContainer.querySelectorAll('input[type="checkbox"]');
    checks.forEach(element => {
        if(element.checked)
            element.checked = false;
    });
}

function generateVideo() {
    var imgDuration = document.getElementById("imageDuration").value;
    var Transition = document.getElementById("transitionType").value;
    var vidResolution = document.getElementById("resolution").value;
    var quality = document.getElementById("quality").value;

    var requestData = {
        imgDuration: imgDuration,
        Transition: Transition,
        vidResolution: vidResolution,
        quality: quality
    };

    fetch('/videoCreate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            console.log(data.message);
            document.getElementById('videoPlayer').querySelector('source').src = data.video_path;
            document.getElementById('videoPlayer').load();
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch(error => {
        console.error('Error generating video:', error);
    });
}

function deleteVideo() {
    fetch('/delete-video', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Failed to delete video');
        }
    })
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error:', error.message);
    });
}

window.addEventListener('beforeunload', function(event) {
    event.preventDefault();
    deleteVideo();
    clearSelection();
    event.returnValue = 'Your selection of images and audio will not be saved.';
});

function downloadVideo() {
    var videoSource = document.getElementById('videoPlayer').querySelector('source').src;
    
    var downloadLink = document.createElement('a');
    downloadLink.href = videoSource;
    downloadLink.download = 'output_video.mp4';
    downloadLink.style.textDecoration = 'none';
    
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}