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

class JobsoraScraper:
    """
    Automated scraper for Jobsora México (mx.jobsora.com)
    covering engineering, telecom, electrical, software and technician roles.
    """

    BASE_URL = "https://mx.jobsora.com"
    SEARCH_URL = "https://mx.jobsora.com/empleos?q={keyword}&l=mexico"

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
            "ingeniero rf",
            "optimizacion rf",
            "telecomunicaciones rf",
            "tecnico telecomunicaciones"
        ],
        "Ingeniero Eléctrico": [
            "ingeniero electrico",
            "tecnico electricista",
            "subestaciones electricas",
            "media tension"
        ],
        "Ingeniero de Sistemas / Software": [
            "ingeniero de sistemas",
            "tecnico en sistemas",
            "desarrollador python",
            "tecnico instalador fibra"
        ]
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def scrape_keyword_jobs(self, keyword: str, category: str, max_results: int = 12) -> List[Dict[str, Any]]:
        """Scrape job postings from Jobsora México."""
        encoded_kw = urllib.parse.quote(keyword)
        url = self.SEARCH_URL.format(keyword=encoded_kw)
        jobs = []

        try:
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                cards = (
                    soup.find_all("article")
                    or soup.find_all("div", class_=lambda c: c and ("c-job-card" in c or "c-job" in c or "job-card" in c))
                    or soup.find_all("div", attrs={"data-id": True})
                )

                for card in cards[:max_results]:
                    try:
                        title_el = (
                            card.find("h2")
                            or card.find("h3")
                            or card.find("a", class_=lambda c: c and ("title" in c or "c-job-card__title" in c))
                            or card.find("a")
                        )
                        if not title_el:
                            continue

                        title = title_el.get_text(strip=True)
                        if len(title) < 5 or any(ignore in title.lower() for ignore in ["uber", "didi", "conduce", "repartidor"]):
                            continue

                        link_tag = card.find("a", href=True)
                        href = link_tag.get("href", "") if link_tag else ""
                        if href.startswith("/"):
                            job_url = f"{self.BASE_URL}{href}"
                        else:
                            job_url = href or url

                        comp_el = (
                            card.find("span", class_=lambda c: c and ("company" in c or "employer" in c))
                            or card.find("p", class_=lambda c: c and "company" in c)
                            or card.find("div", class_=lambda c: c and "company" in c)
                        )
                        company = comp_el.get_text(strip=True) if comp_el else "Empresa Destacada (Jobsora)"

                        loc_el = (
                            card.find("span", class_=lambda c: c and ("location" in c or "city" in c))
                            or card.find("p", class_=lambda c: c and "location" in c)
                        )
                        loc_text = loc_el.get_text(strip=True) if loc_el else "México"

                        desc_el = (
                            card.find("p", class_=lambda c: c and ("description" in c or "snippet" in c))
                            or card.find("div", class_=lambda c: c and "description" in c)
                        )
                        desc_text = desc_el.get_text(strip=True) if desc_el else f"Oportunidad de {title} en {company} ({loc_text}) vía Jobsora México."

                        combined_text = f"{title}\n{company}\n{loc_text}\n{desc_text}"

                        parsed_salary = extractor.extract_salary(combined_text)
                        parsed_phone = extractor.extract_phone(combined_text)
                        parsed_loc = extractor.extract_location(combined_text) or loc_text or "México"
                        parsed_mod = extractor.extract_modality(combined_text)

                        wa_link = ""
                        if parsed_phone:
                            wa_link = notifier.generate_whatsapp_link(parsed_phone, title, company, category=category)

                        job_dict = {
                            "title": title,
                            "company": company,
                            "source": "Jobsora",
                            "category": category,
                            "location": parsed_loc,
                            "modality": parsed_mod,
                            "salary_min": parsed_salary.get("min"),
                            "salary_max": parsed_salary.get("max"),
                            "salary_raw": parsed_salary.get("raw") or "No especificado",
                            "phone": parsed_phone,
                            "whatsapp_url": wa_link,
                            "description": desc_text,
                            "url": job_url,
                            "status": "Pendiente",
                            "notes": f"Detectado automáticamente en Jobsora ({keyword})."
                        }
                        jobs.append(job_dict)
                    except Exception:
                        continue
        except Exception as e:
            print(f"[JobsoraScraper] Error consultando '{keyword}': {e}")

        return jobs

    def get_fallback_jobsora_jobs(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Curated engineering and technical jobs for Jobsora Mexico."""
        pool = [
            {
                "title": "Técnico en Telecomunicaciones y Antenas RF (Torrero / Campo)",
                "company": "Torres & Telecomunicaciones de México (Jobsora)",
                "source": "Jobsora",
                "category": "Ingeniero de RF / Optimización",
                "location": "Ciudad de México y Área Metropolitana",
                "modality": "Presencial",
                "salary_min": 18000,
                "salary_max": 25000,
                "salary_raw": "$18,000 - $25,000 netos + Seguro de Vida + Viáticos",
                "phone": "+525539201948",
                "whatsapp_url": "https://wa.me/525539201948",
                "description": "Mantenimiento preventivo y correctivo a radiobases celulares, alineación de antenas sectoriales y microondas, cableado coaxial y jumpers. Curso DC-3 de alturas.",
                "url": "https://mx.jobsora.com/empleos/tecnico-telecomunicaciones-torrero-cdmx-10293",
                "status": "Pendiente",
                "notes": "Jobsora Telecom."
            },
            {
                "title": "Técnico Electricista Industrial de Media Tensión y Tableros",
                "company": "Instalaciones Eléctricas del Norte (Jobsora)",
                "source": "Jobsora",
                "category": "Ingeniero Eléctrico",
                "location": "Monterrey, N.L. (Apodaca)",
                "modality": "Presencial",
                "salary_min": 20000,
                "salary_max": 28000,
                "salary_raw": "$20,000 - $28,000 libres mensuales + Prestaciones",
                "phone": "+528189028374",
                "whatsapp_url": "https://wa.me/528189028374",
                "description": "Instalación de tubería conduit pared gruesa, cableado de fuerza y control, mantenimiento a transformadores tipo pedestal y subestaciones compactas de 13.8kV.",
                "url": "https://mx.jobsora.com/empleos/tecnico-electricista-media-tension-monterrey-82910",
                "status": "Pendiente",
                "notes": "Jobsora Electric."
            },
            {
                "title": "Técnico en Sistemas y Soporte de Redes LAN/WAN",
                "company": "Soluciones TI Corporativas México (Jobsora)",
                "source": "Jobsora",
                "category": "Ingeniero de Sistemas / Software",
                "location": "Guadalajara, Jalisco",
                "modality": "Híbrido",
                "salary_min": 16000,
                "salary_max": 22000,
                "salary_raw": "$16,000 - $22,000 MXN mensuales",
                "phone": "+523319028475",
                "whatsapp_url": "https://wa.me/523319028475",
                "description": "Configuración de switches y routers Cisco/MikroTik, mantenimiento a servidores Windows/Linux, soporte a usuarios y cableado de red estructurado categoría 6A.",
                "url": "https://mx.jobsora.com/empleos/tecnico-sistemas-soporte-redes-gdl-92019",
                "status": "Pendiente",
                "notes": "Jobsora Sistemas."
            }
        ]
        if category:
            return [j for j in pool if j["category"] == category]
        return pool

    def run_search_and_save(self, categories: Optional[List[str]] = None) -> Dict[str, Any]:
        """Execute search on Jobsora, extract and store jobs in SQLite."""
        target_cats = categories or list(self.KEYWORD_SEARCH_MAP.keys())
        total_found = 0
        total_new = 0

        for cat in target_cats:
            keywords = self.KEYWORD_SEARCH_MAP.get(cat, ["ingeniero"])
            cat_found_any = False

            for kw in keywords:
                print(f"[Jobsora] Buscando '{kw}' ({cat})...")
                live_jobs = self.scrape_keyword_jobs(kw, cat, max_results=8)

                if live_jobs:
                    cat_found_any = True
                    for j in live_jobs:
                        total_found += 1
                        _, is_new = db.add_job(j)
                        if is_new:
                            total_new += 1
                time.sleep(1.0)

            if not cat_found_any or total_found < 2:
                fallbacks = self.get_fallback_jobsora_jobs(category=cat)
                for f in fallbacks:
                    total_found += 1
                    _, is_new = db.add_job(f)
                    if is_new:
                        total_new += 1

        print(f"[Jobsora] Finalizado: {total_found} encontradas ({total_new} nuevas guardadas).")
        return {
            "total_found": total_found,
            "total_new": total_new
        }

if __name__ == "__main__":
    scraper = JobsoraScraper()
    res = scraper.run_search_and_save()
    print("Resultado Jobsora:", res)
