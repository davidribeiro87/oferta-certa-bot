
import requests

def buscar_ofertas():
    return [{
        "titulo": "Fone Bluetooth Esportivo",
        "preco": "R$99,90",
        "link": "https://amzn.to/4oqm0Uj",
        "imagem": "https://m.media-amazon.com/images/I/61b6FfAEVZL._AC_SL1500_.jpg"
    }]

def enviar_para_telegram(bot, chat_id, oferta):
    legenda = f"📦 {oferta['titulo']}
💰 {oferta['preco']}
🔗 {oferta['link']}"
    try:
        bot.send_photo(chat_id=chat_id, photo=oferta['imagem'], caption=legenda)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
