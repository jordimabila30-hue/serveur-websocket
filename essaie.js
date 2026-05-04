const WebSocket = require('ws');
const http = require('http');

const port = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  res.writeHead(200);
  res.end("WebSocket server running");
});

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
    console.log("Client déconnecté");
    clients = clients.filter(c => c !== ws);
  });

  ws.on('error', (err) => {
    console.log("Erreur socket:", err);
  });
});