import urllib.parse
from typing import Optional, Dict, Any
from config.settings import USER_WHATSAPP_PHONE, WHATSAPP_API_KEY

def generate_whatsapp_message(
    job_title: str,
    company: str = "Empresa",
    candidate_name: str = "Ingeniero",
    category: Optional[str] = None
) -> str:
    """
    Generate a professional and courteous WhatsApp message in Spanish
    tailored to Mexican engineering recruiters.
    """
    if category and "RF" in category:
        pitch = "Cuento con experiencia en ingeniería de RF, optimización RAN (4G/5G), Drive Test y herramientas como TEMS/Atoll."
    elif category and "Eléctric" in category:
        pitch = "Cuento con experiencia en proyectos eléctricos, media y alta tensión, subestaciones y cumplimiento de NOM-001-SEDE."
    elif category and ("Sistemas" in category or "Software" in category):
        pitch = "Cuento con experiencia en desarrollo de software, Python/FastAPI, arquitecturas cloud, microservicios y bases de datos."
    else:
        pitch = "Cuento con sólida formación en ingeniería y disponibilidad inmediata para incorporarme a su equipo."

    message = (
        f"¡Hola! Buen día. Espero que te encuentres muy bien.\n\n"
        f"Te contacto con respecto a la vacante de *{job_title}* para *{company}*.\n\n"
        f"{pitch}\n\n"
        f"Me interesa mucho la posición y postularme formalmente. ¿Sigue disponible? Con gusto te comparto mi CV detallado.\n\n"
        f"Quedo a tu disposición. ¡Muchas gracias!"
    )
    return message

def generate_whatsapp_link(
    phone: str,
    job_title: str = "la vacante de ingeniería",
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

    msg = generate_whatsapp_message(job_title, company, candidate_name, category)
    encoded_msg = urllib.parse.quote(msg)
    return f"https://wa.me/{clean_phone}?text={encoded_msg}"

def notify_new_match(job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format and prepare notification payload for a newly found high-match job.
    """
    title = job.get("title", "Vacante")
    company = job.get("company", "Empresa")
    salary = job.get("salary_raw", "No especificado")
    phone = job.get("phone", "")
    category = job.get("category", "")
    url = job.get("url", "")

    wa_contact_url = generate_whatsapp_link(phone, title, company, category=category) if phone else None

    summary_text = (
        f"🎯 *NUEVA VACANTE DETECTADA*\n"
        f"📌 *Puesto:* {title}\n"
        f"🏢 *Empresa:* {company}\n"
        f"🏷️ *Especialidad:* {category}\n"
        f"💰 *Sueldo:* {salary}\n"
        f"📍 *Ubicación:* {job.get('location', 'México')} ({job.get('modality', 'No especificado')})\n"
    )
    if phone:
        summary_text += f"📞 *Contacto:* {phone}\n"
    if url:
        summary_text += f"🔗 *Enlace:* {url}\n"

    return {
        "summary": summary_text,
        "whatsapp_link": wa_contact_url,
        "phone": phone
    }