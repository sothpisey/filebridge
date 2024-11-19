![FileBridge Logo](/docs/media/filebridge.png)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://raw.githubusercontent.com/sothpisey/filebridge/refs/heads/main/LICENSE)

# FileBridge 📂
FileBridge is a streamlined web application that simplifies file transfers over a LAN network. Built with the powerful **FastAPI** framework, it provides users with an intuitive, explorer-like interface to browse and transfer files seamlessly.

## Features
* **User-Friendly Interface**: Navigate files and directories with ease.
* **FastAPI Framework**: Leverages FastAPI's speed and simplicity for robust performance.

## Prerequisites
### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/sothpisey/filebridge.git
    cd filebridge
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create the `config.json` file as described above.

4. Start the development server:
* Windows:
    ```bash
    uvicorn main:app --reload
    ```
    
* Linux or Mac:
    ```bash
    python3 -m uvicorn main:app --reload
    ```

5. Open your browser and navigate to `http://127.0.0.1:8000`.

### Create `config.json` file
Before running the application, ensure you have created a `config.json` file in the project root directory (`filebridge`). This file should contain configuration details in the following format:

```json
{
    "path": "\\path\\to\\your\\folder",
    "user_db": {
        "yourname": {
            "username": "yourname", 
            "full_name": "YOUR Name", 
            "email": "yourname@example.com",
            "hashed_password": "22159$l7tcfA+DtCyYF9GNOdg3+A==$m/ZTD9ydtO6sDpaeodSMzhHZ4lJsGoMb9xNq+dBXCtQ="
        }
    }
}
```

## Explanation of Configuration Fields
* **path**: The directory path for file operations (folder you want to share file).
* **user_db**: A dictionary containing user authentication details. Replace sample values with your own, in order to create `hashed_password` please check this [PBKDF2 Document](/docs/password_hashing_algorithm.md).

## Usage

* Authenticate using credentials defined in `config.json`.
* Authenticate with user credentials defined in config.json.
* Seamlessly transfer files within local network.

## API Documentation
### Authentication
1. Login for Access Token
    * POST `/token`
    * **Description:** Authenticates a user and returns an access token.
    * **Request Body:**
 
        ```json
        {
            "username": "string",
            "password": "string"
        }
        ```
    * **Response:**

        ```json
        {
            "access_token": "string",
            "token_type": "bearer"
        }
        ```
2. Verify Token
    * GET `/verify_token/{token}`
    * **Description:** Validates an access token.
### File Operations
1. Get Folder Structure
    * GET `/api/folder-structure`
    * **Description:** Retrieves the structure of the specified folder.
2. Download File
    * GET `/api/download/{file_name}`
    * **Description:** Downloads a specified file.
3. Download Folder
    * GET `/api/download-folder/{folder_path}`
    * **Description:** Downloads a specified folder as an archive.

## Example Usage with `curl`
### Get Folder Structure
```bash
curl -X GET "http://127.0.0.1:8000/api/folder-structure" \
-H "Authorization: Bearer <your_access_token>"
```
### Download File
```bash
curl -X GET "http://127.0.0.1:8000/api/download/<file_name>" \
-H "Authorization: Bearer <your_access_token>" -O
```

## Application Overview ▶️
![Alt Text](/docs/media/application_overview.gif)

## License
This project is licensed under the [MIT License](/LICENSE).