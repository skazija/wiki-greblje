document.addEventListener("DOMContentLoaded", function () {
    const latInput = document.getElementById("id_latitude");
    const lonInput = document.getElementById("id_longitude");

    if (!latInput || !lonInput || typeof L === "undefined") {
        return;
    }

    const maptilerKey = latInput.dataset.maptilerKey;

    if (!maptilerKey) {
        console.error("MapTiler API key nije pronađen.");
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

    function parseCoordinate(value) {
        return parseFloat(String(value).replace(",", "."));
    }

    let startLat = parseCoordinate(latInput.value);
    let startLon = parseCoordinate(lonInput.value);

    if (isNaN(startLat) || isNaN(startLon)) {
        startLat = 43.9889;
        startLon = 18.1781;
    }

    const map = L.map("custom-grave-map").setView([startLat, startLon], 18);
    const cemeterySelect = document.getElementById("id_cemetery");
    
    const streets = L.tileLayer(
        `https://api.maptiler.com/maps/streets-v4/256/{z}/{x}/{y}.png?key=${maptilerKey}`,
        {
            minZoom: 1,
            maxNativeZoom: 19,
            maxZoom: 22,
            attribution:
                '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> ' +
                '<a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap contributors</a>',
            crossOrigin: true,
            updateWhenIdle: true,
            keepBuffer: 0,
            detectRetina: false
        }
    );

    const satellite = L.tileLayer(
        "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        {
            maxNativeZoom: 19,
            maxZoom: 22,
            attribution: "Tiles © Esri",
            updateWhenIdle: true,
            keepBuffer: 0,
            detectRetina: false
        }
    );

    streets.addTo(map);

    L.control.layers({
        "Mapa": streets,
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

                const cemeteryLat = parseCoordinate(data.lat);
                const cemeteryLon = parseCoordinate(data.lng);

                if (
                    Number.isFinite(cemeteryLat) &&
                    Number.isFinite(cemeteryLon)
                ) {

                    const cemeteryPosition = L.latLng(
                        cemeteryLat,
                        cemeteryLon
                    );

                    map.setView(cemeteryPosition, 19, {
                        animate: false
                    });

                    if (!marker) {

                        marker = L.marker(cemeteryPosition, {
                            draggable: true
                        }).addTo(map);

                        marker.on("dragend", function () {
                            updateInputs(marker.getLatLng());
                        });

                    } else {
                        marker.setLatLng(cemeteryPosition);
                    }

                    updateInputs(cemeteryPosition);

                } else {
                    console.error(
                        "Neispravne koordinate groblja:",
                        data.lat,
                        data.lng
                    );
                }

            } catch (e) {
                console.log(e);
            }

        });
    }
});