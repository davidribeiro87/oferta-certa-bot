import os
import time
from dotenv import load_dotenv

from oferta_utils import publicar_ciclo
from keywords import KEYWORDS

load_dotenv()

INTERVAL = int(os.getenv("POST_INTERVAL_MINUTES", 30))
MAX_PER_CYCLE = int(os.getenv("MAX_PRODUCTS_PER_CYCLE", 3))

if __name__ == "__main__":
    print("[START] Bot Amazon → Telegram rodando…")
    while True:
        try:
            num = publicar_ciclo(KEYWORDS, MAX_PER_CYCLE)
            print(f"[OK] Publicados {num} item(ns) neste ciclo.")
        except Exception as e:
            print("[ERRO] ciclo:", e)
        finally:
            print(f"[SLEEP] Aguardando {INTERVAL} min…")
            time.sleep(INTERVAL * 60)
