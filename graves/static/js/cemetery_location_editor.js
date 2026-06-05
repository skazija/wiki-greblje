document.addEventListener("DOMContentLoaded", function () {

    const latField = document.getElementById("id_latitude");
    const lonField = document.getElementById("id_longitude");

    if (!latField || !lonField) {
        return;
    }

    if (typeof L === "undefined") {
        console.error("Leaflet nije učitan.");
        return;
    }

    const wrapper = lonField.closest(".form-row") || lonField.parentNode;

    const mapContainer = document.createElement("div");
    mapContainer.id = "cemetery-map";
    mapContainer.style.height = "450px";
    mapContainer.style.marginTop = "15px";
    mapContainer.style.marginBottom = "15px";
    mapContainer.style.borderRadius = "10px";
    mapContainer.style.border = "1px solid #ccc";

    wrapper.parentNode.insertBefore(
        mapContainer,
        wrapper.nextSibling
    );

    let lat = parseFloat(latField.value);
    let lon = parseFloat(lonField.value);

    if (isNaN(lat) || isNaN(lon)) {
        lat = 44.2;
        lon = 17.9;
    }

    const map = L.map("cemetery-map").setView([lat, lon], 8);

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 22,
        }
    ).addTo(map);

    let marker = L.marker([lat, lon], {
        draggable: true
    }).addTo(map);

    function updateFields(position) {
        latField.value = position.lat;
        lonField.value = position.lng;
    }

    marker.on("dragend", function () {
        updateFields(marker.getLatLng());
    });

    map.on("click", function (e) {
        marker.setLatLng(e.latlng);
        updateFields(e.latlng);
    });

    setTimeout(function () {
        map.invalidateSize();
    }, 500);
});