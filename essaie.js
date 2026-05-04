const WebSocket = require('ws');
const http = require('http');

const port = process.env.PORT || 3000;

// créer serveur HTTP
const server = http.createServer();

// attacher WebSocket dessus
const wss = new WebSocket.Server({ server });

server.listen(port, () => {
  console.log("Serveur lancé sur le port", port);
});

let clients = [];

wss.on('connection', (ws) => {
  console.log("Client connecté");

  clients.push(ws);

  ws.on('message', (data) => {
    const msg = data.toString();
    console.log("Reçu :", msg);

    clients.forEach(client => {
      if (client !== ws && client.readyState === WebSocket.OPEN) {
        client.send(msg);
      }
    });
  });

  ws.on('close', () => {
    clients = clients.filter(c => c !== ws);
  });
});