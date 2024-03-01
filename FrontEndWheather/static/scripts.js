var coords = {
    lat: 0,
    lon: 0
}

// Get the current location
$.getJSON('https://ipinfo.io/geo', function(response) { 
    var loc = response.loc.split(',');
    var city = response.city;
    var region = response.region;

    coords.lat = loc[0];
    coords.lon = loc[1];

    // Initialize a new leaflet map
    var map = new L.map('map').setView([coords.lat, coords.lon], 13);
    window.map = map; //making it a global variable to be accessed in searchbar_scripts.js

    // Create a new layer and add the map to the layer
    var layer = new L.TileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png");
    map.addLayer(layer);

    // Popup for current location
    L.marker([coords.lat, coords.lon]).addTo(map)
        .bindPopup('Current Location')
        .openPopup();

    document.getElementById("location").innerHTML = "Location: " + city + ", " + region;
});

// Close the incorrect password error message
function closeError() {
    errorBox = document.getElementById("error-message");
    errorBox.style.display = "none";
}