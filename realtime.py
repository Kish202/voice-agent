import os
import openai
import asyncio

openai.api_key = os.getenv("OPENAI_API_KEY")

# -------------------------------
#  OPENAI REALTIME AUDIO SESSION
# -------------------------------
async def start_realtime_session(ws):
    ai = openai.realtime.RealtimeClient(
        model="gpt-4o-realtime"
    )

    await ai.connect()

    # Set AI Call Agent instructions
    await ai.send("session.update", {
        "session": {
            "instructions": """
                You are a polite AI phone agent.
                Keep responses short and natural.
                Speak clearly. Do not talk too fast.
            """
        }
    })

    # When AI sends audio → send to caller
    @ai.on("response.audio.delta")
    async def handle_audio(chunk):
        await ws.send(chunk)

    # Twilio audio → AI
    try:
        async for message in ws:
            await ai.send("input_audio_buffer.append", message)

    except:
        pass


    await ai.disconnect()
