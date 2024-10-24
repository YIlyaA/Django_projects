document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll(".message");

    // If there are messages, display them as popup notifications
    messages.forEach(function (message) {
        let messageText = message.textContent;
        let messageType = message.classList.contains("success") ? "success" : "error";

        // Create a popup div
        let popup = document.createElement("div");
        popup.className = `popup-message ${messageType}`;
        popup.textContent = messageText;

        // Add the popup to the body
        document.body.appendChild(popup);

        // Automatically remove the popup after 3 seconds
        setTimeout(function () {
            popup.style.opacity = "0";  // Fade out effect
            setTimeout(function () {
                popup.remove();  // Remove element from DOM
            }, 500);  // Wait for fade out to complete
        }, 3000);  // Display for 3 seconds
    });
});
