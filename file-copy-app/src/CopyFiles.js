import React, { useState } from 'react';

function CopyFiles() {
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

    const handleCopyFiles = () => {
        if (!jsonFile || !sourceFolder || !destinationFolder) {
            alert("Please provide all the required fields.");
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const jsonData = JSON.parse(e.target.result);
            jsonData.files.forEach(file => {
                console.log(`Copying ${file} from ${sourceFolder} to ${destinationFolder}`);
                // Actual copy logic goes here (Node.js/Backend)
            });
        };
        reader.readAsText(jsonFile);

        alert("Files copied as per JSON!");
    };

    return (
        <div>
            <h2>Copy Files</h2>
            <input type="file" onChange={handleJsonUpload} accept=".json" />
            <button onClick={() => browseFolder(setSourceFolder)}>Select Source Folder</button>
            <button onClick={() => browseFolder(setDestinationFolder)}>Select Destination Folder</button>
            <button onClick={handleCopyFiles}>Copy Files</button>
        </div>
    );
}

export default CopyFiles;
