import os
import httpx
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY")
WHATSAPP_INSTANCE = os.getenv("WHATSAPP_INSTANCE")

async def send_whatsapp_message(phone: str, message: str):
    """
    Envia uma mensagem via Evolution API.
    """
    if not WHATSAPP_API_URL or not WHATSAPP_API_KEY or not WHATSAPP_INSTANCE:
        print("[WHATSAPP] Credenciais não configuradas no .env. Ignorando envio.")
        return False

    url = f"{WHATSAPP_API_URL}/message/sendText/{WHATSAPP_INSTANCE}"
    
    headers = {
        "Content-Type": "application/json",
        "apikey": WHATSAPP_API_KEY
    }
    
    payload = {
        "number": phone,
        "text": message
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 201 or response.status_code == 200:
                print(f"[WHATSAPP] Mensagem enviada para {phone}")
                return True
            else:
                print(f"[WHATSAPP] Erro ao enviar: {response.status_code} - {response.text}")
                return False
    except Exception as e:
        print(f"[WHATSAPP] Exceção ao enviar: {str(e)}")
        return False
