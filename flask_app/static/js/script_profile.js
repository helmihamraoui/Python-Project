// Get references to the image and the popup list
const image = document.getElementById("clickable-image");
const popup = document.getElementById("popup-list");

// Add an event listener to the image
image.addEventListener("click", function() {
    // Toggle the popup visibility
    popup.style.display = popup.style.display === "block" ? "none" : "block";
});

// Optionally close the popup if clicked outside (optional)
window.addEventListener("click", function(event) {
    if (!popup.contains(event.target) && event.target !== image) {
        popup.style.display = "none";
    }
});
