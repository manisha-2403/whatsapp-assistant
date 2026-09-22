
from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import bot_logic

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def receive_message():
    incoming_text = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "")  # e.g. "whatsapp:+919999999999"
    phone = from_number.replace("whatsapp:", "")

    if phone and incoming_text:
        reply_text = bot_logic.handle_message(phone, incoming_text)
    else:
        reply_text = "Sorry, I didn't catch that — could you send it again?"

    twiml = MessagingResponse()
    twiml.message(reply_text)
    return Response(str(twiml), mimetype="text/xml")


if __name__ == "__main__":
    app.run(port=5000, debug=True)
