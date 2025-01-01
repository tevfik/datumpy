function fetchDevices() {
    // Make a GET request to your FastAPI application endpoint
    fetch('http://localhost:8000/devices')
        .then(response => response.json())
        .then(data => displayDeviceList(data.device_ids))
        .catch(error => console.error('Error:', error));
}

// Helper function to append device IDs into the DOM
function displayDeviceList(deviceIds) {
    const listElement = document.getElementById("deviceList");

    // Clear any previous content in this element.
    while (listElement.firstChild) {
        listElement.removeChild(listElement.firstChild);
    }

    if (!deviceIds || !Array.isArray(deviceIds)) return;

    deviceIds.forEach(id => {
        const item = document.createElement('div');
        item.textContent = id;
        listElement.appendChild(item);
    });
}
