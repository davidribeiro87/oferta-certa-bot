import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def buscar_ofertas():
    return [
        {
            "titulo": "Echo Dot (5ª geração) com Relógio",
            "preco": "R$ 379,99",
            "link": "https://amzn.to/40Ic1zq",
            "imagem": "https://m.media-amazon.com/images/I/71RjW+0UftL._AC_SL1500_.jpg",
            "categoria": "Tecnologia"
        }
    ]

def gerar_imagem(titulo, preco, imagem_url):
    response = requests.get(imagem_url)
    img = Image.open(BytesIO(response.content)).convert("RGB")
    img = img.resize((800, 800))

    draw = ImageDraw.Draw(img)
    fonte = ImageFont.load_default()

    draw.rectangle([0, 720, 800, 800], fill="black")
    draw.text((10, 730), f"{titulo} - {preco}", font=fonte, fill="white")

    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return buffer

def enviar_para_telegram(bot, chat_id, oferta):
    imagem = gerar_imagem(oferta["titulo"], oferta["preco"], oferta["imagem"])
    legenda = f"📦 {oferta['titulo']}
💰 {oferta['preco']}
🔗 {oferta['link']}"
    bot.send_photo(chat_id, imagem, caption=legenda)