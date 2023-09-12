function toggleThrobber() {
    let throbberOverlay = document.getElementById("throbberOverlay");
    let throbberMsg = document.getElementById("throbberMessage");
    if (throbberOverlay.style.display != "") {
        throbberOverlay.style.display = "";
    }
    else
        throbberOverlay.style.display = "none";
    throbberMsg.innerHTML = "";
}

function pushAlert(message, type = "primary") {
    const alertPlace = document.getElementById("alertPlace");

    const alert = document.createElement("div");
    alert.setAttribute("class", `alert alert-${type} alert-dismissible`);
    alert.setAttribute("role", "alert");
    alert.textContent = message + " ";

    const dismissButton = document.createElement("button");
    dismissButton.setAttribute("type", "button");
    dismissButton.setAttribute("class", "btn-close");
    dismissButton.setAttribute("data-bs-dismiss", "alert");
    dismissButton.setAttribute("aria-label", "Close");

    alert.appendChild(dismissButton);
    alertPlace.appendChild(alert);
}

async function getAllCregs(cregs, changedSettings) {
    toggleThrobber();
    try {
        const response = await fetch("/api/cregs");
        const data = await response.json();
        if (data["status"] === "ok") {
            cregs = data["cregs"];
            renderCregs(cregs, changedSettings);
        }
        else {
            pushAlert("Something went wrong. Please refresh the app.", "danger");
        }

    } catch (error) {
        pushAlert("Something went wrong. Please refresh the app.", "danger");
    } finally {
        toggleThrobber()
    }
}

async function applyChanges(changedSettings, commitToFlash) {
    let toSend = { "changed": changedSettings, "commit_to_flash": commitToFlash };

    toggleThrobber();
    try {
        const response = await fetch("/api/cregschange", {
            method: "POST",
            mode: "same-origin",
            cache: "no-cache",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json"
            },
            redirect: "follow",
            referrerPolicy: "no-referrer",
            body: JSON.stringify(toSend),
        });

        const data = await response.json();
        if (data["status"] === "ok") {
            changedSettings = [];
            cregs = data["cregs"];
            renderCregs(cregs, changedSettings);
        }
        else {
            pushAlert("Something went wrong. Please refresh the app.", "danger");
        }

    } catch (error) {
        pushAlert("Something went wrong. Please refresh the app.", "danger");
    } finally {
        toggleThrobber()
    }
}

function setupApplyModal(changedSettings) {
    const applyButton = document.getElementById("applyButton");
    const applyForNowButton = document.getElementById("applyModalButtons").children[1];
    const applyCommitButton = document.getElementById("applyModalButtons").children[2];

    applyButton.onclick = () => {
        const applyModalMsg = document.getElementById("applyModalMsg");
        const applyModalMsgNothing = document.getElementById("applyModalMsgNothing");
        if (changedSettings.length == 0) {
            applyModalMsg.style.display = "none";
            applyModalMsgNothing.style.display = "";
            applyForNowButton.style.display = "none";
            applyCommitButton.style.display = "none";
        } else {
            applyModalMsg.style.display = "";
            applyModalMsgNothing.style.display = "none";
            applyForNowButton.style.display = "";
            applyCommitButton.style.display = "";

            const applyModalChanges = document.getElementById("applyModalChanges");
            applyModalChanges.innerHTML = "";
            changedSettings.forEach(chs => {
                const changeBullet = document.createElement("li");
                changeBullet.setAttribute("class", "list-group-item text-center");

                const badgeRegister = document.createElement("span");
                badgeRegister.setAttribute("class", "badge bg-secondary");
                badgeRegister.textContent = chs["register"];
                changeBullet.appendChild(badgeRegister);

                const divider = document.createElement("span");
                divider.textContent = " > ";
                changeBullet.appendChild(divider);

                const badgeField = badgeRegister.cloneNode();
                badgeField.textContent = chs["field"];
                changeBullet.appendChild(badgeField);

                changeBullet.appendChild(document.createElement("br"));

                const values = document.createElement("span");
                values.appendChild(document.createTextNode("from "));

                const fromValue = document.createElement("code");
                fromValue.textContent = chs["prevValue"];
                values.appendChild(fromValue);

                values.appendChild(document.createTextNode(" to "));

                const toValue = document.createElement("code");
                toValue.textContent = chs["value"];
                values.appendChild(toValue);

                changeBullet.appendChild(values);

                applyModalChanges.appendChild(changeBullet);
            });
        }
    };

    applyForNowButton.onclick = () => {
        applyChanges(changedSettings, false);
    };

    applyCommitButton.onclick = () => {
        applyChanges(changedSettings, true);
    };
}

function renderCregs(cregs, changedSettings) {
    const cregsBox = document.getElementById("cregsBox");
    cregsBox.innerHTML = "";
    cregs.forEach(register => {
        // Register heading
        const registerName = document.createElement("h3");

        const registerBadge = document.createElement("span");
        registerBadge.setAttribute("class", "badge bg-secondary");
        registerBadge.textContent = register["name"];

        registerName.appendChild(registerBadge);

        const registerGroup = document.createElement("ul");
        registerGroup.setAttribute("class", "list-group");

        register["fields"].forEach(field => {
            const accordion = document.createElement("div");
            accordion.setAttribute("class", "accordion accordion-item");

            const accordionHeader = document.createElement("h2");
            accordionHeader.setAttribute("class", "accordion-header");

            const accordionButton = document.createElement("button");
            accordionButton.setAttribute("class", "accordion-button collapsed");
            accordionButton.setAttribute("type", "button");
            accordionButton.setAttribute("data-bs-toggle", "collapse");
            accordionButton.setAttribute("data-bs-target", `#${field["name"]}`);
            accordionButton.textContent = field["name"];

            accordionHeader.appendChild(accordionButton);
            accordion.appendChild(accordionHeader);

            const accordionCollapse = document.createElement("div");
            accordionCollapse.setAttribute("class", "accordion-collapse collapse");
            accordionCollapse.setAttribute("id", field["name"]);

            const accordionBody = document.createElement("div");
            accordionBody.setAttribute("class", "accordion-body");

            const fieldDescription = document.createElement("p");
            fieldDescription.textContent = field["description"];
            accordionBody.appendChild(fieldDescription);

            const fieldDataType = document.createElement("p");
            const code = document.createElement("code");
            code.textContent = field["data_type"];
            fieldDataType.appendChild(code);
            accordionBody.appendChild(fieldDataType);

            let picker;
            let rangeLabel;
            if (field["enumerated_values"].length > 0) {
                picker = document.createElement("select");
                picker.setAttribute("class", "form-select");
                picker.setAttribute("autocomplete", "off");
                field["enumerated_values"].forEach(ev => {
                    const option = document.createElement("option");
                    option.setAttribute("value", ev["value"]);
                    option.textContent = ev["name"];
                    if (field["value"]["value"] === ev["value"])
                        option.selected = true;
                    picker.appendChild(option);
                });
            } else {
                picker = document.createElement("input");
                if (field["data_type"] == "uint8_t") {
                    rangeLabel = document.createElement("label");
                    const rangeID = `${field["name"]}Range`;
                    rangeLabel.setAttribute("class", "form-label");
                    rangeLabel.setAttribute("for", rangeID);
                    rangeLabel.textContent = field["value"]["value"];
                    accordionBody.appendChild(rangeLabel);

                    picker.setAttribute("type", "range");
                    picker.setAttribute("class", "form-range");
                    picker.setAttribute("id", rangeID);
                    picker.setAttribute("min", 0);
                    picker.setAttribute("max", 255);
                    picker.setAttribute("step", 1);
                    picker.setAttribute("value", field["value"]["value"]);
                } else {
                    picker.setAttribute("type", "number");
                    picker.setAttribute("class", "form-control");
                    picker.setAttribute("value", field["value"]["value"]);
                }
            }
            picker.onchange = () => {
                if (rangeLabel !== undefined)
                    rangeLabel.textContent = picker.value;

                let pickerValue;
                if (field["data_type"] == "float")
                    pickerValue = parseFloat(picker.value);
                else
                    pickerValue = parseInt(picker.value);

                for (let i = 0; i < changedSettings.length; i++) {
                    const chs = changedSettings[i];

                    if (chs["register"] == register["name"] && chs["field"] == field["name"]) {
                        if (pickerValue == field["value"]["value"]) {
                            changedSettings.splice(i, 1);
                        }
                        else
                            chs["value"] = pickerValue;
                        return;
                    }
                }

                if (pickerValue == field["value"]["value"])
                    return;

                changedSettings.push({
                    "register": register["name"],
                    "field": field["name"],
                    "value": pickerValue,
                    "prevValue": field["value"]["value"]
                });

            };
            accordionBody.appendChild(picker);

            accordionCollapse.appendChild(accordionBody);
            accordion.appendChild(accordionCollapse);

            registerGroup.appendChild(accordion);
        });
        cregsBox.appendChild(registerName);
        cregsBox.appendChild(registerGroup);
        cregsBox.appendChild(document.createElement("br"));
    });

    setupApplyModal(changedSettings);

    console.log("page updated");
}

// Main starts here
let changedSettings = [];
let cregs = []
getAllCregs(cregs, changedSettings);
