document.addEventListener("DOMContentLoaded", function () {

    const changelist = document.getElementById("changelist");
    const filter = document.getElementById("changelist-filter");

    if (!changelist || !filter) {
        return;
    }

    const formContainer =
        changelist.querySelector(".changelist-form-container") ||
        changelist.querySelector("#changelist-form");

    if (!formContainer) {
        return;
    }

    // Napravi sklopivi panel
    const panel = document.createElement("details");
    panel.className = "wg-changelist-filter-panel";

    // Ako je neki filter aktivan, panel ostavi otvoren.
    const params = new URLSearchParams(window.location.search);

    const ignoredParams = new Set([
        "q",
        "p",
        "o",
        "ot",
        "all"
    ]);

    let hasActiveFilter = false;

    for (const key of params.keys()) {
        if (!ignoredParams.has(key)) {
            hasActiveFilter = true;
            break;
        }
    }

    if (hasActiveFilter) {
        panel.open = true;
    }

    const summary = document.createElement("summary");
    summary.className = "wg-changelist-filter-summary";
    summary.innerHTML = `
        <span class="wg-filter-title">
            <span class="wg-filter-icon">⌕</span>
            Filteri
        </span>
        <span class="wg-filter-toggle"></span>
    `;

    panel.appendChild(summary);

    const body = document.createElement("div");
    body.className = "wg-changelist-filter-body";

    // Premjesti originalni Django filter.
    body.appendChild(filter);
    panel.appendChild(body);

    // Filter ide iznad search/action/tabele.
    changelist.insertBefore(panel, formContainer);
});