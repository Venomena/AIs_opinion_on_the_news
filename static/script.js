function fetchAIStatus() {
    console.log("Fetching AI status...");
    fetch('http://192.168.2.105:5004/ai-status')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('status').textContent = data.status;
        })
        .catch(error => console.error('Error fetching AI status:', error));
}

document.addEventListener("DOMContentLoaded", function() {
    fetchAIStatus(); // Call initially
    setInterval(fetchAIStatus, 2000); // Refresh every 2 seconds
});
