document.getElementById("trigger").onclick = function () {
    document.getElementById("overlay").style.display = "block";
    document.getElementById("loginModal").style.display = "block";
};

document.getElementById("closeModal").onclick = function () {
    closeModal();
};

document.getElementById("overlay").onclick = function () {
    closeModal();
};

document.getElementById('form').addEventListener('submit', handleFormSubmission);

const vent = document.getElementById('vent');
const triggerButton = document.getElementById("trigger"); // Reference to the login trigger button
const logoutButton = document.getElementById("logout"); // Reference to the logout button

function handleFormSubmission(event) {
    event.preventDefault(); // Prevent form submission

    const user = document.getElementById('user').value;
    const passwd = document.getElementById('passwd').value;

    const xhr = new XMLHttpRequest();
    const isLogin = event.submitter.id === 'hulu'; // Determine if it's a login or register

    xhr.open('POST', isLogin ? '/login' : '/register', true);
    xhr.setRequestHeader('Content-type', 'application/json');

    xhr.onload = function() {
        let response; // Define the response variable
        try {
            response = JSON.parse(this.responseText); // Attempt to parse the response
        } catch (error) {
            vent.textContent = "Error parsing response: " + error.message; // Handle JSON parsing errors
            return; // Exit the function if parsing fails
        }

        vent.textContent = response.message; // Display response message

        if (xhr.status === 200) {
            if (isLogin) {
                triggerButton.style.display = "none"; // Hide login button on successful login
                logoutButton.style.display = "inline"; // Show logout button
            }
            // Close the login modal if login is successful
            closeModal();
        } else {
            vent.textContent = response.message; // Show error message
        }
    };

    xhr.onerror = function() {
        vent.textContent = xhr.statusText;
    };

    xhr.send(JSON.stringify({ user: user, passwd: passwd }));
}

// Logout functionality
logoutButton.onclick = function () {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/logout', true); // Send a GET request to /logout

    xhr.onload = function() {
        if (xhr.status === 200) {
            vent.textContent = "Successfully logged out.";
            triggerButton.style.display = "inline"; // Show login button
            logoutButton.style.display = "none"; // Hide logout button
        } else {
            vent.textContent = "Error logging out.";
        }
    };

    xhr.onerror = function() {
        vent.textContent = "Error: " + xhr.statusText;
    };

    xhr.send(); // Send the logout request
};

// Handle reservation form submission


// Function to close the modal
function closeModal() {
    document.getElementById("overlay").style.display = "none";
    document.getElementById("loginModal").style.display = "none";
}
