    // Function to show toast
    function showToast(message) {
        const toast = document.createElement('div');
        toast.textContent = message;

         // Toast Styling
         toast.style.position = 'fixed';
         toast.style.top = '20px'; /* Position to top */
         toast.style.right = '20px'; /* Position to the right */
         toast.style.backgroundColor = '#4caf50';
         toast.style.color = 'white';
         toast.style.padding = '10px 20px';
         toast.style.borderRadius = '5px';
         toast.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
         toast.style.zIndex = '1000'; /* Ensure it appears on top */

        document.body.appendChild(toast);

        // Remove toast after 3 seconds
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

// Function to change button text to "Welcome"
function changeButtonText() {
    const loginButton = document.getElementById('loginButton');
    loginButton.textContent = 'Welcome'; // Change button text
}


    // Check for login toast
    window.onload = () => {
        const loginToast = localStorage.getItem('loginToast');
        if (loginToast) {
            showToast(loginToast);
            changeButtonText();
            localStorage.removeItem('loginToast'); // Clear the message
           
            
           
        }
    };