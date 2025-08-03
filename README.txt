
Como usar este bot no Render:

1. Crie um novo serviço web no Render com seu repositório ou faça upload manual.
2. Use os seguintes env vars:
   - TELEGRAM_TOKEN = 8356193016:AAHExuwPl5veXBoqazsgXvu7Bbqn9aKACcI
   - TELEGRAM_CHAT_ID = -1002808972406
3. Configure o comando de inicialização:
   uvicorn bot_oferta_certa:app --host 0.0.0.0 --port 10000
4. Use /forcar-publicacao para testar.
