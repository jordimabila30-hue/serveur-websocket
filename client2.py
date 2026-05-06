import websocket
import threading
import time
import uuid

SERVER_URL = "wss://serveur-websocket-1.onrender.com"
CLIENT_ID = f"RECEIVER-{uuid.uuid4().hex[:6]}"

stop_event = threading.Event()


# ========================
# 📡 EVENTS
# ========================
def on_message(ws, message):
    print(f"\n📩 MESSAGE REÇU → {message}")


def on_error(ws, error):
    print(f"\n❌ ERREUR → {error}")


def on_close(ws, code, msg):
    print("\n🔌 Déconnecté (reconnexion...)")


def on_open(ws):
    print(f"\n🟢 {CLIENT_ID} connecté et en écoute temps réel")
    ws.send(f"SYSTEM: {CLIENT_ID} listener online")


# ========================
# 🔁 RUN + RECONNECT
# ========================
def run():

    while not stop_event.is_set():
        try:
            ws = websocket.WebSocketApp(
                SERVER_URL,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )

            ws.run_forever(
                ping_interval=20,
                ping_timeout=10
            )

        except Exception as e:
            print("⚠️ Reconnexion après erreur:", e)
            time.sleep(2)


# ========================
# 🚀 START
# ========================
if __name__ == "__main__":
    run()