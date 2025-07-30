from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
import telebot
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

BOT_TOKEN = "8356193016:AAGVhVRMA5TSLu1HuHRaPfWLSJ6Z3yTFFcQ"
CHAT_ID = "@ofertacerta"

bot = telebot.TeleBot(BOT_TOKEN)
app = FastAPI()

LOGO_URL = "https://i.imgur.com/gDp5tqb.png"
FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def buscar_produto_amazon():
    url = "https://www.amazon.com.br/dp/B09X2W4JXN"
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    titulo = soup.select_one("#productTitle")
    preco = soup.select_one(".a-price .a-offscreen")
    titulo = titulo.get_text(strip=True) if titulo else "Produto"
    preco = preco.get_text(strip=True) if preco else "Preço indisponível"
    code = url.split("/dp/")[1].split("/")[0]
    link = f"https://www.amazon.com.br/dp/{code}?tag=davidribeiro8-20"
    return titulo, preco, link

def gerar_imagem(titulo, preco, link):
    base = Image.new("RGB", (1080, 1080), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    fonte_titulo = ImageFont.truetype(FONTE, 44)
    fonte_preco = ImageFont.truetype(FONTE, 40)
    fonte_link = ImageFont.truetype(FONTE, 30)
    fonte_marca = ImageFont.truetype(FONTE, 20)
    response = requests.get(LOGO_URL)
    logo = Image.open(BytesIO(response.content)).convert("RGBA").resize((250, 80))
    base.paste(logo, (50, 40), logo)
    draw.text((50, 160), "🔥 Desconto Relâmpago", fill=(255, 102, 0), font=fonte_titulo)
    draw.text((50, 250), titulo[:70], fill=(0, 0, 0), font=fonte_titulo)
    draw.text((50, 350), preco, fill=(0, 128, 0), font=fonte_preco)
    draw.text((50, 450), "Compre agora 👉 " + link, fill=(60, 60, 60), font=fonte_link)
    draw.text((800, 1020), "Oferta Certa", fill=(180, 180, 180), font=fonte_marca)
    buffer = BytesIO()
    base.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def publicar_automatico():
    try:
        titulo, preco, link = buscar_produto_amazon()
        imagem = gerar_imagem(titulo, preco, link)
        legenda = f"{titulo}

💰 {preco}
👉 {link}"
        bot.send_photo(CHAT_ID, imagem, caption=legenda)
        print("✔️ Oferta postada com sucesso!")
    except Exception as e:
        print("Erro ao publicar:", e)

scheduler = BackgroundScheduler()
scheduler.add_job(publicar_automatico, "interval", minutes=30)
scheduler.start()