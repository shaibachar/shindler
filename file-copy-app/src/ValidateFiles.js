import React, { useState } from 'react';

function ValidateFiles() {
    const [jsonFile, setJsonFile] = useState(null);
    const [sourceFolder, setSourceFolder] = useState('');
    const [destinationFolder, setDestinationFolder] = useState('');

    const browseFolder = (setFolder) => {
        const folderInput = document.createElement('input');
        folderInput.type = 'file';
        folderInput.webkitdirectory = true;
        folderInput.directory = true;
        folderInput.multiple = false;

        folderInput.onchange = () => {
            if (folderInput.files.length > 0) {
                const folderPath = folderInput.files[0].webkitRelativePath.split('/')[0];
                setFolder(folderPath);
            }
        };

        folderInput.click();
    };

    const handleJsonUpload = (e) => {
        setJsonFile(e.target.files[0]);
    };

    const handleValidateFiles = () => {
        if (!jsonFile || !sourceFolder || !destinationFolder) {
            alert("Please provide all the required fields.");
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const jsonData = JSON.parse(e.target.result);
            const missingFiles = [];
            jsonData.files.forEach(file => {
                console.log(`Validating ${file} from ${sourceFolder} to ${destinationFolder}`);
                // Actual validation logic goes here (Node.js/Backend)
            });

            if (missingFiles.length > 0) {
                alert(`Validation failed. Missing files: ${missingFiles.join(', ')}`);
            } else {
                alert("Validation successful. All files were copied correctly.");
            }
        };
        reader.readAsText(jsonFile);
    };

    return (
        <div>
            <h2>Validate Copy Files</h2>
            <input type="file" onChange={handleJsonUpload} accept=".json" />
            <button onClick={() => browseFolder(setSourceFolder)}>Select Source Folder</button>
            <button onClick={() => browseFolder(setDestinationFolder)}>Select Destination Folder</button>
            <button onClick={handleValidateFiles}>Validate Files</button>
        </div>
    );
}

export default ValidateFiles;
