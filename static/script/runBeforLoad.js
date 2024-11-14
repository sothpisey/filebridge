function checkAuthentication() {
  const token = sessionStorage.getItem('jwt_token');

  if (!token) {
    window.location.href = '/login';
  }
}

checkAuthentication();