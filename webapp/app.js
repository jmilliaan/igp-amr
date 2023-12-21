import WebSocket from 'ws';

const wss = new WebSocket.Server({port : 8000});

wss.on('connection', (ws) => {
    // Handle incoming messages from the client
    ws.on('message', (message) => {
      // Process the message
      console.log('Received message:', message);
      ws.send('Message received!');
    });
  
    // Handle client disconnection
    ws.on('close', () => {
      console.log('Client disconnected');
    });
  });

  wss.on('error', (error) => {
    console.error('WebSocket server error:', error);
  });

wss.on('listening', () => {
    console.log('WebSocket server listening on port 8000');
  });
  
