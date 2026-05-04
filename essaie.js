const WebSocket = require('ws');

const port = process.env.PORT || 3000;
const wss = new WebSocket.Server({ port });

console.log("Serveur lancé sur le port", port);

let clients = [];

wss.on('connection', function connection(ws) {
  console.log("Client connecté");

  clients.push(ws);

  ws.on('message', function message(data) {
    const msg = data.toString();
    console.log("Reçu :", msg);

    // envoyer à tous les autres clients
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