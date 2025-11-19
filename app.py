import os
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
import asyncio
import websockets
from realtime import start_realtime_session  # your GPT session handler

load_dotenv()

app = Flask(__name__)

# ---------------------
#  HOMEPAGE
# ---------------------
@app.route("/")
def home():
    return "The Voice agent Server Running!"

# ---------------------
#  TWILIO CALL WEBHOOK
# ---------------------
@app.route("/incoming-call", methods=["POST"])
def incoming_call():
    response = VoiceResponse()
    connect = response.connect()

    # Replace this with your ngrok WS URL
    connect.stream(url="wss://prognathous-phytologically-takako.ngrok-free.dev/call-stream")

    return Response(str(response), mimetype="text/xml")


# ------------------------------------------------
#  WEBSOCKET SERVER (Twilio <-> OpenAI Realtime)
# ------------------------------------------------
async def websocket_handler(websocket):
    print("📞 Twilio stream connected")
    try:
        await start_realtime_session(websocket)
    except Exception as e:
        print("❌ Error:", e)
    finally:
        print("📴 Twilio disconnected")


async def start_ws():
    print("🔄 WebSocket server running on :8765/call-stream")
    async with websockets.serve(websocket_handler, "0.0.0.0", 8765):
        await asyncio.Future()  # keep running


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_ws())

    # Use threaded=True to prevent blocking
    app.run(host="0.0.0.0", port=3000, threaded=True)

