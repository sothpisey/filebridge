// Function to fetch folder structure from the API
async function fetchFolderStructure() {
  try {
    const response = await fetch("/api/folder-structure");
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    const treeContainer = document.createElement("div");
    treeContainer.classList.add("tree");
    displayFolderStructure(data, treeContainer);
    document.getElementById("folder-structure").appendChild(treeContainer);
  } catch (error) {
    console.error("Failed to fetch folder structure:", error);
  }
}

// Recursive function to display the folder structure
function displayFolderStructure(item, container) {
  const itemDiv = document.createElement("div");
  itemDiv.classList.add(item.type === "folder" ? "folder" : "file");

  // Add name with icon
  const nameDiv = document.createElement("div");
  nameDiv.classList.add("name");
  nameDiv.textContent = item.name;
  itemDiv.appendChild(nameDiv);

  // Add download link if the item is a file or a non-empty folder with a download link
  if (
    item.download_link &&
    (item.type === "file" ||
      (item.type === "folder" && item.children && item.children.length > 0))
  ) {
    const downloadLink = document.createElement("a");
    downloadLink.href = item.download_link;
    downloadLink.target = "_blank";
    downloadLink.classList.add("download-link");

    // Download icon for the link
    const downloadIcon = document.createElement("img");
    downloadIcon.src = "/static/img/download_icon.svg";
    downloadIcon.alt = "Download";
    downloadIcon.style.width = "16px";
    downloadIcon.style.height = "16px";

    downloadLink.appendChild(downloadIcon);
    itemDiv.appendChild(downloadLink);
  }

  if (item.type === "folder") {
    // Create a nested container for folder contents
    const nestedContainer = document.createElement("div");
    nestedContainer.classList.add("nested");

    // Check if folder has children
    if (item.children && item.children.length > 0) {
      item.children.forEach((child) => {
        displayFolderStructure(child, nestedContainer);
      });
    }

    // Toggle visibility of nested items when folder name is clicked
    nameDiv.addEventListener("click", () => {
      itemDiv.classList.toggle("open");
    });

    container.appendChild(itemDiv);
    container.appendChild(nestedContainer);
  } else {
    // Append file directly to the container
    container.appendChild(itemDiv);
  }
}


function checkAuthentication() {
  const token = sessionStorage.getItem('jwt_token');

  if (!token) {
    window.location.href = '/login';
    return;
  } else {
    fetchFolderStructure();
  }
}


checkAuthentication();
