const form = document.getElementById('weather-form');
const toast = document.getElementById('toast');

form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form refresh

    // Get latitude and longitude from the form
    const lat = document.getElementById('lat').value;
    const lon = document.getElementById('lon').value;

    // API URL with dynamic parameters
    const url = `http://localhost:8000/weather/?lat=${lat}&lon=${lon}`;

    // Send GET request with Axios
    axios.get(url)
        .then(response => {
            console.log('Weather data fetched:', response.data);
            showToast('Data fetched successfully!');
        })
        .catch(error => {
            console.error('Error fetching weather data:', error.message);
            showToast('Failed to fetch weather data');
        });
});

// Show the toast notification
function showToast(message) {
    toast.textContent = message;
    toast.classList.remove('hidden'); // Show toast
    setTimeout(() => {
        toast.classList.add('hidden'); // Hide toast after 3 seconds
    }, 3000);
}