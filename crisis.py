CRISIS_WORDS = [
    "suicide",
    "kill myself",
    "end my life",
    "self harm",
    "i want to die",
    "i should die"
    "i should kill myself",
    "i want to go to sleep and never wake up",
    "i want to end it all",
    "i want to  give up",
]

def detect_crisis(text):
    text = text.lower()
    return any(word in text for word in CRISIS_WORDS)


def crisis_response():

    return """
I'm really sorry that you're feeling this overwhelmed right now.

When thoughts like harming yourself appear, it can feel incredibly heavy and isolating. 
You don't have to face this alone, even though it might feel that way right now.

If you can, please consider reaching out to someone who can support you in real life — 
a trusted friend, family member, or a mental health professional.

If you're able, you could also contact a crisis helpline in your country. 
They have trained people who genuinely want to listen and help you through this moment.

Right now, the most important thing is your safety.

If you're comfortable sharing, what happened today that made things feel this unbearable?
"""