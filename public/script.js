const ws = new WebSocket('ws://192.168.29.219:8000');

ws.onopen = () => {
    console.log('WebSocket connected');
};

const buttonLabels = {
    1: 'Diag. Fwd L',
    2: 'Forward',
    3: 'Diag. Fwd R',
    4: 'Left',
    5: 'Stop',
    6: 'Right',
    7: 'Diag. Rev L',
    8: 'Reverse',
    9: 'Diag. Rev R'
};

const buttonGrid = document.querySelector('.button-grid');
const holdingInterval = 100;

for (let i = 1; i <= 9; i++) {
    const button = document.createElement('button');
    button.id = `btn${i}`;
    button.innerHTML = `<span class="btn-number">${i}</span><span class="btn-label">${buttonLabels[i]}</span>`;
    button.onmousedown = () => startSending(i);
    button.onmouseup = () => stopSending(i);
    button.onmouseleave = () => stopSending(i);
    button.ontouchstart = () => startSending(i);
    button.ontouchend = () => stopSending(i);
    buttonGrid.appendChild(button);
}

let interval;

function startSending(number) {
    stopSending(); // Ensure no other intervals are running
    interval = setInterval(() => {
        ws.send(`Button ${number} pressed`);
    }, holdingInterval); // Adjust the interval time as needed
}

function stopSending() {
    if (interval) {
        clearInterval(interval);
        interval = null;
    }
}
