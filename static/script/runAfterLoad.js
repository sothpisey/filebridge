function displayFolderStructure(item, container, isRoot = false) {
  const itemDiv = document.createElement('div');
  itemDiv.classList.add(item.type === 'folder' ? 'folder' : 'file');

  const nameDiv = document.createElement('div');
  nameDiv.classList.add('name');

  nameDiv.appendChild(document.createTextNode(item.name));
  itemDiv.appendChild(nameDiv);

  if (
    item.download_link &&
    (item.type === 'file' ||
      (item.type === 'folder' && item.children && item.children.length > 0))
  ) {
    const downloadLink = document.createElement('a');
    downloadLink.href = item.download_link;
    downloadLink.target = '_blank';
    downloadLink.classList.add('download-link');

    const downloadIcon = document.createElement('img');
    downloadIcon.src = '/static/img/download_icon.svg';
    downloadIcon.alt = 'Download';
    downloadIcon.style.width = '16px';
    downloadIcon.style.height = '16px';

    const homeIcon = document.createElement('img');
    homeIcon.src = '/static/img/home_icon.svg';
    homeIcon.alt = 'Home';
    homeIcon.style.width = '16px';
    homeIcon.style.height = '16px';
    
    if (isRoot) {
      downloadLink.appendChild(homeIcon);
      downloadLink.style.pointerEvents = 'none';
      itemDiv.appendChild(downloadLink);
    } 
    else {
      downloadLink.appendChild(downloadIcon);
      itemDiv.appendChild(downloadLink);
    } 
  }

  if (item.type === 'folder') {
    const nestedContainer = document.createElement('div');
    nestedContainer.classList.add('nested');

    if (item.children && item.children.length > 0) {
      item.children.forEach((child) => {
        displayFolderStructure(child, nestedContainer);
      });
    }

    nameDiv.addEventListener('click', () => {
      itemDiv.classList.toggle('open');
    });

    container.appendChild(itemDiv);
    container.appendChild(nestedContainer);
  } else {
    container.appendChild(itemDiv);
  }
}


async function fetchFolderStructure(jwt_token) {
  try {
    const response = await fetch('/api/folder-structure', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${jwt_token}`
      }
    });
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    const data = await response.json();
    const treeContainer = document.createElement('div');
    treeContainer.classList.add('tree');
    displayFolderStructure(data, treeContainer, true);
    document.getElementById('folder-structure').appendChild(treeContainer);
  } catch (error) {
    console.error('Failed to fetch folder structure:', error);
  }
}
const jwt_token = sessionStorage.getItem('jwt_token');
fetchFolderStructure(jwt_token);


document.addEventListener('DOMContentLoaded', function () {
  const button = document.getElementById('logout');
  button.addEventListener('click', () => {
    sessionStorage.removeItem('jwt_token');
    if (!sessionStorage.getItem('jwt_token')) {
        window.location.href = '/login';
    }
  });
});