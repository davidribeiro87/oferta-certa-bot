from fastapi import FastAPI
from oferta_utils import buscar_ofertas, enviar_para_telegram

app = FastAPI()

@app.get("/forcar-publicacao")
async def forcar_publicacao():
    ofertas = buscar_ofertas()
    for oferta in ofertas:
        enviar_para_telegram(oferta)
    return {"status": "publicações enviadas com sucesso"}