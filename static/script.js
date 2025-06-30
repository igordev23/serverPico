function atualizarMensagens() {
    fetch('/mensagens')
        .then(response => response.json())
        .then(data => {
            let mensagensDiv = document.getElementById('mensagens');
            mensagensDiv.innerHTML = '';

            if (data.length > 0) {
                data.forEach(msg => {
                    let div = document.createElement('div');
                    div.className = 'mensagem';
                    div.textContent = msg;
                    mensagensDiv.appendChild(div);
                });

                // Atualiza a bússola com a última mensagem recebida
                let ultimaMensagem = data[data.length - 1];
                atualizarBussola(ultimaMensagem);
            } else {
                mensagensDiv.innerHTML = '<p>Nenhuma mensagem recebida ainda.</p>';
            }
        });
}

function atualizarBussola(direcao) {
    let angulos = {
        "Norte": 0,
        "Nordeste": 45,
        "Leste": 90,
        "Sudeste": 135,
        "Sul": 180,
        "Sudoeste": 225,
        "Oeste": 270,
        "Noroeste": 315
    };
    
    // Apenas atualiza a bússola se a direção recebida for válida
    if (angulos.hasOwnProperty(direcao)) {
        let angulo = angulos[direcao];
        document.getElementById('ponteiro').style.transform = `translate(-50%, -100%) rotate(${angulo}deg)`;
    }
}

function resetarBussola() {
    document.getElementById('ponteiro').style.transform = `translate(-50%, -100%) rotate(0deg)`;
}

function resetarMensagens() {
    fetch('/reset', { method: 'POST' })
        .then(() => atualizarMensagens());
}

function mostrarSeção(selecao) {
    document.getElementById('compass-container').style.display = 'none';
    document.getElementById('logs-container').style.display = 'none';

    document.getElementById(selecao).style.display = 'block';
}
function mostrarMapa() {
    document.getElementById('map-container').style.display = 'block';
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
        if (!location) await new Promise(r => setTimeout(r, 1000));
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

setInterval(atualizarMensagens, 2000); // Atualiza os logs a cada 2s
