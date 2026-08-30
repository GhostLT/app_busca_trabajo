import re
import urllib.parse
from typing import Dict, Any, Tuple, Optional, List
from config.settings import get_keywords

def extract_phone(text: str) -> Optional[str]:
    """
    Extract and clean Mexican phone numbers (+52, 10-digit).
    """
    if not text:
        return None

    # Check for direct wa.me link with phone first
    wa_match = re.search(r'wa\.me/(?:send\?phone=)?(\+?52\d{10,11}|\d{10,12})', text, re.IGNORECASE)
    if wa_match:
        digits = re.sub(r'\D', '', wa_match.group(1))
        if digits.startswith("52") and len(digits) in (12, 13):
            return f"+{digits}"
        elif len(digits) == 10:
            return f"+52{digits}"
        return f"+{digits}"

    # Mexican phone patterns
    patterns = [
        r'(?:\+?52\s*(?:1\s*)?)?(?:\(?\d{2,3}\)?[\s.-]*)?\d{3,4}[\s.-]*\d{4}',
        r'\b\d{10}\b'
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, text):
            match_str = match.group(0)
            digits = re.sub(r'\D', '', match_str)
            
            if len(digits) == 10:
                return f"+52{digits}"
            elif len(digits) == 11 and digits.startswith("1"):
                return f"+52{digits[1:]}"
            elif len(digits) in (12, 13) and digits.startswith("52"):
                return f"+{digits}"

    return None

def extract_whatsapp_url(text: str, phone: Optional[str] = None) -> Optional[str]:
    """
    Find explicit wa.me URL or construct one from extracted phone number.
    """
    if text:
        wa_url_match = re.search(r'(https?://(?:wa\.me|api\.whatsapp\.com/send)[^\s<>"\'\)]+)', text, re.IGNORECASE)
        if wa_url_match:
            return wa_url_match.group(1)

    clean_phone = phone or extract_phone(text or "")
    if clean_phone:
        digits_only = re.sub(r'\D', '', clean_phone)
        return f"https://wa.me/{digits_only}"

    return None

def extract_salary(text: str) -> Tuple[Optional[float], Optional[float], str]:
    """
    Extract salary range (min, max, raw_string).
    """
    if not text:
        return (None, None, "")

    cleaned = text.replace(",", "")

    # Range pattern: $20000 a $35000, 20000 - 35000, $20k - $35k
    range_match = re.search(
        r'\$?\s*(\d{2,6}|\d{1,2}k)\s*(?:-|a|al|hasta|to)\s*\$?\s*(\d{2,6}|\d{1,2}k)',
        cleaned,
        re.IGNORECASE
    )

    if range_match:
        v1_raw = range_match.group(1).lower()
        v2_raw = range_match.group(2).lower()

        v1 = float(v1_raw.replace("k", "000")) if "k" in v1_raw else float(v1_raw)
        v2 = float(v2_raw.replace("k", "000")) if "k" in v2_raw else float(v2_raw)

        if 4000 <= v1 <= 300000 or 4000 <= v2 <= 300000:
            s_min = min(v1, v2)
            s_max = max(v1, v2)
            raw = f"${s_min:,.0f} - ${s_max:,.0f} MXN"
            return (s_min, s_max, raw)

    # Single salary pattern: $30,000 mensuales, sueldo: 28000
    single_match = re.search(
        r'(?:sueldo|salario|pago|ofrecemos|ganancias?)[:\s]*\$?\s*(\d{4,6}|\d{1,2}k)',
        cleaned,
        re.IGNORECASE
    )
    if single_match:
        v_raw = single_match.group(1).lower()
        v = float(v_raw.replace("k", "000")) if "k" in v_raw else float(v_raw)
        if 4000 <= v <= 300000:
            raw = f"${v:,.0f} MXN"
            return (v, v, raw)

    # Simple dollar amount match
    dollar_match = re.search(r'\$\s*(\d{4,6})\b', cleaned)
    if dollar_match:
        v = float(dollar_match.group(1))
        if 4000 <= v <= 300000:
            return (v, v, f"${v:,.0f} MXN")

    return (None, None, "")

def extract_location_and_modality(text: str) -> Tuple[str, str]:
    """
    Extract location (City/State) and working modality (Remoto/Híbrido/Presencial).
    """
    if not text:
        return ("México", "No especificado")

    lower_text = text.lower()

    # Modality
    modality = "No especificado"
    if "100% remoto" in lower_text or "home office" in lower_text or "remoto" in lower_text or "teletrabajo" in lower_text:
        if "híbrido" in lower_text or "hibrido" in lower_text:
            modality = "Híbrido"
        else:
            modality = "Remoto"
    elif "híbrido" in lower_text or "hibrido" in lower_text or "esquema mixto" in lower_text:
        modality = "Híbrido"
    elif "presencial" in lower_text or "en sitio" in lower_text or "planta" in lower_text or "obra" in lower_text:
        modality = "Presencial"

    # Known locations in Mexico
    locations = [
        ("Ciudad de México", ["cdmx", "ciudad de méxico", "ciudad de mexico", "distrito federal", "santa fe", "polanco", "reforma", "insurgentes", "tlalnepantla", "naucalpan"]),
        ("Estado de México", ["estado de méxico", "estado de mexico", "edomex", "toluca", "cuautitlán", "ecatepec"]),
        ("Guadalajara", ["guadalajara", "gdl", "zapopan", "jalisco", "tlaquepaque"]),
        ("Monterrey", ["monterrey", "mty", "nuevo león", "nuevo leon", "san pedro", "apodaca", "guadalupe"]),
        ("Querétaro", ["querétaro", "queretaro", "qro", "el marqués", "juriquilla"]),
        ("Puebla", ["puebla", "cholula"]),
        ("Tijuana", ["tijuana", "baja california"]),
        ("Mérida", ["mérida", "merida", "yucatán"]),
        ("León", ["león", "leon", "guanajuato", "silao", "irapuato"]),
        ("San Luis Potosí", ["san luis potosí", "san luis potosi", "slp"]),
        ("Aguascalientes", ["aguascalientes", "ags"])
    ]

    location = "México"
    for loc_name, aliases in locations:
        for alias in aliases:
            if re.search(r'\b' + re.escape(alias) + r'\b', lower_text):
                location = loc_name
                break
        if location != "México":
            break

    if modality == "Remoto" and location == "México":
        location = "Remoto (México)"

    return (location, modality)

def classify_category(text: str, title: str = "") -> str:
    """
    Classify job into one of the 3 key engineering specialties based on keyword hits.
    """
    combined = f"{title} {text}".lower()
    keywords_config = get_keywords().get("categories", {})

    scores: Dict[str, int] = {}

    for category, meta in keywords_config.items():
        score = 0
        keywords_list = meta.get("keywords", [])
        for kw in keywords_list:
            kw_lower = kw.lower()
            if kw_lower in title.lower():
                score += 3
            if kw_lower in combined:
                score += 1
        scores[category] = score

    if not scores or max(scores.values()) == 0:
        if any(term in combined for term in ["rf", "radiofrecuencia", "drive test", "ran", "ericsson", "huawei", "telecom"]):
            return "Ingeniero de RF / Optimización"
        elif any(term in combined for term in ["eléctrico", "electrico", "subestacion", "media tension", "potencia"]):
            return "Ingeniero Eléctrico"
        elif any(term in combined for term in ["software", "sistemas", "python", "backend", "frontend", "devops", "cloud", "programador"]):
            return "Ingeniero de Sistemas / Software"
        return "Ingeniero de RF / Optimización"

    best_cat = max(scores, key=scores.get)
    return best_cat

def parse_job_post(
    text: str,
    source: str = "Facebook",
    fallback_title: Optional[str] = None,
    company: Optional[str] = None
) -> Dict[str, Any]:
    """
    Parse an entire unstructured text post into a standardized job record dict.
    """
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    first_line = lines[0] if lines else "Vacante de Ingeniería"

    title = fallback_title
    if not title:
        for line in lines[:4]:
            cleaned_line = re.sub(r'^[#*•\-\s]+', '', line)
            if any(w in cleaned_line.lower() for w in ["ingeniero", "desarrollador", "consultor", "analista", "vacante", "buscamos", "solicitamos", "posicion", "especialista"]):
                title = cleaned_line
                break
        if not title:
            title = first_line[:80]

    category = classify_category(text, title=title)
    phone = extract_phone(text)
    wa_url = extract_whatsapp_url(text, phone=phone)
    sal_min, sal_max, sal_raw = extract_salary(text)
    location, modality = extract_location_and_modality(text)

    comp = company or "Reclutador en Redes Sociales"
    comp_match = re.search(r'(?:empresa|compañía|cliente|para)[:\s]+([A-Za-z0-9\s&.-]{3,30})', text, re.IGNORECASE)
    if comp_match:
        extracted_comp = comp_match.group(1).strip()
        if not any(stop in extracted_comp.lower() for stop in ["importante", "reconocida", "líder", "confidencial", "solicita"]):
            comp = extracted_comp

    return {
        "title": title,
        "company": comp,
        "source": source,
        "category": category,
        "location": location,
        "modality": modality,
        "salary_min": sal_min,
        "salary_max": sal_max,
        "salary_raw": sal_raw,
        "phone": phone or "",
        "whatsapp_url": wa_url or "",
        "description": text[:2000],
        "url": "",
        "status": "Pendiente"
    }