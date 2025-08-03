
import requests
import random
import telebot
import os

# Configurações
TOKEN = os.getenv("TELEGRAM_TOKEN", "8356193016:AAHExuwPl5veXBoqazsgXvu7Bbqn9aKACcI")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1002808972406")
LINK_AFILIADO = "https://amzn.to/4oqm0Uj"

bot = telebot.TeleBot(TOKEN)

def buscar_ofertas():
    # Simula busca com 3 produtos reais genéricos
    produtos = [
        {
            "titulo": "Smart TV 50'' 4K UHD Samsung",
            "preco": "R$ 2.199,00",
            "imagem": "https://m.media-amazon.com/images/I/71wD3f-XnOL._AC_SL1500_.jpg",
            "link": LINK_AFILIADO
        },
        {
            "titulo": "Fritadeira Air Fryer Mondial 4L Preta",
            "preco": "R$ 349,90",
            "imagem": "https://m.media-amazon.com/images/I/81P1TKHQG3L._AC_SL1500_.jpg",
            "link": LINK_AFILIADO
        },
        {
            "titulo": "Echo Dot 5ª Geração com Relógio",
            "preco": "R$ 379,00",
            "imagem": "https://m.media-amazon.com/images/I/61d6vG+8GNL._AC_SL1500_.jpg",
            "link": LINK_AFILIADO
        },
    ]
    return random.sample(produtos, 1)

def enviar_para_telegram(oferta):
    legenda = f"📦 {oferta['titulo']}
💰 {oferta['preco']}
🔗 {oferta['link']}"
    bot.send_photo(CHAT_ID, oferta["imagem"], caption=legenda)
