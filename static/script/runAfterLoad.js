document.addEventListener('DOMContentLoaded', function () {
  const button = document.getElementById('logout');
  button.addEventListener('click', () => {
    sessionStorage.removeItem('jwt_token');
    if (!sessionStorage.getItem('jwt_token')) {
        window.location.href = '/login';
    }
  });
});