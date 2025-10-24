import json
import time
from datetime import datetime

from colorama import init as colorama_init, Fore, Style
from websocket import WebSocketApp

WEBSOCKET_URL = "wss://pumpportal.fun/api/data"

colorama_init(autoreset=True)

def choose_indicator(mcap_sol: float):
    if mcap_sol >= 100:
        return "HIGH ALERT", (Style.BRIGHT + Fore.RED)
    elif mcap_sol > 30:
        return "TRUSTED", Fore.MAGENTA
    else:
        return "SUSPECT", Fore.BLUE


def handle_message(raw: str):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Silently ignore malformed frames (matches Go's 'continue' on parse error)
        return

    # Expect fields: name, marketCapSol, initialBuy (initialBuy not used)
    name = data.get("name")
    mcap = data.get("marketCapSol")

    if name is None or mcap is None:
        return  # schema mismatch; ignore

    # Only print if > 1 SOL market cap
    try:
        mcap_val = float(mcap)
    except (TypeError, ValueError):
        return

    if mcap_val <= 1:
        return

    label, color_prefix = choose_indicator(mcap_val)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"{label} | Token: {name} | MarketCap: {mcap_val:.2f} SOL | {timestamp}"
    print(f"{color_prefix}{line}{Style.RESET_ALL}")


def on_open(ws: WebSocketApp):
    # Send subscription payload once connected
    payload = {"method": "subscribeNewToken"}
    ws.send(json.dumps(payload))
    print("Connected and subscription message sent.")


def on_message(ws: WebSocketApp, message: str):
    handle_message(message)


def on_error(ws: WebSocketApp, error):
    # Log the error; reconnect handled in outer loop
    print(f"[ws error] {error}")


def on_close(ws: WebSocketApp, status_code, msg):
    print(f"WebSocket closed (code={status_code}, msg={msg}).")


def run_forever_with_reconnect():
    # Simple reconnect loop with backoff ceiling
    backoff = 5
    while True:
        try:
            ws = WebSocketApp(
                WEBSOCKET_URL,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
            )
            # run_forever blocks until closed or error
            ws.run_forever(ping_interval=25, ping_timeout=10)
        except KeyboardInterrupt:
            print("Interrupted by user. Exiting.")
            return
        except Exception as e:
            print(f"[fatal] {e}")

        # Backoff before reconnect
        print(f"Reconnecting in {backoff} seconds...")
        time.sleep(backoff)
        # cap the backoff so it doesn’t grow unbounded
        backoff = min(backoff * 2, 60)


if __name__ == "__main__":
    print("Connecting to WebSocket…")
    run_forever_with_reconnect()
