const WebSocket = require('ws');
const express = require('express');
const http = require('http');
const path = require('path'); // Add this line to use the path module

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });
const port = 8000;

app.use(express.static('public'));

// New route for the root URL
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

wss.on('connection', (ws) => {
    console.log('Client connected');

    ws.on('message', (message) => {
        const readMessage = message.toString();
        console.log(readMessage);
        wss.clients.forEach(client => {
            if (client !== ws && client.readyState === WebSocket.OPEN) {
                client.send(readMessage);
            }
        });
    });

    ws.on('close', () => {
        console.log('Client disconnected');
    });
});

server.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});
