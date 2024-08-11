// Function to browse and select a folder

function browseFolder(inputId) {
    const inputElement = document.getElementById(inputId);
    const folderInput = document.createElement('input');
    folderInput.type = 'file';
    folderInput.webkitdirectory = true;  // Allows selection of a directory
    folderInput.directory = true;  // Some browsers might require this
    folderInput.multiple = false;

    folderInput.onchange = () => {
        if (folderInput.files.length > 0) {
            // Get the path from the first selected directory
            const folderPath = folderInput.files[0].path || folderInput.files[0].webkitRelativePath.split('/')[0];
            inputElement.value = folderPath;  // Display the selected folder path
            console.log("Selected folder path:", folderPath);  // Log folder path
        }
    };

    folderInput.click();
}

// Drag-and-drop functionality for file list
document.getElementById('file_list').addEventListener('dragover', function(event) {
    event.preventDefault(); // Prevent default to allow drop
    event.stopPropagation();
    this.style.border = "2px dashed #0b79d0";
});

document.getElementById('file_list').addEventListener('dragleave', function(event) {
    event.preventDefault();
    event.stopPropagation();
    this.style.border = "2px dashed #ccc";
});

document.getElementById('file_list').addEventListener('drop', function(event) {
    event.preventDefault(); // Prevent default to stop opening the file
    event.stopPropagation();
    this.style.border = "2px dashed #ccc";

    const files = event.dataTransfer.files;
    for (let i = 0; i < files.length; i++) {
        const filePath = files[i].path || files[i].webkitRelativePath || files[i].name;
        this.value += filePath + "\n";
    }

    console.log("Dropped files:", this.value);
});

// Function to browse and select files
function browseFiles(id) {
    const input = document.getElementById(id);
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.multiple = true;
    fileInput.onchange = () => {
        const files = Array.from(fileInput.files).map(file => file.name).join(", ");
        input.value = files;  // Display the selected files in the input field
        const fileContainer = document.getElementById('fileContainer');
        fileContainer.innerHTML = '';  // Clear existing files

        Array.from(fileInput.files).forEach(file => {
            const label = document.createElement('label');
            label.className = 'file-label';
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.name = 'file';
            checkbox.value = file.name;
            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(file.name));
            fileContainer.appendChild(label);
        });

        console.log("Selected files:", files);  // Log selected files
    };
    fileInput.click();
}

// Function to submit selected files
function submitSelectedFiles() {
    const checkboxes = document.querySelectorAll('input[name="file"]:checked');
    const selectedFiles = Array.from(checkboxes).map(cb => cb.value).join(",");
    document.getElementById('selected_files').value = selectedFiles;

    console.log("Submitting selected files:", selectedFiles);  // Log selected files
    console.log("Folder path being submitted:", document.getElementById('folder_path_hidden').value);  // Log folder path being submitted

    document.getElementById('generate_form').submit();
}

// Function to open tag selection popup
function openTagPopup() {
    const popup = window.open("", "Tags", "width=300,height=400");
    const popupContent = `
        <html>
        <head>
            <title>Select Tags</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 10px;
                }
                .tag {
                    display: block;
                    margin-bottom: 5px;
                }
                button {
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <h2>Select Tags</h2>
            <div id="tagContainer"></div>
            <button onclick="selectTags()">Select</button>
            <script>
                function selectTags() {
                    const checkboxes = document.querySelectorAll('input[name="tag"]:checked');
                    const selectedTags = Array.from(checkboxes).map(cb => cb.value).join(",");
                    window.opener.document.getElementById('tags').value = selectedTags;
                    window.close();
                }
                document.addEventListener('DOMContentLoaded', () => {
                    fetch('/tags')
                        .then(response => response.json())
                        .then(tags => {
                            const container = document.getElementById('tagContainer');
                            tags.forEach(tag => {
                                const label = document.createElement('label');
                                label.className = 'tag';
                                const checkbox = document.createElement('input');
                                checkbox.type = 'checkbox';
                                checkbox.name = 'tag';
                                checkbox.value = tag;
                                label.appendChild(checkbox);
                                label.appendChild(document.createTextNode(tag));
                                container.appendChild(label);
                            });
                        });
                });
            </script>
        </body>
        </html>
    `;
    popup.document.write(popupContent);
    popup.document.close();
}

// Function to fetch files from a selected folder
function fetchFiles() {
    const folderPath = document.getElementById('folder_path').value;
    fetch('/list-files', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({ 'folder_path': folderPath })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const fileContainer = document.getElementById('fileContainer');
            fileContainer.innerHTML = '';
            data.files.forEach(file => {
                const label = document.createElement('label');
                label.className = 'file-label';
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.name = 'file';
                checkbox.value = file.filename;
                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(file.filename));
                fileContainer.appendChild(label);
            });
        }
    });
}

function updateFolderPath(selectId) {
    const selectElement = document.getElementById(selectId);
    const inputElement = document.getElementById(selectId + '_input');

    if (selectElement.value) {
        inputElement.value = selectElement.value;  // Set the input field to the selected value
    } else {
        inputElement.value = '';  // Clear the input field if no option is selected
    }
}

function submitFileList() {
    const fileListTextArea = document.getElementById('file_list');
    const fileList = fileListTextArea.value.trim().split("\n").filter(path => path !== "");

    const destinationFolderInput = document.getElementById('destination_folder_input').value;
    const destinationFolder = destinationFolderInput || document.getElementById('destination_folder').value;

    if (!destinationFolder) {
        alert("Please select a destination folder.");
        return;
    }

    console.log("Submitting file list:", fileList);
    console.log("Destination folder:", destinationFolder);

    // Add new destination folder to history
    updateHistory('destination_folders', destinationFolder);

    document.getElementById('generate_form').submit();
}

function updateHistory(fieldName, newEntry) {
    fetch('/update-history', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ field_name: fieldName, new_entry: newEntry })
    });
}

