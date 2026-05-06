import websocket
import threading
import uuid
import time

SERVER_URL = "wss://serveur-websocket-1.onrender.com"
CLIENT_ID = f"Client1-{uuid.uuid4().hex[:6]}"

stop_event = threading.Event()
ws_global = None  # 🔥 référence globale du socket


# ========================
# 🔁 CONNECT
# ========================
def connect():

    def on_message(ws, message):
        print(f"\n[{message}]\n[{CLIENT_ID}] > ", end="", flush=True)

    def on_error(ws, error):
        print(f"\n[{CLIENT_ID}] Erreur: {error}", flush=True)

    def on_close(ws, code, msg):
        global ws_global
        print(f"\n[{CLIENT_ID}] Déconnecté (reconnexion...)", flush=True)
        ws_global = None

        if not stop_event.is_set():
            time.sleep(2)
            start()

    def on_open(ws):
        global ws_global
        ws_global = ws
        print(f"[{CLIENT_ID}] Connecté au serveur", flush=True)
        ws.send(f"SYSTEM: {CLIENT_ID} connected")

    return websocket.WebSocketApp(
        SERVER_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )


# ========================
# ▶️ START
# ========================
def start():
    ws = connect()

    t = threading.Thread(
        target=lambda: ws.run_forever(
            ping_interval=20,
            ping_timeout=10
        ),
        daemon=True
    )
    t.start()

    input_loop()


# ========================
# ⌨️ SAFE INPUT LOOP
# ========================
def input_loop():
    global ws_global

    while not stop_event.is_set():
        try:
            msg = input(f"[{CLIENT_ID}] > ").strip()

            if msg.lower() in ("exit", "quit"):
                stop_event.set()
                if ws_global:
                    ws_global.close()
                break

            if not msg:
                continue

            # 🔥 IMPORTANT: vérifier connexion
            if ws_global and ws_global.sock and ws_global.sock.connected:
                ws_global.send(f"{CLIENT_ID}: {msg}")
            else:
                print("⚠️ Non connecté au serveur")

        except (KeyboardInterrupt, EOFError):
            stop_event.set()
            if ws_global:
                ws_global.close()
            break


# ========================
# 🚀 RUN
# ========================
if __name__ == "__main__":
    start()