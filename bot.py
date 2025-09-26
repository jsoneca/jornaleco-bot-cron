#!/usr/bin/env python3
# bot.py
import os
import requests
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
COUNTRY = os.getenv("COUNTRY", "br")
MAX_ARTICLES = int(os.getenv("MAX_ARTICLES", "5"))

if not (BOT_TOKEN and CHAT_ID and NEWS_API_KEY):
    logging.error("Faltando BOT_TOKEN, CHAT_ID ou NEWS_API_KEY")
    raise SystemExit(1)

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def get_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {"apiKey": NEWS_API_KEY, "country": COUNTRY, "pageSize": MAX_ARTICLES}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    return data.get("articles", [])

def escape_html(s: str) -> str:
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def format_message(articles):
    header = f"📢 Notícias — {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
    parts = []
    for a in articles:
        title = escape_html(a.get("title") or "—")
        src = escape_html(a.get("source", {}).get("name") or "")
        url = a.get("url") or ""
        published = a.get("publishedAt") or ""
        parts.append(f"📰 <b>{title}</b>\n{src} • {published}\n🔗 {url}")
    return header + "\n\n".join(parts)

def send_message(text):
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    r = requests.post(f"{TELEGRAM_API}/sendMessage", json=payload, timeout=15)
    r.raise_for_status()
    return r.json()

def main():
    try:
        articles = get_news()
        if not articles:
            logging.info("Nenhuma notícia encontrada.")
            return
        msg = format_message(articles)
        send_message(msg)
        logging.info("Notícias enviadas com sucesso.")
    except Exception:
        logging.exception("Erro ao buscar/enviar notícias")

if __name__ == "__main__":
    main()
