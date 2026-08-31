import sys
import json
import time
import logging
import threading
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parent.parent))

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import requests

from config import settings
from core.whatsapp_bot import WhatsAppBot

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("WhatsAppServer")

bot_engine = WhatsAppBot()

def send_whatsapp_outbound(to_phone: str, message: str) -> Dict[str, Any]:
    """
    Send outbound WhatsApp message using configured provider (GreenAPI / Meta / UltraMsg / Twilio).
    """
    provider = getattr(settings, "WHATSAPP_PROVIDER", "greenapi").lower()
    
    # 1. GreenAPI Provider
    if provider == "greenapi":
        instance_id = getattr(settings, "GREENAPI_INSTANCE_ID", "")
        api_token = getattr(settings, "GREENAPI_API_TOKEN", "")
        if instance_id and api_token:
            clean_phone = "".join(c for c in to_phone if c.isdigit())
            if not clean_phone.endswith("@c.us"):
                clean_phone = f"{clean_phone}@c.us"
            
            url = f"https://api.green-api.com/waInstance{instance_id}/sendMessage/{api_token}"
            payload = {
                "chatId": clean_phone,
                "message": message
            }
            try:
                r = requests.post(url, json=payload, timeout=15)
                return {"success": r.status_code == 200, "response": r.text}
            except Exception as e:
                logger.error(f"Error sending GreenAPI message: {e}")
                return {"success": False, "error": str(e)}

    # 2. Meta WhatsApp Cloud API Provider
    elif provider == "meta":
        phone_id = getattr(settings, "META_PHONE_NUMBER_ID", "")
        access_token = getattr(settings, "META_ACCESS_TOKEN", "")
        if phone_id and access_token:
            clean_phone = "".join(c for c in to_phone if c.isdigit())
            url = f"https://graph.facebook.com/v18.0/{phone_id}/messages"
            headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": clean_phone,
                "type": "text",
                "text": {"body": message}
            }
            try:
                r = requests.post(url, headers=headers, json=payload, timeout=15)
                return {"success": r.status_code == 200, "response": r.text}
            except Exception as e:
                logger.error(f"Error sending Meta Cloud message: {e}")
                return {"success": False, "error": str(e)}

    return {"success": True, "note": "Simulation mode or credentials not configured"}

def run_greenapi_polling_loop():
    """
    Direct polling loop for GreenAPI.
    Receives incoming WhatsApp messages from your phone line (+52...) without needing ngrok or open ports.
    """
    instance_id = getattr(settings, "GREENAPI_INSTANCE_ID", "")
    api_token = getattr(settings, "GREENAPI_API_TOKEN", "")

    if not instance_id or not api_token:
        logger.info("[GreenAPI Polling] Instance ID o API Token no configurados. En espera de credenciales en .env...")
        return

    logger.info(f"🔄 Iniciando escucha activa GreenAPI para la instancia {instance_id}...")
    receive_url = f"https://api.green-api.com/waInstance{instance_id}/ReceiveNotification/{api_token}"

    while True:
        try:
            r = requests.get(receive_url, timeout=25)
            if r.status_code == 200 and r.text and r.text != "null":
                notification = r.json()
                receipt_id = notification.get("receiptId")
                body = notification.get("body", {})
                type_webhook = body.get("typeWebhook")

                if type_webhook == "incomingMessageReceived":
                    msg_data = body.get("messageData", {})
                    incoming_text = (
                        msg_data.get("textMessageData", {}).get("textMessage")
                        or msg_data.get("extendedTextMessageData", {}).get("text", "")
                    )
                    sender_data = body.get("senderData", {})
                    sender_chat = sender_data.get("chatId", "")
                    sender_phone = sender_chat.replace("@c.us", "")

                    if incoming_text:
                        logger.info(f"📱 Mensaje recibido de +{sender_phone}: '{incoming_text}'")
                        reply_text = bot_engine.process_message(incoming_text, sender_phone)
                        send_whatsapp_outbound(sender_chat, reply_text)
                        logger.info(f"✅ Respuesta enviada exitosamente a +{sender_phone}")

                # Delete processed notification from GreenAPI queue
                if receipt_id:
                    delete_url = f"https://api.green-api.com/waInstance{instance_id}/DeleteNotification/{api_token}/{receipt_id}"
                    requests.delete(delete_url, timeout=10)

        except Exception as e:
            time.sleep(2)

        time.sleep(0.5)

class WhatsAppWebhookHandler(BaseHTTPRequestHandler):
    """
    HTTP Request Handler for universal WhatsApp Webhooks and testing endpoints.
    """

    def _send_json_response(self, data: Dict[str, Any], status_code: int = 200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        # Meta Webhook Verification challenge
        if parsed.path in ["/whatsapp/webhook", "/webhook"]:
            hub_mode = params.get("hub.mode", [""])[0]
            hub_token = params.get("hub.verify_token", [""])[0]
            hub_challenge = params.get("hub.challenge", [""])[0]

            expected_token = getattr(settings, "META_VERIFY_TOKEN", "autojob_token_2026")
            if hub_mode == "subscribe" and hub_token == expected_token:
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(hub_challenge.encode("utf-8"))
                return

            self._send_json_response({
                "status": "active",
                "service": "AutoJob Hunter WhatsApp Webhook",
                "configured_phone": getattr(settings, "USER_WHATSAPP_PHONE", ""),
                "timestamp": str(datetime.now())
            })
            return

        elif parsed.path in ["/whatsapp/status", "/health"]:
            self._send_json_response({
                "status": "healthy",
                "uptime": "running",
                "bot": "WhatsAppBot Interactive Engine",
                "user_phone": getattr(settings, "USER_WHATSAPP_PHONE", "")
            })
            return

        self._send_json_response({"error": "Not found"}, 404)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else ""

        incoming_text = ""
        sender_phone = ""

        content_type = self.headers.get("Content-Type", "")
        if "application/json" in content_type:
            try:
                data = json.loads(raw_body)
            except Exception:
                data = {}

            if "text" in data:
                incoming_text = data.get("text", "")
                sender_phone = data.get("phone", "")

            elif data.get("typeWebhook") == "incomingMessageReceived":
                msg_data = data.get("messageData", {})
                incoming_text = (
                    msg_data.get("textMessageData", {}).get("textMessage")
                    or msg_data.get("extendedTextMessageData", {}).get("text", "")
                )
                sender_phone = data.get("senderData", {}).get("chatId", "").replace("@c.us", "")

            elif "data" in data and "body" in data["data"]:
                incoming_text = data["data"].get("body", "")
                sender_phone = data["data"].get("from", "").replace("@c.us", "")

            elif "entry" in data:
                try:
                    entry = data["entry"][0]
                    changes = entry["changes"][0]
                    value = changes["value"]
                    if "messages" in value:
                        msg = value["messages"][0]
                        sender_phone = msg.get("from", "")
                        if msg.get("type") == "text":
                            incoming_text = msg.get("text", {}).get("body", "")
                except Exception as e:
                    logger.error(f"Error parsing Meta payload: {e}")

        elif "application/x-www-form-urlencoded" in content_type:
            form_data = urllib.parse.parse_qs(raw_body)
            incoming_text = form_data.get("Body", [""])[0]
            sender_phone = form_data.get("From", [""])[0].replace("whatsapp:", "")

        if incoming_text:
            logger.info(f"Incoming message from '{sender_phone}': '{incoming_text}'")
            reply_text = bot_engine.process_message(incoming_text, sender_phone)
            
            if sender_phone:
                send_whatsapp_outbound(sender_phone, reply_text)

            self._send_json_response({
                "success": True,
                "input": incoming_text,
                "sender": sender_phone,
                "reply": reply_text
            })
            return

        self._send_json_response({
            "success": False,
            "error": "No text received in payload"
        }, 400)

def run_webhook_server(port: int = 5000):
    """Start local HTTP Webhook Server and background GreenAPI polling listener."""
    # Launch GreenAPI Polling thread if credentials exist
    instance_id = getattr(settings, "GREENAPI_INSTANCE_ID", "")
    api_token = getattr(settings, "GREENAPI_API_TOKEN", "")
    if instance_id and api_token:
        polling_thread = threading.Thread(target=run_greenapi_polling_loop, daemon=True)
        polling_thread.start()
        logger.info("📡 Escucha continua en segundo plano iniciada para GreenAPI.")

    server_address = ("", port)
    httpd = HTTPServer(server_address, WhatsAppWebhookHandler)
    logger.info(f"🚀 Servidor Webhook de WhatsApp iniciado en http://localhost:{port}")
    logger.info(f"👉 Endpoint Webhook: http://localhost:{port}/whatsapp/webhook")
    logger.info(f"📞 Línea de WhatsApp configurada: {getattr(settings, 'USER_WHATSAPP_PHONE', '+526691798672')}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Servidor detenido.")
        httpd.server_close()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 5000
    run_webhook_server(port)
