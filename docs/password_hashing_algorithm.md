# Hashing Algorithm Documentation
This document explains the hashing algorithm used in my project to securely store and verify user passwords. The algorithm is implemented using Python's `hashlib` library and incorporates random salts and iterations to enhance security.

## Overview
The hashing mechanism relies on the **PBKDF2 (Password-Based Key Derivation Function 2)** algorithm with the following key principles:

1. **Salt:** A random, unique value is generated for each password to prevent pre-computed dictionary attacks (e.g., rainbow table attacks).
2. **Iterations:** A random number of iterations is applied to increase the computational cost, making brute-force attacks more difficult.
3. **Secure Hash Algorithm:** PBKDF2 uses `SHA-256`, a secure hashing algorithm, to generate the password hash.

The hashing mechanism includes two main functions:

* `get_password_hash` for generating password hashes.
* `verify_password` for verifying a plain-text password against the stored hash.

## Implementation Details
### Function: `get_password_hash`
This function generates a hashed password with the following steps:

1. **Generate Salt:** If no salt is provided, a 16-byte random salt is generated using `random.randbytes(16)`.
2. **Generate Iterations:** A random number of iterations (between 10,000 and 100,000) is used to strengthen the hash.
3. **Hashing Process:** The `hashlib.pbkdf2_hmac` function is applied with:
   * **Algorithm:** `sha256`
   * **Password:** User's plain-text password
   * **Salt:** Randomly generated or provided
   * **Iterations:** Randomly generated or provide
4. **Encoding Output:** The result is a string in the format:
    ```r
    iterations$salt$hashed_password
    ```
    where:
    * **iterations:** Number of iterations (integer).
    * **salt:** Base64-encoded salt (string).
    * **hashed_password:** Base64-encoded hashed value (string).
#### Code
```python
import hashlib
import random
import base64

def get_password_hash(password: str, salt: bytes = None, iterations: int = None) -> str:
    if salt is None:
        salt = random.randbytes(16)
    if iterations is None:
        iterations = random.randint(10000, 100000)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
    return f'{iterations}${base64.b64encode(salt).decode('utf-8')}${base64.b64encode(hashed).decode('utf-8')}'
```

### Function: `verify_password`
This function verifies a plain-text password against a hashed password. Steps include:

* **Extract Components:** Parse the hashed password into `iterations`, `salt`, and `hashed_password`.
* **Rehash Password:** Apply the same hashing process to the provided plain-text password using the extracted salt and iterations.
* **Compare Hashes:** Base64-encode the result and compare it to the stored hash. If they match, the password is valid.
  
#### Code:
```python
def verify_password(plain_password: str, hashed_password: str) -> bool:
    iterations, salt, hashed = hashed_password.split('$')
    hashed_from_plain_password = hashlib.pbkdf2_hmac(
        'sha256', 
        plain_password.encode(), 
        base64.b64decode(salt), 
        int(iterations)
    )
    return base64.b64encode(hashed_from_plain_password).decode('utf-8') == hashed
```

## Advantages of This Hashing Algorithm

1. **Salt Prevents Rainbow Table Attacks:** Each password hash uses a unique random salt, making it infeasible to pre-compute hash values.
2. **Dynamic Iterations Add Flexibility:** The number of iterations can vary, adding an extra layer of complexity.
3. **Resilient Against Brute Force:** Higher iteration counts increase the time required to compute each hash, slowing down brute-force attempts.
4. **Secure Hashing Function:** The use of `SHA-256` provides strong cryptographic guarantees.


## Security Considerations
1. **Secure Randomness:** Ensure that the `random.randbytes` and `random.randint` functions provide cryptographically secure random values. If necessary, replace with `secrets` for additional security.
2. **Iteration Count:** Adjust the iteration range as needed to balance security and performance for your system.
3. **Store Hashes Securely:** Always store the generated hashes in a secure, access-controlled environment.