import React, { useState } from 'react';
import { saveAs } from 'file-saver';

function GenerateJson() {
    const [sourceFolder, setSourceFolder] = useState('');
    const [destinationFolder, setDestinationFolder] = useState('');
    const [fileList1, setFileList1] = useState('');
    const [fileList2, setFileList2] = useState('');

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

    const handleGenerateJsonFromFolder = () => {
        const folderName = sourceFolder.split('/').pop();
        const jsonData = { files: [] };

        const folderInput = document.createElement('input');
        folderInput.type = 'file';
        folderInput.webkitdirectory = true;
        folderInput.directory = true;
        folderInput.multiple = true;

        folderInput.onchange = () => {
            for (let i = 0; i < folderInput.files.length; i++) {
                jsonData.files.push(folderInput.files[i].name);
            }

            const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' });
            saveAs(blob, `${folderName}.json`);
            alert(`JSON file generated and saved as ${folderName}.json in the source folder`);
        };

        folderInput.click();
    };

    const handleFileDrop = (e, setFileList) => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        let paths = '';
        for (let i = 0; i < files.length; i++) {
            paths += `${files[i].path || files[i].webkitRelativePath || files[i].name}\n`;
        }
        setFileList(paths);
    };

    const handleGenerateJsonFromDragDrop = () => {
        const jsonData = {
            files: [...fileList1.trim().split('\n'), ...fileList2.trim().split('\n')].filter(Boolean)
        };

        const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' });
        saveAs(blob, `${destinationFolder}/dragged_files.json`);
        alert("JSON file generated and saved!");
    };

    return (
        <div>
            <h2>Generate JSON from Folder</h2>
            <button onClick={() => browseFolder(setSourceFolder)}>Select Source Folder</button>
            <button onClick={handleGenerateJsonFromFolder}>Generate JSON from Folder</button>
            
            <h2>Generate JSON from Drag and Drop</h2>
            <input
                type="text"
                value={destinationFolder}
                onChange={(e) => setDestinationFolder(e.target.value)}
                placeholder="Enter destination folder"
            />
            <button onClick={() => browseFolder(setDestinationFolder)}>Browse Destination Folder</button>

            <div
                onDrop={(e) => handleFileDrop(e, setFileList1)}
                onDragOver={(e) => e.preventDefault()}
                className="dropzone"
            >
                Drop files here (Box 1)
            </div>
            <textarea
                value={fileList1}
                onChange={(e) => setFileList1(e.target.value)}
                rows="5"
                style={{ width: '100%' }}
                readOnly
            ></textarea>

            <div
                onDrop={(e) => handleFileDrop(e, setFileList2)}
                onDragOver={(e) => e.preventDefault()}
                className="dropzone"
            >
                Drop files here (Box 2)
            </div>
            <textarea
                value={fileList2}
                onChange={(e) => setFileList2(e.target.value)}
                rows="5"
                style={{ width: '100%' }}
                readOnly
            ></textarea>

            <button onClick={handleGenerateJsonFromDragDrop}>Generate JSON from Drag and Drop</button>
        </div>
    );
}

export default GenerateJson;
