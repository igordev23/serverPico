function atualizarMensagens() {
    fetch('/mensagens')
        .then(response => response.json())
        .then(data => {
            const mensagensDiv = document.getElementById('mensagens');
            mensagensDiv.innerHTML = '';

            if (data.length > 0) {
                data.forEach(msg => {
                    const div = document.createElement('div');
                    div.className = 'mensagem';
                    div.textContent = msg;
                    mensagensDiv.appendChild(div);
                });
            } else {
                mensagensDiv.innerHTML = '<p>Nenhuma mensagem recebida ainda.</p>';
            }
        });
}

function resetarMensagens() {
    fetch('/reset', { method: 'POST' })
        .then(() => atualizarMensagens());
}

function mostrarSeção(selecao) {
    const seções = ['logs-container', 'map-container'];
    seções.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.add('hidden');
    });

    const ativa = document.getElementById(selecao);
    if (ativa) ativa.classList.remove('hidden');
}

function mostrarMapa() {
    mostrarSeção('map-container');
    if (!window.mapInicializado) {
        initMap();
        window.mapInicializado = true;
    }
}

async function getGPSData() {
    try {
        const response = await fetch("/gps");
        const data = await response.json();

        const lat = parseFloat(data.latitude);
        const lng = parseFloat(data.longitude);

        if (!isNaN(lat) && !isNaN(lng) && lat !== 0 && lng !== 0) {
            return { lat, lng };
        }
    } catch (error) {
        console.error("Erro ao buscar dados GPS:", error);
    }
    return null;
}

let map, marker;

async function initMap() {
    let location = null;
    while (!location) {
        location = await getGPSData();
        if (!location) await new Promise(resolve => setTimeout(resolve, 1000));
    }

    map = new google.maps.Map(document.getElementById("map"), {
        center: location,
        zoom: 17,
    });

    marker = new google.maps.Marker({
        position: location,
        map,
        title: "Localização Atual",
    });

    setInterval(async () => {
        const newLocation = await getGPSData();
        if (newLocation) {
            marker.setPosition(newLocation);
            map.setCenter(newLocation);
        }
    }, 3000);
}

// Atualiza os logs automaticamente
setInterval(atualizarMensagens, 2000);
