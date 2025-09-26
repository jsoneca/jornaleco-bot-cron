import requests
import telegram
import os
from datetime import datetime

# Configurações
BOT_TOKEN = os.getenv("BOT_TOKEN")  # coloque no GitHub Secrets
CHAT_ID = os.getenv("CHAT_ID")      # ID do grupo ou canal
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=br&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    articles = data.get("articles", [])
    noticias = []
    for art in articles[:5]:  # pega só as 5 primeiras
        titulo = art["title"]
        link = art["url"]
        noticias.append(f"📰 {titulo}\n🔗 {link}")
    return "\n\n".join(noticias)

def send_news():
    bot = telegram.Bot(token=BOT_TOKEN)
    noticias = get_news()
    if noticias:
        hoje = datetime.now().strftime("%d/%m/%Y %H:%M")
        mensagem = f"📢 Notícias - {hoje}\n\n{noticias}"
        bot.send_message(chat_id=CHAT_ID, text=mensagem)

if __name__ == "__main__":
    send_news()
