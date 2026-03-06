# 🤖 Python AI Chatbot

A streaming AI chatbot built with OpenAI API and Gradio UI.

## Features

- Real-time streaming responses
- Voice input (Speech-to-Text)
- Voice output (Text-to-Speech)
- Auto Python code execution
- Dangerous code execution blocked
- Token and cost tracking (INR)
- Multiple voice selection
- Chat history saved locally
- Multiple model selection

## Setup

1. Clone the repo
2. Create a virtual environment
3. Install requirements
```
   pip install -r requirements.txt
```
4. Copy `.env.example` to `.env` and add your API key
```
   OPENAI_API_KEY=your_key_here
```
5. Run the app
```
   python app.py
```

## Important

- Never share your `.env` file
- `chat_history.json` is saved locally on your machine
- Dangerous code is automatically blocked before execution

## Models Supported

- gpt-4o-mini
- gpt-4o
- gpt-4.1-mini

## Voices Supported

- alloy, echo, fable, onyx, nova, shimmer