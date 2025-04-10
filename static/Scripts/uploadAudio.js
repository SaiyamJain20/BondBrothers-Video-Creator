document.addEventListener('DOMContentLoaded', function () {
    const uploadButton = document.getElementById('uploadButton');
    const fileInput = document.getElementById('musicUpload');

    uploadButton.addEventListener('click', function () {

        if (fileInput.files.length === 0) {
            console.log('No file selected');
            return;
        }

        const formData = new FormData();
        for (const file of fileInput.files) {
            formData.append('audioFile', file);
        }

        // document.querySelector('.loader').classList.add('show');
        fetch('/upload-audio', {
            method: 'POST',
            body: formData
        })
            .then(response => {
                // document.querySelector('.loader').classList.remove('show');
                if (response.ok) {
                    return response.text();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                console.log('Audio upload successful:', data);
                const fileInput = document.getElementById('musicUpload');
                fileInput.value = '';
            })
            .catch(error => {
                console.error('Error uploading audio:', error);
            });
    });
});
