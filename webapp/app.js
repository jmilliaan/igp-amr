const WebSocket = require('ws');
const express = require('express');
const http = require('http');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });
const port = 8000;

app.use(express.static('public'));

wss.on('connection', (ws) => {
    console.log('Client connected');

    ws.on('message', (message) => {
        const readMessage = message.toString();
        console.log('Received:', readMessage);
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

server.listen(port, () => {
    console.log(`Server running at http://192.168.29.219:${port}/`);
});
