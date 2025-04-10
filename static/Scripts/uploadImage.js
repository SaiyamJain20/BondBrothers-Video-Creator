document.addEventListener('DOMContentLoaded', function () {
    let dropArea = document.getElementById('drop-area');
    let fileInput = document.getElementById('fileInput');
    let imageList = document.getElementById('imageContainer');
    let browseButton = document.getElementById('browseButton');
    let submitButton = document.getElementById('submit');
    let allFiles = [];

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    dropArea.addEventListener('drop', handleDrop, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        dropArea.classList.add('highlight');
    }

    function unhighlight() {
        dropArea.classList.remove('highlight');
    }

    function handleDrop(e) {
        e.preventDefault();
        dropArea.classList.remove('error');

        let files = e.dataTransfer.files;
        allFiles = allFiles.concat(Array.from(files).filter(file => file.type.startsWith('image/')));
        handleFiles(files);
    }

    browseButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', function (e) {
        e.preventDefault();
        dropArea.classList.remove('error');

        allFiles = allFiles.concat(Array.from(e.target.files).filter(file => file.type.startsWith('image/')));
        handleFiles(e.target.files);
    });

    //var ul = document.createElement('ul');
    function handleFiles(files) {
        files = Array.from(files);
        files.forEach(previewFile);
        //imageList.appendChild(ul);
    }

    function previewFile(file) {
        if (!file.type.startsWith('image/')) {
            dropArea.classList.add('error');
            alert('Only image files are supported.');
            return;
        }
        // let li = document.createElement('li');
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function () {
            let container = document.createElement('div');
            container.classList.add('image-item');
            container.target = '_blank';

            let closeButton = document.createElement('i');
            closeButton.classList.add('bi', 'bi-x-circle', 'close-button');

            closeButton.addEventListener('click', function () {
                container.remove();
                allFiles = allFiles.filter(f => f !== file);
                checkForImages();
            });

            let anchor = document.createElement('a');
            anchor.href = reader.result;
            anchor.target = "_blank";

            let img = document.createElement('img');
            img.src = reader.result;

            let label = document.createElement('label');
            label.textContent = file.name;

            anchor.appendChild(img);
            container.appendChild(closeButton);
            container.appendChild(anchor);
            container.appendChild(label);
            imageList.appendChild(container);
            // li.appendChild(img);
        }
    }

    submitButton.addEventListener('click', function () {
        var formData = new FormData();
        allFiles.forEach(file => {
            formData.append('files[]', file);
        });
        // document.querySelector('.loader').classList.add('show');
        fetch('/Upload-images', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                if (response.ok) {
                    // document.querySelector('.loader').classList.remove('show');
                    return response.text();
                }
                alert("ERROR: Please upload an image.");
            })
            .then(data => {
                console.log('Redirecting...');
                window.location.href = '/workspace';
            })
            .catch(error => {
                console.error('Error uploading images:', error);
            });
    });

});
