import os
import tempfile
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def text_to_speech(text):

    speech_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    ) as response:

        response.stream_to_file(speech_file.name)

    return speech_file.name