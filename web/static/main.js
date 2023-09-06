function createChart(name, type, datasetNames, charts) {
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
}

function processUM7Messages(event) {
    let packet = JSON.parse(event.data);
    let chart;

    switch (packet["packet_type"]) {
        case "UM7AllProcPacket":
            chart = charts["Acceleration"];
            chart.data.labels.push(packet["accel_proc_time"]);
            chart.data.datasets[0].data.push(packet["accel_proc_x"]);
            chart.data.datasets[1].data.push(packet["accel_proc_y"]);
            chart.data.datasets[2].data.push(packet["accel_proc_z"]);

            if (chart.data.datasets[0].data.length > 50) {
                chart.data.labels.shift();
                chart.data.datasets.forEach((dataset) => {
                    dataset.data.shift();
                });
                chart.update("none");
            } else {
                chart.update();
            }
            break;
        case "UM7HealthPacket":
            chart = charts["GPS Stats"];
            chart.data.labels.shift();
            chart.data.datasets.forEach((dataset) => {
                dataset.data.shift();
            });

            chart.data.labels.push("");
            chart.data.datasets[0].data.push(packet["sats_in_view"]);
            chart.data.datasets[1].data.push(packet["sats_used"]);

            chart.update("none");
            break;
        case "UM7GPSPacket":
            // chart = charts["GPS"];
            // chart.data.labels.push(packet["gps_time"]);
            // chart.data.datasets[0].data.push(packet["gps_latitude"]);
            // chart.data.datasets[1].data.push(packet["gps_longitude"]);
            // chart.data.datasets[2].data.push(packet["gps_altitude"]);

            // if (chart.data.datasets[0].data.length > 50) {
            //     chart.data.labels.shift();
            //     chart.data.datasets.forEach((dataset) => {
            //         dataset.data.shift();
            //     });
            //     chart.update("none");
            // } else {
            //     chart.update();
            // }
            break;
        default:
            console.log("Error: Unknown packet type")
            // console.log(packet)
            break;
    }
}

// Start Websocket communication
let ws = new WebSocket(`ws://localhost:8000/ws`);

// Chart storage
let charts = {};

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
    charts
);
    // GPS Stats
createChart(
    "GPS Stats",
    "bar",
    [
        "Satelites in view",
        "Satelites used"
    ],
    charts
);
//     // GPS
// createChart(
//     "GPS",
//     [
//         "Latitude",
//         "Longitude",
//         "Altitude"
//     ],
//     charts
// );

// Process incoming messages
ws.onmessage = processUM7Messages;

// let logBox = document.getElementById("logBox");
// ws.onmessage = (event) => {
//     // let newMsg = document.createElement("div");
//     // newMsg.setAttribute("class", "alert alert-primary");
//     // newMsg.innerHTML = event.data;

//     // logBox.prepend(newMsg);

//     // setTimeout(function () {
//     //     let bootAlert = new bootstrap.Alert(newMsg);
//     //     bootAlert.close();
//     // }, 10000);

//     umMessage = JSON.parse(event.data);
//     console.log(umMessage);

//     myChart.data.labels.push("yoo");
//     myChart.data.datasets.forEach((dataset) => {
//         dataset.data.push(1);
//     });
//     myChart.update();
// };
