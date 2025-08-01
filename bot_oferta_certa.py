import telebot
from fastapi import FastAPI

app = FastAPI()

BOT_TOKEN = ""8356193016:AAHExuwPl5veXBoqazsgXvu7Bbqn9aKACcI"
bot = telebot.TeleBot(BOT_TOKEN)

@app.get("/")
def read_root():
    return {"message": "Bot está rodando!"}

@bot.message_handler(commands=['oferta'])
def enviar_oferta(mensagem):
    titulo = "Produto Exemplo"
    preco = "R$ 199,99"
    link = "https://amzn.to/exemplo"
    rotulo = "[OFERTA CERTA]"
    legenda = f"{rotulo}\n\nProduto: {titulo}\nPreço: {preco}\nLink: {link}"
    bot.send_message(mensagem.chat.id, legenda)

import threading
threading.Thread(target=bot.polling, kwargs={"none_stop": True}).start()
