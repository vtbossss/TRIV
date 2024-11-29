// Select form and toast elements
const form = document.getElementById('weather-form');
const toast = document.getElementById('toast');

form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from refreshing the page

    // Get latitude and longitude from the form
    const lat = document.getElementById('lat').value;
    const lon = document.getElementById('lon').value;

    // API URL with dynamic parameters
    const url = `http://localhost/weather/?lat=${lat}&lon=${lon}`;

    // Send GET request with latitude and longitude
    fetch(url)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('Weather data fetched:', data);
        showToast(); // Show success toast
    })
    .catch(error => {
        console.error('Error fetching weather data:', error);
        showToast('Failed to fetch weather data'); // Optionally, show error toast
    });
});

// Show the toast notification
function showToast() {
    toast.classList.add('show'); // Add show class to toast
    setTimeout(function() {
        toast.classList.remove('show'); // Remove show class after 3 seconds
    }, 3000);
}
