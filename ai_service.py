
import requests
import config

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def answer_question(user_message: str, faqs: list, history: list | None = None) -> str:
    """
    user_message: what the customer just sent
    faqs: list of {"question", "answer"} dicts from Google Sheets
    history: optional list of {"role": "user"/"assistant", "content": ...}
    """
    faq_text = "\n".join(f"Q: {f['question']}\nA: {f['answer']}" for f in faqs) or "(no FAQs added yet)"

    system_prompt = (
        f"You are the WhatsApp assistant for {config.BUSINESS_NAME}.\n"
        f"About the business: {config.BUSINESS_CONTEXT}\n\n"
        "Answer the customer's question using ONLY the FAQ list below whenever it's "
        "relevant. If the FAQ list doesn't cover it, answer briefly and helpfully, "
        "but if you're not sure, say you'll check and get back to them rather than "
        "guessing. Keep replies short (2-4 sentences) — this is a WhatsApp chat, not "
        "an email. Do not mention that you are an AI model.\n\n"
        f"FAQ list:\n{faq_text}"
    )

    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history[-6:])  # keep a little recent context, not the whole history
    messages.append({"role": "user", "content": user_message})

    response = requests.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {config.GROQ_API_KEY}"},
        json={"model": config.GROQ_MODEL, "messages": messages, "temperature": 0.4},
        timeout=20,
    )

    if response.status_code != 200:
        # Fail safe rather than crash the webhook — customer still gets a reply.
        print("Groq API error:", response.status_code, response.text)
        return (
            "Sorry, I'm having trouble finding that answer right now. "
            "A team member will follow up with you shortly."
        )

    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
