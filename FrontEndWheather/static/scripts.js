// Initialize a new leaflet map
var map = new L.map('map', {zoom: 10}).locate({setView: true, maxZoom: 16});

// Create a new layer and add the map to the layer
var layer = new L.TileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");
map.addLayer(layer);

// Close the incorrect password error message
function closeError() {
    errorBox = document.getElementById("error-message");
    errorBox.style.display = "none";
}