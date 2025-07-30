from fastapi import FastAPI, Request
import telebot
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

app = FastAPI()

BOT_TOKEN = "8356193016:AAGVhVRMA5TSLu1HuHRaPfWLSJ6Z3yTFFcQ"
CHAT_ID = "@ofertacerta"

bot = telebot.TeleBot(BOT_TOKEN)

LOGO_URL = "https://i.imgur.com/gDp5tqb.png"
FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def extrair_info_amazon(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    titulo = soup.select_one("#productTitle")
    preco = soup.select_one(".a-price .a-offscreen")
    return {
        "titulo": titulo.get_text(strip=True) if titulo else "Produto",
        "preco": preco.get_text(strip=True) if preco else "Preço indisponível"
    }

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

@app.post("/post")
async def postar(request: Request):
    data = await request.json()
    url = data.get("url")
    if not url:
        return {"erro": "URL inválida"}
    info = extrair_info_amazon(url)
    if "/dp/" in url:
        code = url.split("/dp/")[1].split("/")[0]
    else:
        return {"erro": "Link da Amazon inválido"}
    short_link = f"https://www.amazon.com.br/dp/{code}?tag=davidribeiro8-20"
    imagem = gerar_imagem(info["titulo"], info["preco"], short_link)
    bot.send_photo(CHAT_ID, imagem, caption=f"{info['titulo']}

💰 {info['preco']}
👉 {short_link}")
    return {"status": "Postado com sucesso!"}