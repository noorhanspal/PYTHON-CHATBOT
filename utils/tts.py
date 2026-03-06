# #import os
# import tempfile
# #from openai import OpenAI
# #from dotenv import load_dotenv
# from utils.openai_client import client

# # load_dotenv(override=True)

# # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def text_to_speech(text):

#     speech_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

#     with client.audio.speech.with_streaming_response.create(
#         model="gpt-4o-mini-tts",
#         voice="alloy",
#         input=text
#     ) as response:

#         response.stream_to_file(speech_file.name)

#     return speech_file.name


import tempfile
import os
from utils.openai_client import client

def text_to_speech(text):
    speech_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    ) as response:
        response.stream_to_file(speech_file.name)

    return speech_file.name

def cleanup_audio(file_path):
    if file_path and os.path.exists(file_path):
        os.unlink(file_path)