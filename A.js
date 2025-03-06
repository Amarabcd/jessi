function toggleDetails() {
    var details = document.getElementById("movieDetails");
    var button = document.querySelector("button");
    
    if (details.style.display === "none") {
        details.style.display = "block";
        button.textContent = "Hide Details";  // Button text change karega
    } else {
        details.style.display = "none";
        button.textContent = "Show Details";  // Wapas hide karne ka option
    }
}
