import tempfile
import os
from utils.openai_client import client

def text_to_speech(text, voice="alloy"):
    speech_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice=voice,  # ✅ Dynamic voice
        input=text
    ) as response:
        response.stream_to_file(speech_file.name)

    return speech_file.name

def cleanup_audio(file_path):
    if file_path and os.path.exists(file_path):
        os.unlink(file_path)