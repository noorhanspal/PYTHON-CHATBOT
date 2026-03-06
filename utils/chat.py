from utils.openai_client import client

def chat_stream(user_input, history, model):

    messages = [
        {
            "role": "system",
            "content": """
You are an expert Python teacher.

Rules:
- Answer programming questions clearly
- Use markdown formatting
- If code is required, wrap it inside ```python ```
"""
        }
    ]

    messages.extend(history)
    messages.append({"role": "user", "content": user_input})

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
        stream=True
    )

    response = ""

    for chunk in stream:
        delta = chunk.choices[0].delta

        if delta and delta.content:
            response += delta.content
            yield response