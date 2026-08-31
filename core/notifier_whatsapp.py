import urllib.parse
from typing import Optional, Dict, Any
from config.settings import USER_WHATSAPP_PHONE, WHATSAPP_API_KEY

def generate_whatsapp_message(
    job_title: str,
    company: str = "Empresa",
    candidate_name: str = "Ingeniero / Técnico",
    category: Optional[str] = None
) -> str:
    """
    Generate a professional WhatsApp message in Spanish for job applications
    or technician opportunities.
    """
    if category and "RF" in category:
        pitch = "Cuento con experiencia en ingeniería de RF, optimización RAN (4G/5G), Drive Test, fibra óptica y herramientas de medición."
    elif category and "Eléctric" in category:
        pitch = "Cuento con experiencia en proyectos e instalaciones eléctricas residenciales e industriales, media y baja tensión, tableros y cumplimiento de NOM-001-SEDE."
    elif category and ("Sistemas" in category or "Software" in category):
        pitch = "Cuento con experiencia en sistemas, cableado estructurado, redes LAN, soporte técnico e infraestructura TI."
    else:
        pitch = "Cuento con sólida formación técnica y disponibilidad inmediata para realizar trabajos y proyectos."

    message = (
        f"¡Hola! Buen día. Espero que te encuentres muy bien.\n\n"
        f"Te contacto con respecto a la oportunidad de *{job_title}* para *{company}*.\n\n"
        f"{pitch}\n\n"
        f"Me interesa mucho la posición y brindar nuestros servicios. ¿Sigue disponible? Con gusto te comparto mi información detallada.\n\n"
        f"Quedo a tu disposición. ¡Muchas gracias!"
    )
    return message

def generate_quotation_message(
    service_title: str,
    contact_name: str = "Cliente",
    location: str = "su ubicación",
    provider_name: str = "Ingeniero / Contratista Eléctrico"
) -> str:
    """
    Generate a customized, professional proposal and quotation message
    for clients/contractors needing electrical installations and technician services.
    """
    clean_contact = contact_name if contact_name and contact_name != "Facebook" else "Estimado cliente"
    message = (
        f"¡Hola {clean_contact}! Buen día. Espero que se encuentre muy bien.\n\n"
        f"Vi su solicitud en Facebook requiriendo servicio de *{service_title}* en *{location}*.\n\n"
        f"Somos especialistas en *instalaciones eléctricas, canalizaciones, tableros, transformadores y mantenimiento industrial/comercial* bajo la norma NOM-001-SEDE.\n\n"
        f"Con gusto podemos hacerle una visita técnica o revisar el alcance de su proyecto para enviarle una *cotización formal y presupuesto detallado* con los mejores tiempos de entrega y garantía.\n\n"
        f"¿Me podría compartir más detalles del trabajo o la dirección exacta para agendar el levantamiento? ¡Quedo a sus órdenes!"
    )
    return message

def generate_whatsapp_link(
    phone: str,
    job_title: str = "el trabajo / servicio",
    company: str = "su empresa",
    candidate_name: str = "Ingeniero",
    category: Optional[str] = None
) -> str:
    """
    Construct a direct wa.me link with URL-encoded greeting message.
    """
    clean_phone = "".join(c for c in phone if c.isdigit())
    if clean_phone.startswith("521") and len(clean_phone) == 13:
        pass
    elif len(clean_phone) == 10:
        clean_phone = f"52{clean_phone}"

    # If it is an installation / quote request, use the quotation message template
    if any(k in job_title.lower() for k in ["instalación", "instalacion", "cotización", "cotizacion", "servicio", "presupuesto", "obra", "remodelación"]):
        msg = generate_quotation_message(job_title, company, "México")
    else:
        msg = generate_whatsapp_message(job_title, company, candidate_name, category)
        
    encoded_msg = urllib.parse.quote(msg)
    return f"https://wa.me/{clean_phone}?text={encoded_msg}"

def notify_new_match(job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format and prepare notification payload for a newly found job or service lead.
    """
    title = job.get("title", "Vacante")
    company = job.get("company", "Empresa")
    salary = job.get("salary_raw", "No especificado")
    phone = job.get("phone", "")
    category = job.get("category", "")
    url = job.get("url", "")

    wa_contact_url = generate_whatsapp_link(phone, title, company, category=category) if phone else None

    summary_text = (
        f"🎯 *NUEVA OPORTUNIDAD DETECTADA*\n"
        f"📌 *Puesto / Trabajo:* {title}\n"
        f"🏢 *Contacto / Cliente:* {company}\n"
        f"🏷️ *Especialidad:* {category}\n"
        f"💰 *Presupuesto / Sueldo:* {salary}\n"
        f"📍 *Ubicación:* {job.get('location', 'México')} ({job.get('modality', 'No especificado')})\n"
    )
    if phone:
        summary_text += f"📞 *Teléfono:* {phone}\n"
    if url:
        summary_text += f"🔗 *Enlace:* {url}\n"

    return {
        "summary": summary_text,
        "whatsapp_link": wa_contact_url,
        "phone": phone
    }