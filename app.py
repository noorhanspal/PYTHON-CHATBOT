# import os
# import gradio as gr
# from openai import OpenAI
# import tempfile
# import subprocess
# import re
# from dotenv import load_dotenv

# load_dotenv(override=True)

# # ============================
# # OpenAI Client
# # ============================

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# print("Loaded KEY:", os.getenv("OPENAI_API_KEY"))
# # ============================
# # Python Code Executor
# # ============================

# def run_python_code(code):
#     try:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as f:
#             f.write(code)
#             file_path = f.name

#         result = subprocess.run(
#             ["python", file_path],
#             capture_output=True,
#             text=True,
#             timeout=10
#         )

#         output = result.stdout if result.stdout else result.stderr

#         return output

#     except Exception as e:
#         return str(e)


# # ============================
# # Extract Python Code
# # ============================

# def extract_python_code(text):

#     pattern = r"```python(.*?)```"
#     matches = re.findall(pattern, text, re.DOTALL)

#     if matches:
#         return matches[0]

#     return None


# # ============================
# # Chat Streaming
# # ============================

# def chat_stream(user_input, history, model):

#     messages = [
#         {
#             "role": "system",
#             "content": """
# You are an expert Python teacher.

# Rules:
# - Answer programming questions clearly
# - Use markdown formatting
# - If code is required, wrap it inside ```python ```
# """
#         }
#     ]

#     messages.extend(history)

#     messages.append({"role": "user", "content": user_input})

#     stream = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=0.3,
#         stream=True
#     )

#     response = ""

#     for chunk in stream:
#         if chunk.choices[0].delta.content:
#             response += chunk.choices[0].delta.content
#             yield response


# # ============================
# # Text To Speech
# # ============================

# def text_to_speech(text):

#     speech_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")

#     with client.audio.speech.with_streaming_response.create(
#         model="gpt-4o-mini-tts",
#         voice="alloy",
#         input=text
#     ) as response:

#         response.stream_to_file(speech_file.name)

#     return speech_file.name


# # ============================
# # Handle Input
# # ============================

# def handle_input(text, audio, history, model):

#     history = history or []

#     # 🎤 Speech to text
#     if audio:
#         with open(audio, "rb") as f:
#             transcript = client.audio.transcriptions.create(
#                 model="gpt-4o-mini-transcribe",
#                 file=f
#             )
#         text = transcript.text

#     if not text:
#         yield history, history, None
#         return

#     # Add user message (NEW FORMAT)
#     history.append({"role": "user", "content": text})
#     yield history, history, None

#     bot_response = ""

#     for chunk in chat_stream(text, history, model):
#         bot_response = chunk

#         if len(history) > 0 and history[-1]["role"] == "assistant":
#             history[-1]["content"] = bot_response
#         else:
#             history.append({"role": "assistant", "content": bot_response})

#         yield history, history, None

#     # ============================
#     # Auto Python Code Execution
#     # ============================

#     code = extract_python_code(bot_response)

#     if code:
#         output = run_python_code(code)
#         bot_response += f"\n\n### 🧪 Code Output\n```\n{output}\n```"
#         history[-1]["content"] = bot_response
#         yield history, history, None

#     # ============================
#     # Text To Speech
#     # ============================

#     try:
#         audio_file = text_to_speech(bot_response)
#     except:
#         audio_file = None

#     yield history, history, audio_file


# # ============================
# # Gradio UI
# # ============================

# pink_theme = gr.themes.Soft(
#     primary_hue="pink",
#     secondary_hue="rose"
# )

# with gr.Blocks() as demo:

#     gr.Markdown("#  Python AI Chatbot")
#     gr.Markdown("Streaming + Voice + Python Code Execution")

#     model_dropdown = gr.Dropdown(
#         choices=["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
#         value="gpt-4o-mini",
#         label="Select Model"
#     )

#     chatbot = gr.Chatbot()

#     state = gr.State([])

#     with gr.Row():

#         txt = gr.Textbox(
#             placeholder="Ask Python question...",
#             scale=3
#         )

#         audio_input = gr.Audio(
#             sources=["microphone"],
#             type="filepath",
#             label="Speak"
#         )

#     send_btn = gr.Button("Send")

#     audio_output = gr.Audio(
#         label="Voice Response",
#         autoplay=True
#     )

#     send_btn.click(
#         handle_input,
#         inputs=[txt, audio_input, state, model_dropdown],
#         outputs=[chatbot, state, audio_output]
#     ).then(
#         lambda: "",
#         None,
#         txt
#     )

# demo.launch(theme=pink_theme)



import gradio as gr
from utils.chat import chat_stream
from utils.tools import run_python_code, extract_python_code
from utils.tts import text_to_speech
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ============================
# Handle Input
# ============================

def handle_input(text, audio, history, model):

    history = history or []

    # 🎤 Speech to text
    if audio:
        with open(audio, "rb") as f:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=f
            )
        text = transcript.text

    if not text:
        yield history, history, None
        return

    history.append({"role": "user", "content": text})
    yield history, history, None

    bot_response = ""

    for chunk in chat_stream(text, history, model):
        bot_response = chunk

        if len(history) > 0 and history[-1]["role"] == "assistant":
            history[-1]["content"] = bot_response
        else:
            history.append({"role": "assistant", "content": bot_response})

        yield history, history, None

    # Auto Python Execution
    code = extract_python_code(bot_response)

    if code:
        output = run_python_code(code)
        bot_response += f"\n\n### 🧪 Code Output\n```\n{output}\n```"
        history[-1]["content"] = bot_response
        yield history, history, None

    # Text to Speech
    try:
        audio_file = text_to_speech(bot_response)
    except:
        audio_file = None

    yield history, history, audio_file


# ============================
# UI
# ============================

pink_theme = gr.themes.Soft(
    primary_hue="pink",
    secondary_hue="rose"
)

with gr.Blocks() as demo:

    gr.Markdown("# Python AI Chatbot")
    gr.Markdown("Streaming + Voice + Python Code Execution")

    model_dropdown = gr.Dropdown(
        choices=["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
        value="gpt-4o-mini",
        label="Select Model"
    )

    chatbot = gr.Chatbot()
    state = gr.State([])

    with gr.Row():
        txt = gr.Textbox(placeholder="Ask Python question...", scale=3)
        audio_input = gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="Speak"
        )

    send_btn = gr.Button("Send")

    audio_output = gr.Audio(
        label="Voice Response",
        autoplay=True
    )

    send_btn.click(
        handle_input,
        inputs=[txt, audio_input, state, model_dropdown],
        outputs=[chatbot, state, audio_output]
    ).then(lambda: "", None, txt)

demo.launch(theme=pink_theme)