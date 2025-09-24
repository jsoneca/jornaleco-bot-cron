import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 🔑 Tokens
TELEGRAM_TOKEN = "SEU_TOKEN_DO_TELEGRAM"
NEWSAPI_KEY = "SUA_CHAVE_NEWSAPI"

# Função para buscar notícias
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=br&apiKey={NEWSAPI_KEY}"
    response = requests.get(url).json()
    
    if response["status"] == "ok":
        articles = response["articles"][:5]  # pega só 5 notícias
        news_list = []
        for art in articles:
            title = art["title"]
            url = art["url"]
            news_list.append(f"📰 {title}\n🔗 {url}")
        return "\n\n".join(news_list)
    else:
        return "Erro ao buscar notícias."

# Comando /news
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    news_text = get_news()
    await update.message.reply_text(news_text)

# Início do bot
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("news", news))
    app.run_polling()

if __name__ == "__main__":
    main()
