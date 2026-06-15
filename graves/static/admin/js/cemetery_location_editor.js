document.addEventListener("DOMContentLoaded", function () {

    const latField = document.getElementById("id_latitude");
    const lonField = document.getElementById("id_longitude");
    const boundaryField = document.getElementById("id_boundary_geojson");

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
    mapContainer.style.height = "500px";
    mapContainer.style.marginTop = "15px";
    mapContainer.style.marginBottom = "15px";
    mapContainer.style.borderRadius = "10px";
    mapContainer.style.border = "1px solid #ccc";

    const helpText = document.createElement("p");
    helpText.innerHTML = "Klik na mapu pomjera lokaciju groblja. Za granicu koristi dugmad ispod mape.";
    helpText.style.marginTop = "10px";
    helpText.style.color = "#666";

    const controls = document.createElement("div");
    controls.style.marginBottom = "15px";

    const drawButton = document.createElement("button");
    drawButton.type = "button";
    drawButton.textContent = "Crtaj granicu";
    drawButton.className = "button";

    const clearButton = document.createElement("button");
    clearButton.type = "button";
    clearButton.textContent = "Očisti granicu";
    clearButton.className = "button";
    clearButton.style.marginLeft = "10px";

    controls.appendChild(drawButton);
    controls.appendChild(clearButton);

    wrapper.parentNode.insertBefore(helpText, wrapper.nextSibling);
    wrapper.parentNode.insertBefore(mapContainer, helpText.nextSibling);
    wrapper.parentNode.insertBefore(controls, mapContainer.nextSibling);

    let lat = parseFloat(latField.value);
    let lon = parseFloat(lonField.value);

    if (isNaN(lat) || isNaN(lon)) {
        lat = 44.2;
        lon = 17.9;
    }

    const map = L.map("cemetery-map").setView([lat, lon], 16);

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        { maxZoom: 22 }
    ).addTo(map);

    let marker = L.marker([lat, lon], {
        draggable: true
    }).addTo(map);

    function updateLocationFields(position) {
        latField.value = position.lat;
        lonField.value = position.lng;
    }

    marker.on("dragend", function () {
        updateLocationFields(marker.getLatLng());
    });

    let drawingBoundary = false;
    let boundaryPoints = [];
    let boundaryMarkers = [];
    let boundaryPolygon = null;

    function redrawBoundary() {
        boundaryMarkers.forEach(function (m) {
            map.removeLayer(m);
        });

        boundaryMarkers = [];

        if (boundaryPolygon) {
            map.removeLayer(boundaryPolygon);
            boundaryPolygon = null;
        }

        boundaryPoints.forEach(function (point) {
            const m = L.circleMarker(point, {
                radius: 5
            }).addTo(map);

            boundaryMarkers.push(m);
        });

        if (boundaryPoints.length >= 3) {
            boundaryPolygon = L.polygon(boundaryPoints).addTo(map);
        }

        if (boundaryField) {
            boundaryField.value = JSON.stringify(boundaryPoints);
        }
    }

    map.on("click", function (e) {
        if (drawingBoundary) {
            boundaryPoints.push([e.latlng.lat, e.latlng.lng]);
            redrawBoundary();
        } else {
            marker.setLatLng(e.latlng);
            updateLocationFields(e.latlng);
        }
    });

    drawButton.addEventListener("click", function () {
        drawingBoundary = !drawingBoundary;

        if (drawingBoundary) {
            drawButton.textContent = "Završi crtanje";
        } else {
            drawButton.textContent = "Crtaj granicu";
        }
    });

    clearButton.addEventListener("click", function () {
        boundaryPoints = [];
        if (boundaryField) {
            boundaryField.value = "";
        }
        redrawBoundary();
    });

    setTimeout(function () {
        map.invalidateSize();
    }, 500);
});