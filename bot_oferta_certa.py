
from fastapi import FastAPI
from oferta_utils import buscar_ofertas, enviar_para_telegram
import telebot
from apscheduler.schedulers.background import BackgroundScheduler

API_TOKEN = '8356193016:AAHExuwPl5veXBoqazsgXvu7Bbqn9aKACcI'
CHAT_ID = -1002808972406

bot = telebot.TeleBot(API_TOKEN)
app = FastAPI()

def tarefa():
    ofertas = buscar_ofertas()
    for oferta in ofertas:
        enviar_para_telegram(bot, CHAT_ID, oferta)

scheduler = BackgroundScheduler()
scheduler.add_job(tarefa, 'interval', minutes=30)
scheduler.start()

@app.get("/")
def read_root():
    return {"status": "Bot rodando"}

@app.get("/forcar-publicacao")
def forcar_publicacao():
    tarefa()
    return {"status": "Publicado manualmente"}
