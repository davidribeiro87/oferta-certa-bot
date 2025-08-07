import requests
import telebot

TOKEN = "COLOQUE_SEU_TOKEN_AQUI"
CHAT_ID = "COLOQUE_SEU_CHAT_ID_AQUI"
LINK_AFILIADO = "https://amzn.to/40MEvrL"
ID_RASTREAMENTO = "davidribeiro8-20"

bot = telebot.TeleBot(TOKEN)

def buscar_ofertas():
    # Simulação de lista de produtos (em produção, seria uma API ou scraping)
    return [
        {
            "titulo": "Echo Dot (5ª Geração)",
            "preco": "R$ 279,00",
            "imagem": "https://m.media-amazon.com/images/I/61lEQr9bm-L._AC_SX679_.jpg",
            "link": "https://www.amazon.com.br/dp/B09SVXLMVZ"
        }
    ]

def enviar_para_telegram(oferta):
    legenda = (
        f"📦 {oferta['titulo']}
"
        f"💰 {oferta['preco']}
"
        f"🔗 Compre aqui: {LINK_AFILIADO}?tag={ID_RASTREAMENTO}"
    )
    bot.send_photo(chat_id=CHAT_ID, photo=oferta["imagem"], caption=legenda)