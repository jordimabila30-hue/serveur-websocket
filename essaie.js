const WebSocket = require('ws');
const http = require('http');

const port = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end("Server is running");
});

const wss = new WebSocket.Server({ server });

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
    console.log("Client déconnecté");
    clients = clients.filter(c => c !== ws);
  });

  ws.on('error', (err) => {
    console.log("Erreur socket:", err);
  });
});

server.listen(port, '0.0.0.0', () => {
  console.log("Serveur lancé sur le port", port);
});