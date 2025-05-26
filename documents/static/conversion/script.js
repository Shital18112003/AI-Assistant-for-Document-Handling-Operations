const menuButton = document.getElementById("menu-btn");
const sidebar = document.getElementById("sidebar");
const conversionOption = document.getElementById("conversion-option");
const conversionSection = document.getElementById("conversion-section");
const fileInput = document.getElementById("file-input");
const uploadButton = document.getElementById("upload-btn");
const conversionOptions = document.getElementById("conversion-options");
const pdfToWordButton = document.getElementById('pdf-to-word');

// Toggle sidebar visibility
menuButton.addEventListener("click", () => {
  sidebar.classList.toggle("hidden");
});

// Show conversion section when Conversion option is clicked
conversionOption.addEventListener("click", () => {
  conversionSection.classList.remove("hidden");
  sidebar.classList.add("hidden"); // Close sidebar
});

// Show conversion options after file upload
uploadButton.addEventListener("click", () => {
  if (fileInput.files.length > 0) {
    conversionOptions.classList.remove("hidden");
  } else {
    alert("Please upload a file first.");
  }
});

// Function to handle PDF to Word conversion
pdfToWordButton.addEventListener('click', () => {
  const file = fileInput.files[0];
  console.log("Selected file:", file); // Print selected file

  if (!file) {
    alert('Please upload a file first.');
    return;
  }

  // Create a FormData object to send the file via AJAX
  const formData = new FormData();
  formData.append('file', file);

  // Get CSRF token from the cookie
  const csrftoken = document.cookie.split(';').find(item => item.trim().startsWith('csrftoken=')).split('=')[1];
  console.log("CSRF Token:", csrftoken); // Print CSRF token for debugging

  // Send a POST request to the backend to convert PDF to Word
  fetch('/conversion/pdf-to-word/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrftoken // Include CSRF token in the headers
    },
    body: formData
  })
  .then(response => {
    console.log("Response status:", response.status); // Print response status for debugging
    
    // Check if the response is successful
    if (!response.ok) {
      return response.text().then(text => {
        console.error("Error response body:", text); // Log the error response
        throw new Error(text); // Throw an error with the response text
      });
    }

    // Check if the response is JSON
    const contentType = response.headers.get('content-type');
    if (!contentType?.includes('application/json')) {
      throw new Error('Response is not valid JSON');
  }
  

    return response.json(); // Parse JSON response
  })
  .then(data => {
    console.log("Response data:", data); // Print the response data for debugging

    if (data.error) {
      alert('Error: ' + data.error);
    } else {
      // Provide a link to download the converted Word file
      let downloadLink = document.getElementById('download-link');

      if (!downloadLink) {
        downloadLink = document.createElement('a');
        downloadLink.id = 'download-link'; // Set an ID to avoid duplicates
        downloadLink.textContent = 'Download Word File';
        downloadLink.setAttribute('download', data.word_file); // Set download filename
        document.body.appendChild(downloadLink); // Append link to the body
      }

      downloadLink.href = '/' + data.word_file;  // Assuming media files are served at the root URL
      alert('Conversion successful! Click the link to download your file.'); // Notify user of success
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('An error occurred during the conversion. Check console for details: ' + error.message);
  });
})
