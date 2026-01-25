const API_URL = "/generate";

let map;
let marker;

document.addEventListener("DOMContentLoaded", () => {
    initApp();
});

function initApp() {
    // Set default date
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    document.getElementById("datetime").value = now.toISOString().slice(0, 16);

    // Initialize Map
    initMap();

    // Event Listeners
    document.getElementById("skyForm").addEventListener("submit", handleGenerate);
    document.getElementById("downloadBtn").addEventListener("click", downloadImage);
    document.getElementById("downloadPdfBtn").addEventListener("click", downloadPDF);
    document.getElementById("searchBtn").addEventListener("click", searchLocation);
    document.getElementById("locationSearch").addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            searchLocation();
        }
    });

    // Initial canvas draw
    drawPlaceholder();
}

function initMap() {
    // Default: Merida, Mexico (as per user's prompt examples) or 0,0
    const startLat = 20.689;
    const startLon = -88.201;

    // Create map instance
    map = L.map('mapContainer').setView([startLat, startLon], 10);

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    // Add draggable marker
    marker = L.marker([startLat, startLon], { draggable: true }).addTo(map);

    // Sync inputs on drag
    marker.on('dragend', function (e) {
        const coord = marker.getLatLng();
        updateInputs(coord.lat, coord.lng);
    });

    // Map click -> Move marker
    map.on('click', function (e) {
        marker.setLatLng(e.latlng);
        updateInputs(e.latlng.lat, e.latlng.lng);
    });

    // Initial input sync
    updateInputs(startLat, startLon);
}

function updateInputs(lat, lon) {
    document.getElementById('lat').value = lat.toFixed(4);
    document.getElementById('lon').value = lon.toFixed(4);
}

async function searchLocation() {
    const query = document.getElementById("locationSearch").value;
    if (!query) return;

    const btn = document.getElementById("searchBtn");
    const originalText = btn.textContent;
    btn.textContent = "⏳";
    btn.disabled = true;

    try {
        const response = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`);
        const data = await response.json();

        if (data && data.length > 0) {
            const lat = parseFloat(data[0].lat);
            const lon = parseFloat(data[0].lon);

            map.setView([lat, lon], 12);
            marker.setLatLng([lat, lon]);
            updateInputs(lat, lon);
        } else {
            alert("Ubicación no encontrada");
        }
    } catch (err) {
        console.error("Error searching location:", err);
        alert("Error al buscar la ubicación");
    } finally {
        btn.textContent = originalText;
        btn.disabled = false;
    }
}

function drawPlaceholder() {
    const canvas = document.getElementById("skyCanvas");
    const ctx = canvas.getContext("2d");

    // Fill background
    ctx.fillStyle = "#0b0d17";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw circle frame
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2 - 100; // Shift up for text
    const radius = 500;

    ctx.strokeStyle = "rgba(255,255,255,0.2)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    ctx.stroke();

    ctx.fillStyle = "rgba(255,255,255,0.5)";
    ctx.font = "30px Inter";
    ctx.textAlign = "center";
    ctx.fillText("Configura tu mapa para ver las estrellas", centerX, centerY);
}

async function handleGenerate(e) {
    e.preventDefault();

    const datetime = document.getElementById("datetime").value;
    const lat = parseFloat(document.getElementById("lat").value);
    const lon = parseFloat(document.getElementById("lon").value);
    const recipient = document.getElementById("recipient").value;
    const message = document.getElementById("message").value;

    const loading = document.getElementById("loadingOverlay");
    const downloadBtn = document.getElementById("downloadBtn");
    const downloadPdfBtn = document.getElementById("downloadPdfBtn");
    const statusMsg = document.getElementById("statusMsg");

    loading.classList.remove("hidden");
    statusMsg.textContent = "Conectando con el universo...";
    downloadBtn.disabled = true;
    downloadPdfBtn.disabled = true;

    try {
        let data;
        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    lat,
                    lon,
                    datetime_utc: new Date(datetime).toISOString().replace('T', ' ').slice(0, 19) // Format YYYY-MM-DD HH:MM:SS
                })
            });

            if (!response.ok) throw new Error("Backend not reachable");
            data = await response.json();

        } catch (err) {
            console.warn("Backend API failed, using mock data for demo:", err);
            statusMsg.textContent = "Modo Demo (Backend no detectado)";
            await new Promise(r => setTimeout(r, 1000)); // Fake delay
            data = generateMockData();
        }

        drawMap(data, recipient, message);
        downloadBtn.disabled = false;
        downloadPdfBtn.disabled = false;
        if (statusMsg.textContent !== "Modo Demo (Backend no detectado)") {
            statusMsg.textContent = "Mapa generado con éxito.";
        }

    } catch (error) {
        console.error(error);
        statusMsg.textContent = "Error al generar el mapa.";
    } finally {
        loading.classList.add("hidden");
    }
}

function drawMap(data, recipient, message) {
    const canvas = document.getElementById("skyCanvas");
    const ctx = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;

    const centerX = width / 2;
    const centerY = height / 2 - 100;
    const radius = 500;

    // 1. Background
    ctx.fillStyle = "#0b0d17";
    ctx.fillRect(0, 0, width, height);

    // 2. DecorFrame
    ctx.save();
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
    ctx.fillStyle = "#111b29";
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = "#ffffff";
    ctx.stroke();
    ctx.clip();

    // 3. Grid
    drawGrid(ctx, centerX, centerY, radius);

    // 4. Stars
    if (data.stars) {
        data.stars.forEach(star => {
            const { x, y } = altAzToXY(star.alt_deg, star.az_deg, centerX, centerY, radius);
            const size = Math.max(0.5, (6 - star.magnitude) * 0.6);

            ctx.fillStyle = "#ffffff";
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();
        });
    }

    // 5. Constellations
    if (data.constellations) {
        ctx.strokeStyle = "rgba(255, 255, 255, 0.3)";
        ctx.lineWidth = 1;

        data.constellations.forEach(constellation => {
            constellation.lines.forEach(line => {
                ctx.beginPath();
                let first = true;
                line.forEach(pt => {
                    const { x, y } = altAzToXY(pt.alt, pt.az, centerX, centerY, radius);
                    if (first) {
                        ctx.moveTo(x, y);
                        first = false;
                    } else {
                        ctx.lineTo(x, y);
                    }
                });
                ctx.stroke();
            });

            // Draw Name
            if (constellation.centroid && constellation.centroid.visible) {
                const { x, y } = altAzToXY(constellation.centroid.alt, constellation.centroid.az, centerX, centerY, radius);
                // Only draw if within reasonable bounds (sometimes centroid is low but constellation is high)
                // But we have visible flag.

                ctx.fillStyle = "rgba(255, 255, 255, 0.6)";
                ctx.font = "10px Inter";
                ctx.textAlign = "center";
                ctx.fillText(constellation.name.toUpperCase(), x, y);
            }
        });
    }

    // 6. Solar System
    if (data.solar_system) {
        data.solar_system.forEach(obj => {
            const { x, y } = altAzToXY(obj.alt_deg, obj.az_deg, centerX, centerY, radius);

            let color = "#ddd";
            let size = 5;

            if (obj.name === "Sun") { color = "#FFD700"; size = 10; }
            else if (obj.name === "Moon") { color = "#F4F6F0"; size = 8; }
            else if (obj.name === "Mars") { color = "#ff6b6b"; size = 6; }

            ctx.fillStyle = color;
            ctx.beginPath();
            ctx.arc(x, y, size, 0, Math.PI * 2);
            ctx.fill();

            // Label
            ctx.fillStyle = "#fff";
            ctx.font = "12px Inter";
            ctx.fillText(obj.name, x + 8, y + 4);
        });
    }

    ctx.restore();

    // Compass Marks
    drawCompassLabels(ctx, centerX, centerY, radius);

    // 7. Text Overlay
    ctx.fillStyle = "#ffffff";
    ctx.textAlign = "center";

    if (recipient) {
        ctx.font = "italic 40px 'Playfair Display'";
        ctx.fillText(recipient, centerX, 100);
    }
    // Message (Bottom)
    if (message) {
        ctx.font = "30px 'Playfair Display'";
        // Split precisely into lines of max 60 chars
        wrapText(ctx, message, centerX, height - 260, 1000, 40, 60);
    }

    // Date/Location Stamp
    ctx.font = "16px Inter";
    ctx.fillStyle = "rgba(255,255,255,0.6)";
    const dateStr = new Date(document.getElementById("datetime").value).toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
    const locStr = `${parseFloat(document.getElementById("lat").value).toFixed(2)}° N, ${parseFloat(document.getElementById("lon").value).toFixed(2)}° W`;
    ctx.fillText(`${dateStr.toUpperCase()} | ${locStr}`, centerX, height - 160);

    // Watermark
    ctx.font = "12px Inter";
    ctx.fillStyle = "rgba(255,255,255,0.3)";
    ctx.fillText("© 2026 Starlight Project", centerX, height - 80);
}

function altAzToXY(alt, az, cx, cy, radius) {
    const r = radius * (1 - alt / 90);
    const theta = (az - 90) * (Math.PI / 180);
    const x = cx + r * Math.cos(theta);
    const y = cy + r * Math.sin(theta);
    return { x, y };
}

function drawGrid(ctx, cx, cy, r) {
    ctx.strokeStyle = "rgba(255,255,255,0.1)";
    ctx.lineWidth = 1;
    ctx.beginPath(); ctx.arc(cx, cy, r * 0.33, 0, Math.PI * 2); ctx.stroke();
    ctx.beginPath(); ctx.arc(cx, cy, r * 0.66, 0, Math.PI * 2); ctx.stroke();
    for (let i = 0; i < 360; i += 45) {
        const rad = i * Math.PI / 180;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + r * Math.cos(rad), cy + r * Math.sin(rad));
        ctx.stroke();
    }
}

function drawCompassLabels(ctx, cx, cy, r) {
    ctx.fillStyle = "#fff";
    ctx.font = "bold 20px Inter";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    const offset = 25;
    ctx.fillText("N", cx, cy - r - offset);
    ctx.fillText("S", cx, cy + r + offset);
    ctx.fillText("E", cx + r + offset, cy);
    ctx.fillText("O", cx - r - offset, cy);
}

function wrapText(ctx, text, x, y, maxWidth, lineHeight, maxCharsPerLine = 0) {
    // If strict char limit
    if (maxCharsPerLine > 0) {
        const words = text.split(' ');
        let lines = [];
        let currentLine = words[0];

        for (let i = 1; i < words.length; i++) {
            if (currentLine.length + 1 + words[i].length <= maxCharsPerLine) {
                currentLine += " " + words[i];
            } else {
                lines.push(currentLine);
                currentLine = words[i];
            }
        }
        lines.push(currentLine);

        // Limit to 2 lines if desired, or just print them all
        // User asked for "60 and 60", so 2 lines max ideally
        const maxLines = 2;
        // Start Y adjustment to center vertically if we wanted, but we place manual Y

        lines.slice(0, maxLines).forEach((l, i) => {
            ctx.fillText(l, x, y + (i * lineHeight));
        });
        return;
    }

    // Default fit to width logic
    const words = text.split(' ');
    let line = '';
    for (let n = 0; n < words.length; n++) {
        const testLine = line + words[n] + ' ';
        const metrics = ctx.measureText(testLine);
        const testWidth = metrics.width;
        if (testWidth > maxWidth && n > 0) {
            ctx.fillText(line, x, y);
            line = words[n] + ' ';
            y += lineHeight;
        } else {
            line = testLine;
        }
    }
    ctx.fillText(line, x, y);
}

function downloadImage() {
    const canvas = document.getElementById("skyCanvas");
    const link = document.createElement("a");
    link.download = "starlight-map.png";
    link.href = canvas.toDataURL("image/png");
    link.click();
}

function downloadPDF() {
    const { jsPDF } = window.jspdf;
    const canvas = document.getElementById("skyCanvas");
    const imgData = canvas.toDataURL("image/jpeg", 0.9); // JPEG slightly smaller

    // Letter format: 215.9 x 279.4 mm
    const pdf = new jsPDF({
        orientation: "portrait",
        unit: "mm",
        format: "letter"
    });

    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = pdf.internal.pageSize.getHeight();

    // Add image full page (or nicely centered)
    pdf.addImage(imgData, 'JPEG', 0, 0, pdfWidth, pdfHeight);
    pdf.save("starlight-map.pdf");
}

function generateMockData() {
    const stars = [];
    for (let i = 0; i < 300; i++) {
        stars.push({
            alt_deg: Math.random() * 90,
            az_deg: Math.random() * 360,
            magnitude: Math.random() * 6
        });
    }
    return {
        stars,
        solar_system: [
            { name: "Moon", alt_deg: 45, az_deg: 180, type: "moon" },
            { name: "Jupiter", alt_deg: 60, az_deg: 120, type: "planet" }
        ],
        constellations: []
    };
}

