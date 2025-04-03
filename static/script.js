function atualizarMensagens() {
    fetch('/mensagens')
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                let ultimaMensagem = data[data.length - 1]; // Pega a última mensagem
                atualizarBussola(ultimaMensagem);
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
    let angulo = angulos[direcao] || 0;
    document.getElementById('ponteiro').style.transform = `translate(-50%, -100%) rotate(${angulo}deg)`;
}

function resetarBussola() {
    document.getElementById('ponteiro').style.transform = `translate(-50%, -100%) rotate(0deg)`;
}

function mostrarSeção(selecao) {
    document.getElementById('compass-container').style.display = 'none';
    document.getElementById('logs-container').style.display = 'none';

    document.getElementById(selecao).style.display = 'block';
}

function atualizarLogs() {
    fetch('/logs')
        .then(response => response.json())
        .then(data => {
            let logsDiv = document.getElementById('logs');
            logsDiv.innerHTML = '';
            data.forEach(log => {
                let p = document.createElement('p');
                p.textContent = log;
                logsDiv.appendChild(p);
            });
        });
}

setInterval(atualizarMensagens, 2000); // Atualiza a bússola a cada 2s
setInterval(atualizarLogs, 2000); // Atualiza os logs a cada 2s
