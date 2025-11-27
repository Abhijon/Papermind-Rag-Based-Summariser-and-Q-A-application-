document.addEventListener('DOMContentLoaded', () => {
    const sourceModelSelect = document.getElementById('sourceModel');
    const sourceTypeSelect = document.getElementById('sourceType');
    const inputFields = document.getElementById('inputFields');
    const generateSummaryBtn = document.getElementById('generateSummaryBtn');
    const summaryResult = document.getElementById('summaryResult');

    // Store selected files
    let uploadedFiles = [];

    sourceTypeSelect.addEventListener('change', () => {
        const selectedOption = sourceTypeSelect.value;
        uploadedFiles = []; // Reset files on type change

        // Hide all input fields
        inputFields.innerHTML = '';

        // Dynamically add input fields based on the selected source type
        if (selectedOption === 'youtube') {
            // Add input field for YouTube video link
            inputFields.innerHTML = `
                    <label for="youtubeLink">Enter YouTube Video Link:</label>
                    <input type="text" id="youtubeLink" name="text" placeholder="https://www.youtube.com/watch?v=...">
                `;
        } else if (selectedOption === 'pdf') {
            inputFields.innerHTML = `
                    <div class="pdf-upload">
                        <div class="drop-pdf-upload">
                        <div id="pdfFileDropArea">
                            <p id="file-name">Drag/drop files here <br> or<br>Select files</p>
                            <input type="file" id="pdfFileInput" accept=".pdf" multiple style="display: none;">
                        </div>
                        </div>
                        <div id="fileListContainer" style="margin-top: 10px;">
                            <ul id="fileList" style="list-style: none; padding: 0;"></ul>
                        </div>
                        <div id="pagenumbers">
                            <label for="from">From PageNo.: </label>
                            <input class="pagenumber" type="number" id="from" placeholder="From:" required>
                            <label for="till">Till PageNo.: </label>
                            <input class="pagenumber" type="number" id="till" placeholder="Till:" required>
                        </div>
                    </div>
                `;

            // Add event listeners for drag-and-drop functionality
            const pdfFileDropArea = document.getElementById('pdfFileDropArea');
            const pdfFileInput = document.getElementById('pdfFileInput');

            pdfFileDropArea.addEventListener('click', () => {
                pdfFileInput.click(); // Trigger the hidden input file element
            });
            pdfFileDropArea.addEventListener('dragover', (e) => {
                e.preventDefault(); // Prevent default behavior
                pdfFileDropArea.classList.add('dragover'); // Add a CSS class for styling
            });

            pdfFileDropArea.addEventListener('dragleave', () => {
                pdfFileDropArea.classList.remove('dragover'); // Remove the dragover class
            });

            pdfFileDropArea.addEventListener('drop', (e) => {
                e.preventDefault(); // Prevent default behavior
                pdfFileDropArea.classList.remove('dragover'); // Remove the dragover class
                const files = e.dataTransfer.files; // Get the dropped files
                handleDroppedFiles(files);
            });

            pdfFileInput.addEventListener('change', (e) => {
                const files = e.target.files; // Get the selected files
                handleDroppedFiles(files);
                // Reset input value so the same file can be selected again if needed
                pdfFileInput.value = '';
            });

            function handleDroppedFiles(files) {
                for (const file of files) {
                    // Check if file is PDF
                    if (file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')) {
                        // Avoid duplicates based on name
                        if (!uploadedFiles.some(f => f.name === file.name)) {
                            uploadedFiles.push(file);
                        }
                    }
                }
                renderFileList();
            }

            function renderFileList() {
                const fileList = document.getElementById('fileList');
                fileList.innerHTML = '';

                if (uploadedFiles.length === 0) {
                    document.getElementById("file-name").innerText = "Drag/drop files here \n or\nSelect files";
                    return;
                }

                document.getElementById("file-name").innerText = `${uploadedFiles.length} file(s) selected`;

                uploadedFiles.forEach((file, index) => {
                    const li = document.createElement('li');
                    li.style.display = 'flex';
                    li.style.alignItems = 'center';
                    li.style.marginBottom = '5px';
                    li.style.padding = '5px';
                    li.style.backgroundColor = '#f0f0f0';
                    li.style.borderRadius = '4px';

                    // Checkbox
                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.checked = true;
                    checkbox.id = `file-check-${index}`;
                    checkbox.style.marginRight = '10px';

                    // File Name
                    const nameSpan = document.createElement('span');
                    nameSpan.textContent = file.name;
                    nameSpan.style.flexGrow = '1';
                    nameSpan.style.overflow = 'hidden';
                    nameSpan.style.textOverflow = 'ellipsis';
                    nameSpan.style.whiteSpace = 'nowrap';
                    nameSpan.style.marginRight = '10px';

                    // Fix visibility and make clickable
                    nameSpan.style.color = '#333'; // Dark text for visibility
                    nameSpan.style.cursor = 'pointer';
                    nameSpan.title = "Click to view PDF";

                    nameSpan.onclick = () => {
                        const fileURL = URL.createObjectURL(file);
                        window.open(fileURL, '_blank');
                    };

                    // Delete Button (Cross)
                    const deleteBtn = document.createElement('span');
                    deleteBtn.innerHTML = '&#10006;'; // Cross symbol
                    deleteBtn.style.cursor = 'pointer';
                    deleteBtn.style.color = 'red';
                    deleteBtn.style.fontWeight = 'bold';
                    deleteBtn.onclick = (e) => {
                        e.stopPropagation(); // Prevent triggering drop area click
                        removeFile(index);
                    };

                    li.appendChild(checkbox);
                    li.appendChild(nameSpan);
                    li.appendChild(deleteBtn);
                    fileList.appendChild(li);
                });
            }

            function removeFile(index) {
                uploadedFiles.splice(index, 1);
                renderFileList();
            }
        } else if (selectedOption === 'text') {
            inputFields.innerHTML = `
                    <label for="longText">Enter Long Text:</label>
                    <textarea id="longText" name="text" rows="6" placeholder="Enter your text here..."></textarea>
                `;
        } else if (selectedOption === 'select') {
            inputFields.innerHTML = `
                `;
        }
    });

    generateSummaryBtn.addEventListener('click', function (event) {
        event.preventDefault();

        const selectedOption = sourceTypeSelect.value;
        const selectedModel = sourceModelSelect.value;
        let inputText = 'Nonee';
        let till = 'Nonee';
        let from = 'Nonee';
        let goOn = false;

        const formData = new FormData();

        if (selectedOption === 'youtube' || selectedOption === 'text') {
            inputText = document.getElementById(selectedOption === 'youtube' ? 'youtubeLink' : 'longText').value;
            if (inputText.trim() !== '') {
                goOn = true;
            }
            formData.append('inputText', inputText);
        }
        else if (selectedOption == 'pdf') {
            from = document.getElementById('from').value;
            till = document.getElementById('till').value;

            // Get checked files
            const fileList = document.getElementById('fileList');
            let hasFiles = false;

            if (fileList) {
                const listItems = fileList.getElementsByTagName('li');
                for (let i = 0; i < listItems.length; i++) {
                    const checkbox = listItems[i].querySelector('input[type="checkbox"]');
                    if (checkbox && checkbox.checked) {
                        formData.append('file', uploadedFiles[i]);
                        hasFiles = true;
                    }
                }
            }

            if (hasFiles) {
                goOn = true;
                inputText = "Multiple Files"; // Placeholder
            } else {
                alert("Please select at least one file to process.");
                return;
            }

            formData.append('inputText', inputText);
        }

        if (goOn) {
            this.disabled = true;
            document.getElementById("processingAnimation").classList.remove("hidden");

            formData.append('selectedOption', selectedOption);
            formData.append('selectedModel', selectedModel);
            formData.append('from', from);
            formData.append('till', till);

            fetch('/summary', {
                method: 'POST',
                body: formData,
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then((data) => {
                    summaryResult.innerHTML = data.result;
                    document.getElementById("processingAnimation").classList.add("hidden");
                    this.disabled = false;
                    const qaSection = document.getElementById('qaSection'); if (qaSection) { qaSection.style.display = 'block'; }
                })
                .catch((error) => {
                    console.error('Error:', error);
                    document.getElementById("processingAnimation").classList.add("hidden");
                    this.disabled = false;
                    alert("An error occurred while generating the summary.");
                });
        } else {
            alert("Error!! Enter details Correctly!!");
        }
    });

});