const PORT = 8080;
const https = require('https');
const fs = require('fs');
const rateLimit = require('express-rate-limit');
const socketIO = require('socket.io'); // Import socket.io
const filewatcher = require('filewatcher');

const server = https.createServer((request, response) => {
    let url = request.url;

    if (url.indexOf('?') > 0)
        url = url.substring(0, url.indexOf('?'));

    console.log('URL: ' + url);

    if (!fs.existsSync('.' + url)) {
        console.log('ERROR: NOT FOUND: ' + url);
        return;
    }

    switch (url) {
        case '/':
        case '/index.html':
            response.setHeader('Content-Type', 'text/html; charset=UTF-8');
            fs.createReadStream('index.html').pipe(response);
            break;
        case '/client.js':
            response.setHeader('Content-Type', 'application/javascript');
            fs.createReadStream('client.js').pipe(response);
            break;
        case '/gcal.png':
            response.setHeader('Content-Type', 'image/png');
            fs.createReadStream('gcal.png').pipe(response);
            break;
        case '/screenshot.png':
            response.setHeader('Content-Type', 'image/png');
            fs.createReadStream('screenshot.png').pipe(response);
            break;
        default:
            response.status(404).end();
            break;
    }
});

const io = socketIO(server); // Initialize socket.io

const sendMessage = (scope, message) => {
    const json = JSON.stringify({ msj: message, sc: scope });
    io.emit('message', json); // Use socket.io to emit messages
    console.log('message sent: ' + json);
};

server.on('error', error => {
    if (error.code === 'EADDRINUSE')
        console.log('ERROR: Port already in use');
    else
        console.log(error);
});

server.on('request', () => {
    console.log('New request');
});

// Start watching directory..
const watcher = filewatcher();
const watchFiles = ['./screenshot.png', './gcal.png'];
for (const url of watchFiles) {
    if (!fs.existsSync(url)) {
        console.log(url, 'NOT FOUND, creating... ');
        fs.closeSync(fs.openSync(url, 'w'));
    }
    watcher.add(url);
}

let last = Date.now();

watcher.on('change', (filename, stat) => {
    if (stat.blocks < 1 || stat.size < 1) return;
    const now = Date.now();
    if (now - last < 1000) return; // file watcher flood protection
    console.log('onChange:', filename, stat);
    sendMessage('bg', filename.substring(2));
    last = now;
});

server.listen(PORT, () => {
    console.log('Listening on port ' + PORT);
});
