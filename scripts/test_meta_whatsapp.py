import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import settings
from core.whatsapp_server import send_whatsapp_outbound

def test_send_to_my_line():
    phone = getattr(settings, "USER_WHATSAPP_PHONE", "+526691798672")
    phone_id = getattr(settings, "META_PHONE_NUMBER_ID", "")
    token = getattr(settings, "META_ACCESS_TOKEN", "")

    print(f"=== PRUEBA DE CONEXIÓN META WHATSAPP CLOUD API ===")
    print(f"📞 Destinatario: {phone}")
    print(f"🆔 Phone Number ID: {phone_id or 'NO CONFIGURADO'}")
    print(f"🔑 Access Token: {token[:15] + '...' if token else 'NO CONFIGURADO'}")
    print("=" * 55)

    if not phone_id or not token:
        print("\n⚠️ Faltan credenciales en tu archivo .env:")
        print("   META_PHONE_NUMBER_ID=tu_phone_number_id")
        print("   META_ACCESS_TOKEN=tu_access_token")
        return

    test_message = (
        "🚀 *¡Hola! Tu conexión con Meta WhatsApp Cloud API está funcionando correctamente.*\n\n"
        "🤖 Puedes interactuar con tu bot respondiendo a este mensaje con:\n"
        "• `!resumen` - Métricas de hoy\n"
        "• `!cotizaciones` - Solicitudes de obras y electricistas\n"
        "• `!vacantes` - Últimas vacantes encontradas\n"
        "• `!ayuda` - Lista de comandos\n\n"
        "¡Éxito en tus proyectos! 💼"
    )

    print("\nEnviando mensaje de prueba...")
    res = send_whatsapp_outbound(phone, test_message)
    print("Resultado:", res)

if __name__ == "__main__":
    test_send_to_my_line()
