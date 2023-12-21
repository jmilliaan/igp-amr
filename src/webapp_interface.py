import websocket
import threading
import time

class WebInterface:
    def __init__(self, url):
        self.ws = websocket.WebSocketApp(url,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True

    def on_open(self, ws):
        print("WebSocket opened")

    def on_message(self, ws, message):
        print("Received:", message)
        
    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### WebSocket closed ###")

    def start(self):
        self.thread.start()

    def stop(self):
        self.ws.close()

