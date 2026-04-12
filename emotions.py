import ollama

def detect_emotion(text):

    prompt = f"""
Detect the emotion of the following message.

Possible emotions:
sadness
anxiety
stress
anger
neutral

Message:
{text}

Reply with only the emotion word.
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    emotion = response["message"]["content"].strip().lower()

    return emotion