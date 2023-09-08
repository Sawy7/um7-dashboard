function getAllCregs() {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "/api/cregs", false);
    try {
        xmlHttp.send(null);
    } catch (error) {
        return false;
    }

    return JSON.parse(xmlHttp.responseText);
}

function renderCregs(cregs, changedSettings) {
    const cregsBox = document.getElementById("cregsBox");
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
                    "value": pickerValue
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

    const applyButton = document.getElementById("applyButton");
    applyButton.style.display = "";
    applyButton.onclick = () => {
        const applyModalMsg = document.getElementById("applyModalMsg");
        const applyModalMsgNothing = document.getElementById("applyModalMsgNothing");
        const modalButtons = document.getElementById("applyModalButtons");
        if (changedSettings.length == 0) {
            applyModalMsg.style.display = "none";
            applyModalMsgNothing.style.display = "";
            modalButtons.children[1].style.display = "none";
            modalButtons.children[2].style.display = "none";
        } else {
            applyModalMsg.style.display = "";
            applyModalMsgNothing.style.display = "none";
            modalButtons.children[1].style.display = "";
            modalButtons.children[2].style.display = "";
        }
    };

    const loadingSpinner = document.getElementById("loadingSpinner");
    loadingSpinner.style = "display: none;";
}

let cregs = getAllCregs();
let changedSettings = [];

if (cregs === false)
    console.log("API error");
else {
    renderCregs(cregs, changedSettings);
}