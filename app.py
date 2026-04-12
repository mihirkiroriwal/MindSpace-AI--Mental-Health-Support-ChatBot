import streamlit as st
import ollama
import random
from gtts import gTTS
import tempfile

from prompts import SYSTEM_PROMPT
from crisis import detect_crisis, crisis_response
from emotions import detect_emotion
from questions import FOLLOW_UP_QUESTIONS


def speak(text):
    tts = gTTS(text=text, lang="en")

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)

    return temp_file.name


st.set_page_config(page_title="Mental Health AI")
st.title("🧠 Mental Health Support Chat")
st.caption("A safe place to talk when things feel overwhelming.")
st.divider()


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

if "audio_file" not in st.session_state:
    st.session_state.audio_file = None


MAX_HISTORY = 10

def get_recent_messages():
    return st.session_state.messages[-MAX_HISTORY:]


for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])


user_input = st.chat_input("How are you feeling today?")


if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    st.chat_message("user").write(user_input)

    if detect_crisis(user_input):
        ai_reply = crisis_response()

    else:
        emotion = detect_emotion(user_input)

        emotion_prompt = {
            "role": "system",
            "content": f"""
User emotion: {emotion}
User message: "{user_input}"

Respond naturally, emotionally, and specifically.
Do not repeat patterns.
Mirror user language.
"""
        }

        try:
            with st.spinner("🤖 Thinking..."):

                response = ollama.chat(
                    model="llama3",
                    messages=get_recent_messages() + [emotion_prompt],
                    options={
                        "temperature": 0.85,
                        "top_p": 0.9,
                        "num_predict": 500
                    }
                )

                ai_reply = response["message"]["content"].strip()

                lines = ai_reply.split("\n")
                clean_lines = []
                for line in lines:
                    if line not in clean_lines:
                        clean_lines.append(line)
                ai_reply = "\n".join(clean_lines)

                if "?" not in ai_reply and len(ai_reply) > 80:
                    ai_reply += "\n\n" + random.choice(FOLLOW_UP_QUESTIONS)

        except Exception as e:
            ai_reply = "I'm having trouble responding right now."
            st.error(e)

    assistant_container = st.chat_message("assistant")
    assistant_container.write(ai_reply)

    if st.button("🔊 Play Voice", key=f"voice_{len(st.session_state.messages)}"):
        st.session_state.audio_file = speak(ai_reply)

    if st.session_state.audio_file:
        with open(st.session_state.audio_file, "rb") as f:
            audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")

    st.session_state.messages.append(
        {"role": "assistant", "content": ai_reply}
    )