import requests

def buscar_ofertas():
    return [
        {
            'titulo': 'Smart TV 50” 4K UHD Samsung',
            'preco': 'R$ 2.399,00',
            'link': 'https://amzn.to/4oqm0Uj',
            'imagem': 'https://m.media-amazon.com/images/I/81DeoOAZRxL._AC_SL1500_.jpg'
        }
    ]

def enviar_para_telegram(bot, chat_id, oferta):
    legenda = f"📦 {oferta['titulo']}\n💰 {oferta['preco']}\n🔗 {oferta['link']}"
    bot.send_photo(chat_id=chat_id, photo=oferta['imagem'], caption=legenda)