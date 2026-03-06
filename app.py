import re
import json
from utils.openai_client import client
import gradio as gr
from utils.chat import chat_stream
from utils.tools import run_python_code, extract_python_code
from utils.tts import text_to_speech, cleanup_audio


def save_history(history):
    with open("chat_history.json", "w") as f:
        json.dump(history, f)


def load_history():
    try:
        with open("chat_history.json", "r") as f:
            return json.load(f)
    except:
        return []


def clean_for_tts(text):
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"[#*`]", "", text)
    return text.strip()


def handle_input(text, audio, history, model, voice):

    text = text.strip() if text else ""
    history = history or []

    if not text and not audio:
        yield history, history, None
        return

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

    try:
        for chunk in chat_stream(text, history, model):
            bot_response = chunk

            if len(history) > 0 and history[-1]["role"] == "assistant":
                history[-1]["content"] = bot_response
            else:
                history.append({"role": "assistant", "content": bot_response})

            yield history, history, None

    except Exception as e:
        history.append({"role": "assistant", "content": f"❌ Error: {str(e)}"})
        yield history, history, None
        return

    # Auto Python Execution
    code = extract_python_code(bot_response)

    if code:
        output = run_python_code(code)
        display_response = bot_response + f"\n\n### 🧪 Code Output\n```\n{output}\n```"
        history[-1]["content"] = display_response
        yield history, history, None

    # Text to Speech
    audio_file = None

    try:
        clean_text = clean_for_tts(bot_response)
        audio_file = text_to_speech(clean_text, voice)

    except Exception as e:
        print(f"TTS Error: {e}")
        audio_file = None

    save_history(history)
    yield history, history, audio_file


pink_theme = gr.themes.Soft(
    primary_hue="pink",
    secondary_hue="rose"
)

with gr.Blocks() as demo:

    gr.Markdown("# 🤖 Python AI Chatbot")
    gr.Markdown("Streaming + Voice + Python Code Execution")

    model_dropdown = gr.Dropdown(
        choices=["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
        value="gpt-4o-mini",
        label="Select Model"
    )

    voice_dropdown = gr.Dropdown(
        choices=["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
        value="alloy",
        label="🎙️ Voice"
    )

    chatbot = gr.Chatbot()
    state = gr.State(load_history())

    with gr.Row():

        txt = gr.Textbox(
            placeholder="Ask Python question...",
            scale=3
        )

        audio_input = gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="Speak"
        )

    send_btn = gr.Button("Send")
    clear_btn = gr.Button("🗑️ Clear Chat")

    audio_output = gr.Audio(
        label="Voice Response",
        autoplay=True
    )

    send_btn.click(
        handle_input,
        inputs=[txt, audio_input, state, model_dropdown, voice_dropdown],
        outputs=[chatbot, state, audio_output]
    ).then(lambda: "", None, txt)

    txt.submit(
        handle_input,
        inputs=[txt, audio_input, state, model_dropdown, voice_dropdown],
        outputs=[chatbot, state, audio_output]
    ).then(lambda: "", None, txt)

    clear_btn.click(
        lambda: ([], [], None),
        None,
        [chatbot, state, audio_output]
    )

demo.launch(theme=pink_theme)