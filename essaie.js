const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 3000 });

console.log("Serveur lancé sur le port 3000");

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