document.addEventListener("DOMContentLoaded", function () {
    const latInput = document.getElementById("id_latitude");
    const lonInput = document.getElementById("id_longitude");

    if (!latInput || !lonInput || typeof L === "undefined") {
        return;
    }

    const mapDiv = document.createElement("div");
    mapDiv.id = "custom-grave-map";
    mapDiv.style.height = "420px";
    mapDiv.style.width = "100%";
    mapDiv.style.marginTop = "12px";
    mapDiv.style.border = "1px solid #ccc";
    mapDiv.style.borderRadius = "8px";

    const locationFieldset = lonInput.closest(".form-row")
    || lonInput.closest(".field-longitude")
    || lonInput.parentNode;

    locationFieldset.appendChild(mapDiv);

    let startLat = parseFloat(latInput.value);
    let startLon = parseFloat(lonInput.value);

    if (isNaN(startLat) || isNaN(startLon)) {
        startLat = 43.9889;
        startLon = 18.1781;
    }

    const map = L.map("custom-grave-map").setView([startLat, startLon], 18);
    const cemeterySelect = document.getElementById("id_cemetery");
    const osm = L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            maxZoom: 22,
            attribution: "© OpenStreetMap"
        }
    );

    const satellite = L.tileLayer(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        {
            maxZoom: 22,
            attribution: "Tiles © Esri"
        }
    );

    osm.addTo(map);

    L.control.layers({
        "Mapa": osm,
        "Satelit": satellite
    }).addTo(map);

    let marker = null;

    function updateInputs(latlng) {
        latInput.value = latlng.lat.toFixed(7);
        lonInput.value = latlng.lng.toFixed(7);
    }

    if (!isNaN(startLat) && !isNaN(startLon)) {
        marker = L.marker([startLat, startLon], {
            draggable: true
        }).addTo(map);

        marker.on("dragend", function () {
            updateInputs(marker.getLatLng());
        });
    }

    map.on("click", function (e) {
        if (!marker) {
            marker = L.marker(e.latlng, {
                draggable: true
            }).addTo(map);

            marker.on("dragend", function () {
                updateInputs(marker.getLatLng());
            });
        } else {
            marker.setLatLng(e.latlng);
        }

        updateInputs(e.latlng);
    });

    setTimeout(function () {
        map.invalidateSize();
    }, 400);

    if (cemeterySelect) {

        cemeterySelect.addEventListener("change", async function () {

            const cemeteryId = this.value;

            if (!cemeteryId) {
                return;
            }

            try {

                const response = await fetch(
                    `/api/cemetery-location/${cemeteryId}/`
                );

                const data = await response.json();

                if (data.lat && data.lng) {

                    map.setView([data.lat, data.lng], 19);

                    if (!marker) {

                        marker = L.marker([data.lat, data.lng], {
                            draggable: true
                        }).addTo(map);

                        marker.on("dragend", function () {
                            updateInputs(marker.getLatLng());
                        });

                    } else {
                        marker.setLatLng([data.lat, data.lng]);
                    }

                    updateInputs({
                        lat: data.lat,
                        lng: data.lng
                    });
                }

            } catch (e) {
                console.log(e);
            }

        });
    }
});