
import os
import time
import asyncio
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from oferta_utils import buscar_ofertas, enviar_para_telegram

app = FastAPI()

# Função principal de publicação automática
def publicar_ofertas():
    try:
        ofertas = buscar_ofertas()
        for oferta in ofertas:
            enviar_para_telegram(oferta)
            time.sleep(2)
    except Exception as e:
        print(f"Erro ao publicar ofertas: {e}")

# Agendador
scheduler = BackgroundScheduler()
scheduler.add_job(publicar_ofertas, "interval", minutes=30)
scheduler.start()

@app.get("/")
def home():
    return {"status": "Bot de ofertas está ativo."}

@app.get("/forcar-publicacao")
def forcar_publicacao():
    publicar_ofertas()
    return {"status": "Publicação forçada executada com sucesso"}
