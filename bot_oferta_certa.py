from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
import telebot, requests, random, logging
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

BOT_TOKEN = "8356193016:AAGVhVRMA5TSLu1HuHRaPfWLSJ6Z3yTFFcQ"
CHAT_ID = "@ofertacerta"
ADMIN_ID = 6863480446

bot = telebot.TeleBot(BOT_TOKEN)
app = FastAPI()

LOGO_URL = "https://i.imgur.com/gDp5tqb.png"
FONTE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

produtos = [
    ("B0CW1FVDP7", "Air Fryer 4L Mondial"),
    ("B09X2W4JXN", "Fone de Ouvido Sem Fio Bluetooth"),
    ("B07Z8RWMFJ", "Smart TV 50'' Samsung"),
    ("B0CW1CSN3S", "Notebook Lenovo IdeaPad"),
    ("B08ZL41ZK3", "Kit Organizadores de Gaveta"),
    ("B089M4ZTBZ", "Suporte Articulado para TV"),
    ("B0BS8MJXLN", "Echo Dot 5ª Geração"),
    ("B09F5Y2ZWX", "Cafeteira Elétrica Nespresso"),
    ("B0BTT6FT3G", "Hub USB-C HDMI"),
    ("B07X2Q44H8", "Aspirador Vertical Electrolux")
]

rotulos = [
    "🔥 Desconto Relâmpago",
    "🎯 Oferta Certa do Dia",
    "🏆 Top Achado",
    "🎟️ Cupom Exclusivo",
    "🛒 Achado Útil",
    "🚀 Oferta Quente"
]

def gerar_imagem(titulo, preco, link, rotulo):
    base = Image.new("RGB", (1080, 1080), (255, 255, 255))
    draw = ImageDraw.Draw(base)
    f1 = ImageFont.truetype(FONTE, 44)
    f2 = ImageFont.truetype(FONTE, 40)
    f3 = ImageFont.truetype(FONTE, 30)
    f4 = ImageFont.truetype(FONTE, 20)
    logo = Image.open(BytesIO(requests.get(LOGO_URL).content)).convert("RGBA").resize((250, 80))
    base.paste(logo, (50, 40), logo)
    draw.text((50, 160), rotulo, fill=(255, 102, 0), font=f1)
    draw.text((50, 250), titulo[:70], fill=(0, 0, 0), font=f1)
    draw.text((50, 350), preco, fill=(0, 128, 0), font=f2)
    draw.text((50, 450), "Compre agora 👉 " + link, fill=(60, 60, 60), font=f3)
    draw.text((800, 1020), "Oferta Certa", fill=(180, 180, 180), font=f4)
    buffer = BytesIO()
    base.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def publicar_automatico():
    try:
        asin, titulo = random.choice(produtos)
        preco = "Oferta imperdível"
        link = f"https://www.amazon.com.br/dp/{asin}?tag=davidribeiro8-20"
        rotulo = random.choice(rotulos)
        imagem = gerar_imagem(titulo, preco, link, rotulo)
    legenda = f"[OFERTA CERTA]\n\nProduto: {titulo}\nPreço: {preco}\nLink: {link}"

📦 {titulo}
💰 {preco}
👉 {link}"
        bot.send_photo(CHAT_ID, imagem, caption=legenda)
    except Exception as e:
        logging.error(f"Erro ao postar: {e}")
        bot.send_message(ADMIN_ID, f"❌ Erro no bot Oferta Certa:
{e}")

scheduler = BackgroundScheduler()
scheduler.add_job(publicar_automatico, "interval", minutes=30)
scheduler.start()