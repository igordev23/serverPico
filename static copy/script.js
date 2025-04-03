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


function resetarMensagens() {
    fetch('/reset', { method: 'POST' })
        .then(() => {
            atualizarMensagens();
            resetarBussola();
        });
}


setInterval(atualizarMensagens, 2000); // Atualiza a cada 2 segundos
