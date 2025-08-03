from fastapi import FastAPI
from oferta_utils import buscar_ofertas, enviar_para_telegram
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

scheduler = BackgroundScheduler()
scheduler.add_job(func=enviar_para_telegram, trigger="interval", minutes=30)
scheduler.start()

@app.get("/forcar-publicacao")
async def forcar_publicacao():
    enviar_para_telegram()
    return {"status": "ok"}