from utils.openai_client import client
from utils.prompts import SYSTEM_PROMPT

def chat_stream(user_input, history, model):

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_input})

    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.3,
        stream=True,
        stream_options={"include_usage": True}  # ✅ Token tracking
    )

    response = ""

    for chunk in stream:
        # ✅ Token info print karo
        if chunk.usage:
            tokens = chunk.usage.total_tokens
            cost = tokens * 0.000001
            cost_inr = cost * 84  # 1 USD = 84 INR
            print(f"📊 Tokens used: {tokens} | Approx cost: ₹{cost_inr:.4f}")

        # ✅ Pehle check karo choices empty toh nahi
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta
        if delta and delta.content:
            response += delta.content
            yield response