import telebot
import requests
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from oferta_utils import buscar_ofertas, enviar_para_telegram

app = FastAPI()
TOKEN = "8356193016:AAHExuwPl5veXBoqazsgXvu7Bbqn9aKACcI"
CHAT_ID = "-1002808972406"
bot = telebot.TeleBot(TOKEN)

scheduler = BackgroundScheduler()

def tarefa_agendada():
    print("🔄 Executando tarefa agendada...")
    ofertas = buscar_ofertas()
    for oferta in ofertas:
        enviar_para_telegram(bot, CHAT_ID, oferta)

scheduler.add_job(tarefa_agendada, "interval", minutes=30)
scheduler.start()

@app.get("/")
def home():
    return {"status": "Bot Oferta Certa rodando"}

@app.get("/forcar-publicacao")
def forcar_publicacao():
    tarefa_agendada()
    return {"status": "Publicação forçada enviada"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("bot_oferta_certa:app", host="0.0.0.0", port=10000)