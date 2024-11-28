function handleLogin() {
  // Example: Check credentials (mock logic here)
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  if (username === 'admin' && password === 'password') {
      // Store toast message in localStorage
      localStorage.setItem('loginToast', 'You have successfully logged in!');
      // Redirect to index.html
      window.location.href = 'index.html';
  } else {
      alert('Invalid credentials!');
  }
}