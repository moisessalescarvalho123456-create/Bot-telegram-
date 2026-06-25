import os
import json
import hmac
import hashlib
import requests
from flask import Flask, request, jsonify
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Suas credenciais (configure no Render como variáveis de ambiente)
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
APP_SECRET = os.environ.get("APP_SECRET")

# Histórico de conversa por usuário (em memória)
conversation_history = {}

SYSTEM_PROMPT = """Você é uma assistente virtual simpática que representa uma mulher chamada Ana.
Você responde mensagens no Facebook de forma carinhosa, divertida e levemente flertando para manter a conversa fluindo.

Regras importantes:
- Seja sempre simpática, alegre e use emojis com moderação 😊
- Flerte de forma sutil e educada, nunca vulgar
- Faça perguntas para manter a conversa (sobre hobbies, cidade, o que gosta de fazer)
- Demonstre interesse genuíno na pessoa
- Use linguagem natural e informal, como se fosse uma conversa real
- Nunca revele que é um bot ou IA
- Se a pessoa perguntar se é robô, desvie com humor
- Mensagens curtas e naturais, como no Messenger mesmo
"""

def verify_signature(payload, signature):
    if not APP_SECRET:
        return True
    expected = "sha256=" + hmac.new(
        APP_SECRET.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v18.0/me/messages"
    headers = {"Content-Type": "application/json"}
    params = {"access_token": PAGE_ACCESS_TOKEN}
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    return response.json()

def get_ai_response(user_id, user_message):
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({
        "role": "user",
        "content": user_message
    })

    # Mantém apenas as últimas 10 mensagens para não estourar contexto
    history = conversation_history[user_id][-10:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        max_tokens=300,
        temperature=0.85
    )

    assistant_message = response.choices[0].message.content

    conversation_history[user_id].append({
        "role": "assistant",
        "content": assistant_message
    })

    return assistant_message

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verificado com sucesso!")
        return challenge, 200
    return "Token inválido", 403

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    signature = request.headers.get("X-Hub-Signature-256", "")
    if not verify_signature(request.data, signature):
        return "Assinatura inválida", 403

    data = request.get_json()

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]

                if "message" in event and "text" in event["message"]:
                    user_text = event["message"]["text"]
                    print(f"Mensagem de {sender_id}: {user_text}")

                    ai_response = get_ai_response(sender_id, user_text)
                    send_message(sender_id, ai_response)

    return jsonify({"status": "ok"}), 200

@app.route("/", methods=["GET"])
def home():
    return "Bot está online! 🚀", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
