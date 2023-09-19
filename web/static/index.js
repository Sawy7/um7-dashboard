function createChart(name, type, datasetNames, charts, times) {
    // Define viable plot colors
    const plotColors = ["#ff2700", "#00d353", "#007bff"];

    // Find plotBox
    const plotBox = document.getElementById("plotBox");

    // Create heading
    const plotHeading = document.createElement("h2");
    plotHeading.innerHTML = name;
    plotBox.appendChild(plotHeading);

    // Create canvas
    const ctx = document.createElement("canvas");
    ctx.setAttribute("class", "my-4 w-100");
    ctx.setAttribute("width", "900");
    ctx.setAttribute("height", "380");
    plotBox.appendChild(ctx);

    // Prepare datasets
    let datasets = [];
    for (let i = 0; i < datasetNames.length; i++) {
        datasets.push({
            label: datasetNames[i],
            data: [],
            lineTension: 0,
            backgroundColor: plotColors[i],
            borderColor: plotColors[i],
            pointBackgroundColor: plotColors[i]
        });
    }

    const chartElement = new Chart(ctx, {
        type: type,
        data: {
            datasets: datasets
        },
        options: {
            plugins: {
                legend: {
                    labels: {
                        usePointStyle: true
                    }
                },
                tooltip: {
                    boxPadding: 3
                }
            }
        }
    });

    charts[name] = chartElement;
    times[name] = 0;
}

function processUM7Messages(event) {
    let packet = JSON.parse(event.data);

    switch (packet["packet_type"]) {
        case "UM7AllProcPacket":
            // Acceleration
            const accelerationChart = charts["Acceleration"];
            accelerationChart.data.labels.push(times["Acceleration"]);
            accelerationChart.data.datasets[0].data.push(packet["accel_proc_x"]);
            accelerationChart.data.datasets[1].data.push(packet["accel_proc_y"]);
            accelerationChart.data.datasets[2].data.push(packet["accel_proc_z"]);

            // Gyroscope
            const gyroChart = charts["Gyroscope"];
            gyroChart.data.labels.push(times["Acceleration"]);
            gyroChart.data.datasets[0].data.push(packet["gyro_proc_x"]);
            gyroChart.data.datasets[1].data.push(packet["gyro_proc_y"]);
            gyroChart.data.datasets[2].data.push(packet["gyro_proc_z"]);

            // Magnetometer
            const magChart = charts["Magnetometer"];
            magChart.data.labels.push(times["Acceleration"]);
            magChart.data.datasets[0].data.push(packet["mag_proc_x"]);
            magChart.data.datasets[1].data.push(packet["mag_proc_y"]);
            magChart.data.datasets[2].data.push(packet["mag_proc_z"]);

            times["Acceleration"]++;

            if (accelerationChart.data.datasets[0].data.length > 50) {
                // Remove label
                accelerationChart.data.labels.shift();
                gyroChart.data.labels.shift();
                magChart.data.labels.shift();

                // Remove value
                accelerationChart.data.datasets.forEach((dataset) => {
                    dataset.data.shift();
                });
                gyroChart.data.datasets.forEach((dataset) => {
                    dataset.data.shift();
                });
                magChart.data.datasets.forEach((dataset) => {
                    dataset.data.shift();
                });
            }

            // Refresh chart
            accelerationChart.update("none");
            gyroChart.update("none");
            magChart.update("none");

            break;
        case "UM7HealthPacket":
            const gpsStatsChart = charts["GPS Stats"];
            gpsStatsChart.data.labels.shift();
            gpsStatsChart.data.datasets.forEach((dataset) => {
                dataset.data.shift();
            });

            gpsStatsChart.data.labels.push("");
            gpsStatsChart.data.datasets[0].data.push(packet["sats_in_view"]);
            gpsStatsChart.data.datasets[1].data.push(packet["sats_used"]);

            gpsStatsChart.update("none");
            break;
        case "UM7GPSPacket":
            // Do nothing
            console.log(packet["gps_time"], packet["gps_speed"]);
            break;
        case "UM7VelocityPacket":
            const velocityChart = charts["Velocity"];
            velocityChart.data.labels.push(times["Velocity"]);
            velocityChart.data.datasets[0].data.push(packet["velocity_north"]);
            velocityChart.data.datasets[1].data.push(packet["velocity_east"]);
            velocityChart.data.datasets[2].data.push(packet["velocity_up"]);

            times["Velocity"]++;

            if (velocityChart.data.datasets[0].data.length > 50) {
                // Remove label
                velocityChart.data.labels.shift();

                // Remove value
                velocityChart.data.datasets.forEach((dataset) => {
                    dataset.data.shift();
                });
            }

            // Refresh chart
            velocityChart.update("none");

            break;
        default:
            console.log("Error: Unknown packet type");
            // console.log(packet);
            break;
    }
}

async function getRequest(url) {
    try {
        const response = await fetch(url);
        return response.json();
    } catch (error) {
        pushAlert("Something went wrong. Please refresh the app.", "danger");
    }
}

async function postRequest(url, data) {
    try {
        const response = await fetch(url, {
            method: "POST",
            mode: "same-origin",
            cache: "no-cache",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json"
            },
            redirect: "follow",
            referrerPolicy: "no-referrer",
            body: JSON.stringify(data),
        });
        return response.json();
    } catch (error) {
        pushAlert("Something went wrong. Please refresh the app.", "danger");
    }
}

function toggleCaptureButton(newState) {
    if (newState) {
        captureButton.setAttribute("class", "btn btn-sm btn-danger");
        captureButton.children[1].textContent = "Capturing";
    } else {
        captureButton.setAttribute("class", "btn btn-sm btn-outline-secondary");
        captureButton.children[1].textContent = "Capture";
    }
}

async function getInitialCaptureState() {
    const response = await getRequest("/api/iscapturing");
    captureState = response["status"];
    toggleCaptureButton(captureState);
    captureButton.disabled = false;
}

// Start Websocket communication
let ws = new WebSocket(`ws://${location.host}/ws`);

// Chart storage
let charts = {};
let times = {};

// Create charts
    // Acceleration
createChart(
    "Acceleration",
    "line",
    [
        "Acceleration X",
        "Acceleration Y",
        "Acceleration Z"
    ],
    charts, times
);
    // Gyroscope
createChart(
    "Gyroscope",
    "line",
    [
        "Gyroscope X",
        "Gyroscope Y",
        "Gyroscope Z"
    ],
    charts, times
);
    // Magnetometer
createChart(
    "Magnetometer",
    "line",
    [
        "Magnetometer X",
        "Magnetometer Y",
        "Magnetometer Z"
    ],
    charts, times
);
    // Velocity
createChart(
    "Velocity",
    "line",
    [
        "Velocity North",
        "Velocity East",
        "Velocity Up"
    ],
    charts, times
)
    // GPS Stats
createChart(
    "GPS Stats",
    "bar",
    [
        "Satelites in view",
        "Satelites used"
    ],
    charts, times
);

// Process incoming messages
ws.onmessage = processUM7Messages;

// Capture
let captureState = false;
const captureButton = document.getElementById("captureButton");
getInitialCaptureState();

captureButton.onclick = async () => {
    if (!captureState)
       await postRequest("/api/startcapture", {"timestamp": Math.floor((new Date()).getTime()/1000)});
    else
       await getRequest("/api/stopcapture");
    captureState = !captureState;
    toggleCaptureButton(captureState);
};
