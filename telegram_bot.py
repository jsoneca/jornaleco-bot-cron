import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def main():
    mensagem = "⏰ Mensagem automática enviada pelo GitHub Actions!"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensagem}
    requests.post(url, data=payload)

if __name__ == "__main__":
    main()
