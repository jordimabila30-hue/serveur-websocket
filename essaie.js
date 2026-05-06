const http = require("http");
const { WebSocketServer } = require("ws");

const port = process.env.PORT || 3000;

const server = http.createServer((req, res) => {
  res.writeHead(200);
  res.end("WebSocket server alive");
});

const wss = new WebSocketServer({
  server,
  perMessageDeflate: false,
});

console.log("🚀 Server starting...");

// ========================
// 🧠 HEARTBEAT SYSTEM
// ========================
function heartbeat() {
  this.isAlive = true;
}

// ========================
// 🔌 CONNECTION
// ========================
wss.on("connection", (ws) => {
  console.log("🟢 Client connecté");

  ws.isAlive = true;
  ws.on("pong", heartbeat);

  // welcome message
  ws.send("SYSTEM: connected");

  ws.on("message", (data) => {
    const msg = data.toString().trim();

    if (!msg) return;
    if (msg === "PING") return;
    if (msg.startsWith("SYSTEM:")) return;

    console.log("📩 Reçu :", msg);

    // broadcast clean
    wss.clients.forEach((client) => {
      if (client.readyState === 1) {
        client.send(msg);
      }
    });
  });

  ws.on("close", () => {
    console.log("🔴 Client déconnecté");
  });

  ws.on("error", (err) => {
    console.log("⚠️ Erreur:", err.message);
  });
});

// ========================
// 🫀 KEEP ALIVE (IMPORTANT)
// ========================
const interval = setInterval(() => {
  wss.clients.forEach((ws) => {
    if (ws.isAlive === false) {
      console.log("💀 Client mort supprimé");
      return ws.terminate();
    }

    ws.isAlive = false;
    ws.ping(); // WebSocket natif ping (IMPORTANT)
  });
}, 30000);

// cleanup
wss.on("close", () => clearInterval(interval));

// ========================
// 🚀 START
// ========================
server.listen(port, "0.0.0.0", () => {
  console.log(`🌍 Server running on port ${port}`);
});