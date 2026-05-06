import websocket
import threading
import uuid
import time

SERVER_URL = "ws://localhost:3000"
CLIENT_ID = f"Client1-{uuid.uuid4().hex[:6]}"

stop_event = threading.Event()

def on_message(ws, message):
    print(f"\n[{message}]\n[{CLIENT_ID}] > ", end="", flush=True)

def on_error(ws, error):
    print(f"\n[{CLIENT_ID}] Erreur: {error}", flush=True)

def on_close(ws, close_status_code, close_msg):
    print(f"\n[{CLIENT_ID}] Déconnecté", flush=True)
    stop_event.set()

def on_open(ws):
    print(f"[{CLIENT_ID}] Connecté au serveur", flush=True)

def receive_loop(ws):
    ws.run_forever(
        ping_interval=20,
        ping_timeout=10
    )

def main():
    ws = websocket.WebSocketApp(
        SERVER_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    t = threading.Thread(target=receive_loop, args=(ws,), daemon=True)
    t.start()

    # petit délai pour stabiliser la connexion
    time.sleep(1)

    while not stop_event.is_set():
        try:
            msg = input(f"[{CLIENT_ID}] > ").strip()

            if not msg:
                continue

            if msg.lower() in ("exit", "quit"):
                stop_event.set()
                ws.close()
                break

            ws.send(f"{CLIENT_ID}: {msg}")

        except (KeyboardInterrupt, EOFError):
            stop_event.set()
            ws.close()
            break

if __name__ == "__main__":
    main()