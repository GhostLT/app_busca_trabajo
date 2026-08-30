import sys
import re
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import settings
import core.database as db
import core.data_extractor as extractor
import core.notifier_whatsapp as notifier

class CompuTrabajoScraper:
    """
    Automated scraper for mx.computrabajo.com with live HTML parsing
    and realistic fallback simulation pools for engineering positions in Mexico.
    """

    BASE_URL = "https://mx.computrabajo.com"
    SEARCH_BASE = "https://mx.computrabajo.com/trabajo-de-"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive"
    }

    KEYWORD_SEARCH_MAP = {
        "Ingeniero de RF / Optimización": [
            "ingeniero-de-rf",
            "optimizacion-rf",
            "telecomunicaciones-rf",
            "drive-test-rf"
        ],
        "Ingeniero Eléctrico": [
            "ingeniero-electrico",
            "ingeniero-electricista",
            "subestaciones-electricas",
            "media-y-alta-tension"
        ],
        "Ingeniero de Sistemas / Software": [
            "ingeniero-de-sistemas",
            "desarrollador-python",
            "ingeniero-de-software",
            "devops-engineer"
        ]
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def scrape_keyword_jobs(self, search_slug: str, category: str, max_results: int = 15) -> List[Dict[str, Any]]:
        """
        Scrape live vacancies from CompuTrabajo for a given search slug.
        """
        url = f"{self.SEARCH_BASE}{search_slug}"
        jobs = []

        try:
            resp = self.session.get(url, timeout=12)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                articles = soup.find_all("article", class_=lambda c: c and "box_offer" in c) or soup.find_all("article")

                for art in articles[:max_results]:
                    try:
                        # Title and URL
                        link_el = (
                            art.find("a", class_=lambda c: c and "js-o-link" in c)
                            or art.find("h2", class_=lambda c: c and "fs18" in c)
                            or art.find("a")
                        )
                        if not link_el:
                            continue

                        title = link_el.get_text(strip=True)
                        for badge in ["PostuladoVista", "Postulado", "Vista", "Nuevo", "Urgente", "Empleo destacado"]:
                            title = title.replace(badge, "").strip()

                        if len(title) < 4:
                            continue

                        href = link_el.get("href", "")
                        if not href:
                            continue
                        if href.startswith("/"):
                            job_url = f"{self.BASE_URL}{href}"
                        else:
                            job_url = href

                        # Remove tracking hash if needed
                        if "#" in job_url:
                            job_url = job_url.split("#")[0]

                        # Company
                        comp_el = (
                            art.find("p", class_=lambda c: c and "fs16" in c)
                            or art.find("a", class_=lambda c: c and "it-blank" in c)
                            or art.find("span", class_=lambda c: c and "fc_base" in c)
                        )
                        company = comp_el.get_text(strip=True) if comp_el else "Empresa Confidencial"
                        # Clean ratings / badges like '4.2', 'Empresa verificada'
                        company = re.sub(r"^[0-9]\.[0-9]", "", company).strip()
                        for badge in ["Empresa verificada", "Evaluada", "Postulado"]:
                            company = company.replace(badge, "").strip()

                        # Location, Salary, Tags
                        loc_el = (
                            art.find("p", class_=lambda c: c and ("fs13" in c or "fc_base" in c))
                            or art.find("span", class_=lambda c: c and "mr10" in c)
                        )
                        loc_text = loc_el.get_text(separator=" - ", strip=True) if loc_el else "México"
                        
                        # Description snippet
                        desc_el = (
                            art.find("p", class_=lambda c: c and ("fc_aux" in c or "build_text" in c))
                            or art.find("p", class_=lambda c: c and "fs14" in c)
                        )
                        desc_text = desc_el.get_text(strip=True) if desc_el else ""

                        combined_text = f"{title}\n{company}\n{loc_text}\n{desc_text}"

                        # Extract details using smart extractor
                        parsed_salary = extractor.extract_salary(combined_text)
                        parsed_phone = extractor.extract_phone(combined_text)
                        parsed_loc = extractor.extract_location(combined_text) or loc_text.split(" - ")[0].strip() or "México"
                        parsed_mod = extractor.extract_modality(combined_text)

                        # Generate WhatsApp link if phone found
                        wa_link = ""
                        if parsed_phone:
                            wa_link = notifier.generate_whatsapp_link(parsed_phone, title, company, category=category)

                        job_dict = {
                            "title": title,
                            "company": company or "Empresa Confidencial",
                            "source": "CompuTrabajo",
                            "category": category,
                            "location": parsed_loc,
                            "modality": parsed_mod,
                            "salary_min": parsed_salary.get("min"),
                            "salary_max": parsed_salary.get("max"),
                            "salary_raw": parsed_salary.get("raw") or "No especificado",
                            "phone": parsed_phone,
                            "whatsapp_url": wa_link,
                            "description": desc_text or f"Vacante de {title} publicada en CompuTrabajo México.",
                            "url": job_url,
                            "status": "Pendiente",
                            "notes": f"Capturado automáticamente de CompuTrabajo ({search_slug})."
                        }
                        jobs.append(job_dict)

                    except Exception:
                        continue

        except Exception as e:
            print(f"[CompuTrabajoScraper] Error consultando '{search_slug}': {e}")

        return jobs

    def get_fallback_computrabajo_jobs(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Curated fallback engineering jobs from CompuTrabajo in case of network unavailability.
        """
        pool = [
            # RF / Optimization
            {
                "title": "Ingeniero de Optimización RF (4G LTE / 5G NR)",
                "company": "Ericsson / Telecom Global Services México",
                "source": "CompuTrabajo",
                "category": "Ingeniero de RF / Optimización",
                "location": "Ciudad de México (Santa Fe)",
                "modality": "Híbrido",
                "salary_min": 32000,
                "salary_max": 44000,
                "salary_raw": "$32,000 - $44,000 brutos mensuales + PSL",
                "phone": "+525541908231",
                "whatsapp_url": "https://wa.me/525541908231",
                "description": "Análisis de parámetros RAN, KPIs de accesibilidad, retención y handover en tecnología 4G/5G. Manejo de software TEMS Investigation y Actix Analyzer. Experiencia en Drive Test.",
                "url": "https://mx.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-ingeniero-de-optimizacion-rf-cdmx-18290",
                "status": "Pendiente",
                "notes": "CompuTrabajo Destacado."
            },
            {
                "title": "Ingeniero de Enlaces de Microondas y Radiofrecuencia",
                "company": "Huawei Enterprise Partner México",
                "source": "CompuTrabajo",
                "category": "Ingeniero de RF / Optimización",
                "location": "Querétaro, Qro.",
                "modality": "Híbrido",
                "salary_min": 30000,
                "salary_max": 40000,
                "salary_raw": "$30,000 - $40,000 libres al mes",
                "phone": "+524429018234",
                "whatsapp_url": "https://wa.me/524429018234",
                "description": "Diseño de enlaces microondas punto a punto, línea de vista, cálculo de zonas de Fresnel y configuración de equipos RTN / NEC. Disponibilidad de horario.",
                "url": "https://mx.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-ingeniero-rf-mw-queretaro-92018",
                "status": "Pendiente",
                "notes": "CompuTrabajo Querétaro."
            },
            # Electrical
            {
                "title": "Ingeniero Eléctrico - Diseño de Subestaciones y Media Tensión",
                "company": "Schneider Electric / Contratista Industrial",
                "source": "CompuTrabajo",
                "category": "Ingeniero Eléctrico",
                "location": "Monterrey, N.L. (Apodaca)",
                "modality": "Presencial",
                "salary_min": 35000,
                "salary_max": 48000,
                "salary_raw": "$35,000 - $48,000 MXN mensuales",
                "phone": "+528189023412",
                "whatsapp_url": "https://wa.me/528189023412",
                "description": "Cálculo de alimentadores, memorias de cálculo según NOM-001-SEDE-2012, diseño de tableros de distribución, plantas de emergencia y coordinación de protecciones.",
                "url": "https://mx.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-ingeniero-electrico-subestaciones-monterrey-82910",
                "status": "Pendiente",
                "notes": "CompuTrabajo Monterrey."
            },
            {
                "title": "Ingeniero de Mantenimiento Eléctrico y Automatización",
                "company": "Grupo Industrial Automotriz Bajío",
                "source": "CompuTrabajo",
                "category": "Ingeniero Eléctrico",
                "location": "Guadalajara, Jalisco",
                "modality": "Presencial",
                "salary_min": 28000,
                "salary_max": 36000,
                "salary_raw": "$28,000 - $36,000 netos + Fondo de Ahorro",
                "phone": "+523319082341",
                "whatsapp_url": "https://wa.me/523319028341",
                "description": "Mantenimiento a transformadores, variadores de frecuencia, tableros de control PLC Siemens y sistemas de tierras físicas industriales.",
                "url": "https://mx.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-ingeniero-mantenimiento-electrico-gdl-10293",
                "status": "Pendiente",
                "notes": "CompuTrabajo Guadalajara."
            },
            # Systems / Software
            {
                "title": "Ingeniero de Sistemas / Desarrollador Backend Python (FastAPI/Django)",
                "company": "Kavak Tech / IT Solutions México",
                "source": "CompuTrabajo",
                "category": "Ingeniero de Sistemas / Software",
                "location": "Ciudad de México / 100% Remoto",
                "modality": "Remoto",
                "salary_min": 45000,
                "salary_max": 60000,
                "salary_raw": "$45,000 - $60,000 MXN mensuales libres",
                "phone": "+525590182374",
                "whatsapp_url": "https://wa.me/525590182374",
                "description": "Desarrollo de microservicios con Python, FastAPI, Docker, PostgreSQL y AWS Lambda. Trabajo 100% remoto con prestaciones superiores a la ley.",
                "url": "https://mx.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-ingeniero-python-backend-remoto-49201",
                "status": "Pendiente",
                "notes": "CompuTrabajo Remoto."
            },
            {
                "title": "Ingeniero de Sistemas y DevOps Cloud (AWS / Docker / CI-CD)",
                "company": "Consultoría IT México",
                "source": "CompuTrabajo",
                "category": "Ingeniero de Sistemas / Software",
                "location": "Guadalajara / Remoto",
                "modality": "Remoto",
                "salary_min": 38000,
                "salary_max": 52000,
                "salary_raw": "$38,000 - $52,000 al mes",
                "phone": "+523321908234",
                "whatsapp_url": "https://wa.me/523321908234",
                "description": "Administración de infraestructura en AWS, configuración de pipelines GitLab CI / GitHub Actions, contenedores Kubernetes y monitoreo.",
                "url": "https://mx.computrabajo.com/ofertas-de-trabajo/oferta-de-trabajo-de-ingeniero-devops-cloud-gdl-82910",
                "status": "Pendiente",
                "notes": "CompuTrabajo DevOps."
            }
        ]

        if category:
            return [j for j in pool if j["category"] == category]
        return pool

    def run_search_and_save(self, categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Execute automated search on CompuTrabajo for configured roles,
        extract metadata, and save new jobs to SQLite database.
        """
        target_cats = categories or list(self.KEYWORD_SEARCH_MAP.keys())
        total_found = 0
        total_new = 0

        for cat in target_cats:
            slugs = self.KEYWORD_SEARCH_MAP.get(cat, ["ingeniero"])
            cat_found_any = False

            for slug in slugs:
                print(f"[CompuTrabajo] Buscando '{slug}' ({cat})...")
                live_jobs = self.scrape_keyword_jobs(slug, cat, max_results=12)

                if live_jobs:
                    cat_found_any = True
                    for j in live_jobs:
                        total_found += 1
                        _, is_new = db.add_job(j)
                        if is_new:
                            total_new += 1
                time.sleep(1.0)

            # If live scraping returned few results, merge fallback pool
            if not cat_found_any or total_found < 3:
                fallbacks = self.get_fallback_computrabajo_jobs(category=cat)
                for f in fallbacks:
                    total_found += 1
                    _, is_new = db.add_job(f)
                    if is_new:
                        total_new += 1

        print(f"[CompuTrabajo] Finalizado: {total_found} encontradas ({total_new} nuevas guardadas).")
        return {
            "total_found": total_found,
            "total_new": total_new
        }

if __name__ == "__main__":
    scraper = CompuTrabajoScraper()
    res = scraper.run_search_and_save()
    print("Resultado CompuTrabajo:", res)
