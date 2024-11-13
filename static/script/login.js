document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch('/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                'username': username,
                'password': password,
            })
        });

        if (!response.ok) {
            throw new Error('Login failed');
        }

        const data = await response.json();
        const token = data.access_token;

        sessionStorage.setItem('jwt_token', token);
        window.location.href = '/';
    } catch (error) {
        console.error('Error:', error);
        loginFailedMessage();
    }
});


const loginFailed = document.getElementById('login-failed')
const errorIcon = document.getElementById('error-icon')
async function loginFailedMessage() {
    loginFailed.classList.add('active');
    errorIcon.classList.add('active')
    setTimeout(() => {
        loginFailed.classList.remove('active');
        errorIcon.classList.remove('active')
    }, 3000);
}