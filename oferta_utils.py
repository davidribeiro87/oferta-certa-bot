import hashlib, hmac, datetime, json, os, random, time, requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PARTNER_TAG = os.getenv("AMAZON_PARTNER_TAG")
ACCESS_KEY = os.getenv("AMAZON_ACCESS_KEY")
SECRET_KEY = os.getenv("AMAZON_SECRET_KEY")
REGION = os.getenv("AMAZON_REGION", "BR")
HOST = os.getenv("AMAZON_HOST", "webservices.amazon.com.br")

SERVICE = "ProductAdvertisingAPI"
URI = "/paapi5/searchitems"

def _sign(key, msg): return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

def _get_signature_key(key, date_stamp, region_name, service_name):
    k_date = _sign(("AWS4"+key).encode("utf-8"), date_stamp)
    k_region = _sign(k_date, region_name)
    k_service = _sign(k_region, service_name)
    k_signing = _sign(k_service, "aws4_request")
    return k_signing

def _amz_datetime():
    now = datetime.datetime.utcnow()
    return now.strftime("%Y%m%dT%H%M%SZ"), now.strftime("%Y%m%d")

def _canonical_headers(amz_dt):
    return f"content-encoding:amz-1.0\\ncontent-type:application/json; charset=utf-8\\nhost:{HOST}\\nx-amz-date:{amz_dt}\\n"

def _signed_headers(): return "content-encoding;content-type;host;x-amz-date"

def _authorization_header(amz_dt, date_stamp, payload_hash, region, canonical_request):
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{date_stamp}/{region}/{SERVICE}/aws4_request"
    string_to_sign = f"{algorithm}\\n{amz_dt}\\n{credential_scope}\\n{hashlib.sha256(canonical_request.encode()).hexdigest()}"
    signing_key = _get_signature_key(SECRET_KEY, date_stamp, region, SERVICE)
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{algorithm} Credential={ACCESS_KEY}/{credential_scope}, SignedHeaders={_signed_headers()}, Signature={signature}"

def _do_paapi_request(uri, payload_dict, region=REGION):
    amz_dt, date_stamp = _amz_datetime()
    payload = json.dumps(payload_dict)
    payload_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_headers = _canonical_headers(amz_dt)
    canonical_request = f"POST\\n{uri}\\n\\n{canonical_headers}\\n{_signed_headers()}\\n{payload_hash}"
    auth = _authorization_header(amz_dt, date_stamp, payload_hash, region.lower(), canonical_request)
    headers = {"content-encoding":"amz-1.0","content-type":"application/json; charset=utf-8","host":HOST,"x-amz-date":amz_dt,"Authorization":auth}
    url = f"https://{HOST}{uri}"
    resp = requests.post(url, headers=headers, data=payload, timeout=20)
    resp.raise_for_status()
    return resp.json()

def buscar_itens_por_keyword(keyword, page=1, max_results=10):
    payload = {"Keywords":keyword,"PartnerTag":PARTNER_TAG,"PartnerType":"Associates","Marketplace":"www.amazon.com.br","ItemCount":max_results,"ItemPage":page,
               "Resources":["Images.Primary.Large","Images.Primary.Medium","ItemInfo.Title","Offers.Listings.Price","Offers.Listings.IsPrimeEligible","Offers.Listings.DeliveryInfo.IsAmazonFulfilled"]}
    try:
        data = _do_paapi_request(URI, payload)
        items = data.get("SearchResult", {}).get("Items", [])
        resultados = []
        for it in items:
            try:
                asin = it.get("ASIN")
                title = it.get("ItemInfo", {}).get("Title", {}).get("DisplayValue")
                img = (it.get("Images", {}).get("Primary", {}).get("Large", {}).get("URL") or it.get("Images", {}).get("Primary", {}).get("Medium", {}).get("URL"))
                offer = (it.get("Offers", {}) or {}).get("Listings", [{}])[0]
                price = (offer.get("Price") or {}).get("DisplayAmount")
                prime = offer.get("IsPrimeEligible")
                fulfilled = (offer.get("DeliveryInfo") or {}).get("IsAmazonFulfilled")
                resultados.append({"asin":asin,"title":title,"image_url":img,"price":price,"prime":prime,"fulfilled":fulfilled,"link":gerar_link_afiliado(asin)})
            except Exception:
                continue
        return resultados
    except Exception as e:
        print("[ERRO] buscar_itens_por_keyword:", e)
        return []

def gerar_link_afiliado(asin: str) -> str:
    return f"https://www.amazon.com.br/dp/{asin}?tag={PARTNER_TAG}"

def enviar_para_telegram(item: dict) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[ERRO] TELEGRAM_BOT_TOKEN/CHAT_ID não configurados")
        return False
    titulo = item.get("title","Oferta Amazon")
    preco = item.get("price","Ver preço")
    link = item.get("link")
    img = item.get("image_url")
    badges = []
    if item.get("prime"): badges.append("Prime")
    if item.get("fulfilled"): badges.append("Full")
    badge_str = " | ".join(badges)
    badge_line = f"\\n{badge_str}" if badge_str else ""
    pagamento = "Formas de pagamento na Amazon: cartão, boleto e Pix (sujeito a elegibilidade)."
    legenda = f"📦 {titulo}\\n💰 {preco}{badge_line}\\n🛒 {pagamento}\\n➡️ Compre aqui: {link}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
    payload = {"chat_id":TELEGRAM_CHAT_ID,"photo": img or "https://m.media-amazon.com/images/G/01/social/api-share/amazon_logo_500500._CB633266945_.png","caption":legenda,"parse_mode":"HTML"}
    try:
        r = requests.post(url, data=payload, timeout=30)
        if not r.ok: print("[ERRO] Telegram:", r.text)
        return r.ok
    except Exception as e:
        print("[ERRO] enviar_para_telegram:", e)
        return False

def publicar_ciclo(keywords: list, max_products: int = 3) -> int:
    random.shuffle(keywords)
    publicados = 0
    for kw in keywords:
        if publicados >= max_products: break
        itens = buscar_itens_por_keyword(kw, page=1, max_results=10)
        random.shuffle(itens)
        for item in itens:
            if publicados >= max_products: break
            if enviar_para_telegram(item):
                publicados += 1
                time.sleep(2)
    return publicados
