import requests
from telegram import Bot
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
CHAT_ID = os.getenv("CHAT_ID")  # seu chat_id ou grupo do telegram

bot = Bot(token=TELEGRAM_TOKEN)

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=br&apiKey={NEWSAPI_KEY}"
    response = requests.get(url).json()
    
    if response["status"] == "ok":
        articles = response["articles"][:5]
        news_list = []
        for art in articles:
            title = art["title"]
            url = art["url"]
            news_list.append(f"📰 {title}\n🔗 {url}")
        return "\n\n".join(news_list)
    else:
        return "Erro ao buscar notícias."

def main():
    news_text = get_news()
    bot.send_message(chat_id=CHAT_ID, text=news_text)

if __name__ == "__main__":
    main()
