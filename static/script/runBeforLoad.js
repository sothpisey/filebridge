async function verifyToken(token) {
  const endpoint = `/verify_token/${token}`;

  try {
    const response = await fetch(endpoint, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const isValid = await response.json();
    console.log('Token verification result:', isValid);
    return isValid;
  } catch (error) {
    console.error('Error verifying token:', error);
    return false;
  }
}

function isTokenExpired(jwt_token) {
  const exp_date = JSON.parse(atob(jwt_token.split('.')[1])).exp;
  const current_date = Math.floor(Date.now() / 1000);
  if (current_date >= exp_date) {
    console.warn('The Token has expired!');
    sessionStorage.removeItem('jwt_token');
    window.location.href = '/login';
    return true;
  } else {
    return false;
  }
}


async function startTokenVerification(intervalMs) {
  const verifyAndHandle = async () => {
    const jwt_token = sessionStorage.getItem('jwt_token');

    if (!jwt_token) {
      console.warn('No token found, redirecting to login...');
      window.location.href = '/login';
      return;
    }

    if (!isTokenExpired(jwt_token)) {
      const isValid = await verifyToken(jwt_token);
      if (!isValid) {
        console.warn('Invalid token, logging out...');
        sessionStorage.removeItem('jwt_token');
        window.location.href = '/login';
      }
    }
  }

  await verifyAndHandle();
  setInterval(verifyAndHandle, intervalMs);
}


startTokenVerification(900000);