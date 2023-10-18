from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VERIFY_TOKEN = "mySuperSecretToken123456"
PAGE_ACCESS_TOKEN = "EAADb9yUPZC5sBO6gIgWRdP6N0bUi80ZBYRIrzUSkdHGhEImitVDs3uEYYZCrmfpitjV0Sq1wuPf1qWsjitzeZCy7xKJvcwo62Y7qHpRgdHvYBAKG3hDUpAViDXJkGdZC3rtmlizmR3C2kdFTcsMFU5Bxm8P4x6wOyc3FinYdnBR2SdDMuM8yfInsgZCKRU2MpH"

@app.route("/", methods=['GET'])
def ping():
    return "hello world"

@app.route("/webhook", methods=['GET'])
def verify_webhook():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    else:
        return "Invalid verification token", 403


@app.route("/webhook", methods=['POST'])
def handle_messages():
    data = request.json
    if data["object"] == "page":
        for entry in data["entry"]:
            for message_event in entry["messaging"]:
                sender_id = message_event["sender"]["id"]
                if "message" in message_event:
                    handle_text_message(sender_id, message_event["message"]["text"])
    return "OK", 200


def handle_text_message(sender_id, message_text):
    # Here you can process the message, determine the response, and send it back.
    # For simplicity, we're just echoing the received message.
    send_text_message(sender_id, message_text)


def send_text_message(recipient_id, message_text):
    import requests

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }

    response = requests.post(
        f"https://graph.facebook.com/v13.0/me/messages?access_token={PAGE_ACCESS_TOKEN}",
        headers=headers,
        json=data
    )

    return response.json()


if __name__ == "__main__":
    app.run(debug=True)