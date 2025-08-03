import requests
from bs4 import BeautifulSoup
import random
import telebot
import re
import os

TOKEN = os.getenv("BOT_TOKEN", "SEU_TOKEN_AQUI")
CHAT_ID = os.getenv("CHAT_ID", "SEU_CHAT_ID_AQUI")
AFILIADO_LINK = os.getenv("AFILIADO_LINK", "https://amzn.to/4oqm0Uj")

bot = telebot.TeleBot(TOKEN)

CATEGORIAS = [
    "https://www.amazon.com.br/s?i=kitchen&rh=n%3A17849330011",
    "https://www.amazon.com.br/s?i=electronics&rh=n%3A16243862011"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def buscar_ofertas():
    url = random.choice(CATEGORIAS)
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    produtos = soup.select(".s-result-item")

    ofertas = []

    for produto in produtos:
        titulo_tag = produto.select_one("h2 .a-text-normal")
        preco_tag = produto.select_one(".a-price .a-offscreen")
        imagem_tag = produto.select_one(".s-image")
        link_tag = produto.select_one("h2 a")

        if titulo_tag and preco_tag and imagem_tag and link_tag:
            titulo = titulo_tag.text.strip()
            preco = preco_tag.text.strip()
            imagem = imagem_tag["src"]
            link = "https://www.amazon.com.br" + link_tag["href"].split("?")[0]
            link_afiliado = AFILIADO_LINK + "&tag=" + link.split("/dp/")[-1].split("/")[0]

            ofertas.append({
                "titulo": titulo,
                "preco": preco,
                "imagem": imagem,
                "link": link_afiliado
            })

        if len(ofertas) >= 1:
            break

    return ofertas

def enviar_para_telegram():
    ofertas = buscar_ofertas()

    for oferta in ofertas:
        legenda = f"📦 {oferta['titulo']}
💰 {oferta['preco']}
🔗 {oferta['link']}"

        try:
            img_response = requests.get(oferta['imagem'], stream=True)
            if img_response.status_code == 200:
                bot.send_photo(chat_id=CHAT_ID, photo=img_response.raw, caption=legenda)
            else:
                bot.send_message(chat_id=CHAT_ID, text=legenda)
        except Exception as e:
            print(f"[ERRO] Falha ao enviar para Telegram: {e}")