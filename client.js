const body = document.body;

const COLOR_OK = '#1f7f39';
const COLOR_ERROR = '#c43131';
const fileNames = ['gcal.png', 'screenshot.png'];

let active = false;
let currentView = 0;

const setMessage = (message, color) => {
    body.innerHTML = message;
    body.style.color = color;
};

const setBG = (fileName) => {
    const now = new Date().getTime();
    body.style.backgroundImage = `url("http://${window.location.hostname}:8080/${fileName}?${now}")`;
};

const cycleCurrentView = () => {
    currentView = (currentView + 1) % fileNames.length;
    setBG(fileNames[currentView]);
};

const startListener = () => {
    if (active) {
        return;
    }

    active = true;
    const socket = io(); // Initialize socket.io client

    socket.on('connect', () => {
        setMessage('Active', COLOR_OK);
    });

    socket.on('disconnect', (reason) => {
        setMessage(`Disconnected: ${reason}`, COLOR_ERROR);
        active = false;
    });

    socket.on('connect_error', (error) => {
        setMessage(`ERROR: ${error.message}`, COLOR_ERROR);
    });

    socket.on('message', (message) => {
        try {
            const data = JSON.parse(message);
            setMessage(data.msj, COLOR_OK);

            if (data.sc === 'bg') {
                if (data.msj === 'gcal.png' && fileNames[currentView] !== data.msj) {
                    return;
                }

                currentView = fileNames.indexOf(data.msj);
                setBG(fileNames[currentView]);
            }
        } catch (e) {
            setMessage(`MSG ERROR: ${e}`, COLOR_ERROR);
        }
    });
};

body.addEventListener('click', cycleCurrentView);

startListener();
