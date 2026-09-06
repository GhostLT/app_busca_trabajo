import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
import time
import random
import re
from typing import List, Dict, Any, Optional
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import core.database as db
import core.data_extractor as extractor
import core.notifier_whatsapp as notifier
from config.settings import FB_EMAIL, FB_PASSWORD, DATA_DIR


class FacebookScraper:
    """
    Automated real scraper, browser navigator, and text extractor for Facebook:
    - Logs into the user's Facebook account (or uses saved session profile in data/fb_profile).
    - Discovers all groups the user has joined (https://www.facebook.com/groups/joins/).
    - Scrapes posts from each group to find real job openings, contractor requests, and quotations.
    - Extracts position title, contact/company, phone numbers, WhatsApp links, and salaries.
    - Saves all opportunities to jobs.db and provides structured lists.
    """
    TARGET_GROUPS = [
        "Cotizaciones y Trabajos Eléctricos e Instalaciones México",
        "Oficiales Electricistas, Medio Oficiales y Ayudantes Eléctricos México",
        "Servicios Eléctricos, Subestaciones y Obras Eléctricas CDMX / EdoMex",
        "Obras, Remodelaciones y Contratistas Eléctricos Monterrey & Querétaro",
        "Bolsa de Proyectos e Instalaciones Eléctricas Industriales Guadalajara",
        "Bolsa de Empleo Ingenieros de RF y Telecomunicaciones México",
        "Red de Ingenieros Eléctricos, Subestaciones y Potencia México",
        "Bolsa de Trabajo Técnicos Instaladores de Fibra Óptica y Telecomunicaciones México",
        "Técnicos Electricistas e Instalaciones Eléctricas Industriales México",
        "Técnicos en Sistemas, Soporte TI y Redes México"
    ]

    def __init__(self, email: Optional[str] = None, password: Optional[str] = None, profile_dir: Optional[str] = None):
        self.email = email or FB_EMAIL
        self.password = password or FB_PASSWORD
        self.profile_dir = Path(profile_dir) if profile_dir else (DATA_DIR / "fb_profile")
        self.profile_dir.mkdir(parents=True, exist_ok=True)

    def get_driver(self, headless: bool = False) -> webdriver.Chrome:
        """
        Configure and launch Chrome WebDriver with dedicated Facebook profile
        so login sessions, cookies, and tokens persist between executions.
        """
        options = Options()
        if headless:
            options.add_argument("--headless=new")

        profile_path = str(self.profile_dir.resolve())
        options.add_argument(f"--user-data-dir={profile_path}")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        options.add_argument("--lang=es-MX")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        driver = webdriver.Chrome(options=options)
        return driver

    def is_logged_in(self, driver: webdriver.Chrome) -> bool:
        """
        Determine if the user is authenticated in Facebook.
        """
        try:
            curr = driver.current_url.lower()
            if "login" in curr or "checkpoint" in curr or "recover" in curr:
                return False

            # Check if login input fields are present
            email_inputs = driver.find_elements(By.NAME, "email")
            pass_inputs = driver.find_elements(By.NAME, "pass")
            if email_inputs or pass_inputs:
                return False

            # Check if feed, navigation, or profile element exists
            nav_indicators = driver.find_elements(
                By.CSS_SELECTOR,
                "div[role='navigation'], div[role='feed'], svg[aria-label*='perfil'], a[href*='/me'], svg[aria-label*='Cuenta']"
            )
            return len(nav_indicators) > 0 or "facebook.com/groups" in curr or "facebook.com" in curr
        except Exception:
            return False

    def login(self, driver: webdriver.Chrome, wait_timeout: int = 90) -> bool:
        """
        Ensure Facebook is logged in. Attempts automatic login if credentials exist in .env,
        or allows interactive login/2FA in the opened visible browser window.
        """
        print("[Facebook] Navegando a Facebook para verificar sesión...")
        driver.get("https://www.facebook.com")
        time.sleep(4)

        if self.is_logged_in(driver):
            print("✅ [Facebook] Sesión activa verificada.")
            return True

        # Check if real credentials exist in .env
        is_real_creds = (
            self.email and "ejemplo.com" not in self.email and
            self.password and "contraseña" not in self.password
        )

        if is_real_creds:
            print(f"[Facebook] Intentando autenticación automática con cuenta: {self.email}...")
            try:
                email_box = driver.find_element(By.NAME, "email")
                email_box.clear()
                email_box.send_keys(self.email)
                time.sleep(1)

                pass_box = driver.find_element(By.NAME, "pass")
                pass_box.clear()
                pass_box.send_keys(self.password)
                time.sleep(1)

                login_btn = driver.find_element(By.NAME, "login")
                login_btn.click()
                time.sleep(6)
            except Exception as e:
                print(f"[Facebook] Error al enviar formulario de login: {e}")

            if self.is_logged_in(driver):
                print("✅ [Facebook] Inicio de sesión automático completado con éxito.")
                return True

        # Interactive login wait
        print("=" * 70)
        print("⚠️  [Facebook] ATENCIÓN: Se requiere iniciar sesión en Facebook.")
        print("    Por favor ingresa tu correo y contraseña (y código 2FA si aplica)")
        print("    en la ventana de Google Chrome que se abrió en tu pantalla.")
        print(f"    El sistema esperará hasta {wait_timeout} segundos para detectar tu sesión...")
        print("=" * 70)

        start_time = time.time()
        while time.time() - start_time < wait_timeout:
            time.sleep(3)
            if self.is_logged_in(driver):
                print("✅ [Facebook] ¡Sesión iniciada con éxito! Continuando con la extracción...")
                return True

        print("❌ [Facebook] Tiempo de espera agotado sin inicio de sesión confirmado.")
        return False

    def get_my_groups(self, driver: webdriver.Chrome) -> List[Dict[str, str]]:
        """
        Extract the complete list of groups the user belongs to from https://www.facebook.com/groups/joins/.
        """
        print("[Facebook] Obteniendo lista de grupos a los que perteneces (https://www.facebook.com/groups/joins/)...")
        driver.get("https://www.facebook.com/groups/joins/")
        time.sleep(5)

        # Scroll down smoothly to load all joined groups
        for _ in range(4):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        groups: List[Dict[str, str]] = []
        seen_urls = set()

        # Find all link elements
        links = driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            try:
                href = link.get_attribute("href") or ""
                if "/groups/" in href:
                    clean_url = href.split("?")[0].rstrip("/")
                    if clean_url in seen_urls:
                        continue

                    # Ignore administrative or system Facebook group paths
                    ignore_slugs = ["/groups/feed", "/groups/joins", "/groups/discover", "/groups/create", "/groups/categories"]
                    if any(clean_url.endswith(slug) or slug in clean_url for slug in ignore_slugs):
                        continue

                    # Extract group display name
                    name = link.text.strip()
                    if not name:
                        name = link.get_attribute("title") or link.get_attribute("aria-label") or ""

                    # Clean badges or secondary subtitles
                    if "\n" in name:
                        name = name.split("\n")[0].strip()

                    name_clean = name.strip()
                    if len(name_clean) >= 3 and not name_clean.lower().startswith("ver más") and not name_clean.lower().startswith("unirse"):
                        seen_urls.add(clean_url)
                        group_id = clean_url.split("/groups/")[-1].replace("/", "")
                        groups.append({
                            "name": name_clean,
                            "url": clean_url,
                            "id": group_id
                        })
            except Exception:
                continue

        print(f"✅ [Facebook] Se detectaron {len(groups)} grupos en tu cuenta.")
        return groups

    def scrape_group_posts(
        self,
        driver: webdriver.Chrome,
        group_url: str,
        group_name: str,
        max_scrolls: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Enter a specific Facebook group, scroll its feed, and extract real job opportunities and contacts.
        """
        print(f"[Facebook] Escaneando publicaciones en: '{group_name}' ({group_url})...")
        driver.get(group_url)
        time.sleep(4)

        for _ in range(max_scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.5)

        extracted_jobs: List[Dict[str, Any]] = []
        seen_hashes = set()

        # Target post elements
        post_elements = driver.find_elements(By.CSS_SELECTOR, "div[role='article'], div[role='feed'] > div, div.x1y1aw1k")

        for elem in post_elements:
            try:
                text = elem.text.strip()
                if not text or len(text) < 30:
                    continue

                h = hash(text[:120])
                if h in seen_hashes:
                    continue
                seen_hashes.add(h)

                lower_text = text.lower()
                # Keywords indicating a hiring request, job opening, or quotation opportunity
                hiring_keywords = [
                    "solicito", "se busca", "vacante", "contrataci", "urgente",
                    "oficial", "ayudante", "electricista", "instalaci", "cotiza",
                    "presupuesto", "obra", "sueldo", "pago", "ingeniero", "técnico",
                    "tecnico", "telecom", "fibra", "sistemas", "redes", "mantenimiento",
                    "interesados", "manda whatsapp", "comunicarse", "envia cv"
                ]

                if not any(k in lower_text for k in hiring_keywords):
                    continue

                # Parse post with smart extractor
                parsed = extractor.parse_job_post(
                    text=text,
                    source="Facebook",
                    company=group_name
                )

                # Locate post link if available
                post_links = elem.find_elements(By.CSS_SELECTOR, "a[href*='/posts/'], a[href*='/permalink/'], a[href*='multi_permalinks']")
                if post_links:
                    parsed["url"] = post_links[0].get_attribute("href") or group_url
                else:
                    parsed["url"] = group_url

                # Save to local database
                job_id, is_new = db.add_job(parsed)
                saved_job = db.get_job_by_id(job_id)

                if saved_job:
                    extracted_jobs.append(saved_job)
            except Exception:
                continue

        print(f"  -> Encontradas {len(extracted_jobs)} oportunidades en '{group_name}'.")
        return extracted_jobs

    def run_live_account_extraction(
        self,
        max_groups: int = 15,
        max_posts_per_group: int = 10,
        headless: bool = False
    ) -> Dict[str, Any]:
        """
        Full end-to-end execution:
        1. Opens browser with persistent session.
        2. Verifies / performs login.
        3. Retrieves the user's groups.
        4. Extracts jobs and contacts from each group.
        5. Saves to database and returns organized report.
        """
        driver = None
        try:
            driver = self.get_driver(headless=headless)
            logged_in = self.login(driver)

            if not logged_in:
                return {
                    "success": False,
                    "error": "No se pudo iniciar sesión en Facebook. Por favor ejecuta el escaneo nuevamente e inicia sesión en la ventana del navegador.",
                    "groups": [],
                    "jobs": [],
                    "jobs_by_group": {}
                }

            groups = self.get_my_groups(driver)
            all_jobs: List[Dict[str, Any]] = []
            jobs_by_group: Dict[str, List[Dict[str, Any]]] = {}

            # Process user groups
            target_groups = groups[:max_groups]
            for g in target_groups:
                jobs = self.scrape_group_posts(
                    driver=driver,
                    group_url=g["url"],
                    group_name=g["name"],
                    max_scrolls=3
                )
                jobs_by_group[g["name"]] = jobs
                all_jobs.extend(jobs)

            return {
                "success": True,
                "total_groups": len(groups),
                "groups": groups,
                "scanned_groups_count": len(target_groups),
                "total_jobs_found": len(all_jobs),
                "jobs": all_jobs,
                "jobs_by_group": jobs_by_group,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "groups": [],
                "jobs": [],
                "jobs_by_group": {}
            }
        finally:
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass

    def parse_and_save_post(
        self,
        post_text: str,
        group_name: str = "Facebook Grupos de Empleo",
        custom_title: Optional[str] = None,
        contact_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Parse unstructured Facebook text, extract metadata and save to DB.
        """
        parsed = extractor.parse_job_post(
            text=post_text,
            source="Facebook",
            fallback_title=custom_title,
            company=contact_name or group_name
        )

        job_id, is_new = db.add_job(parsed)
        saved_job = db.get_job_by_id(job_id)

        notification = None
        if saved_job and saved_job.get("phone"):
            notification = notifier.notify_new_match(saved_job)

        return {
            "success": True,
            "job_id": job_id,
            "is_new": is_new,
            "job_data": saved_job,
            "notification": notification
        }

    def run_scan_and_save(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        High-level runner invoked by CLI or API.
        Attempts live account extraction if session/credentials available,
        or provides structured extraction.
        """
        res = self.run_live_account_extraction(max_groups=10, headless=False)
        if res.get("success"):
            return {
                "success": True,
                "total_found": res["total_jobs_found"],
                "new_saved": res["total_jobs_found"],
                "groups": res["groups"],
                "jobs_by_group": res["jobs_by_group"],
                "timestamp": res["timestamp"]
            }
        return res


if __name__ == "__main__":
    scraper = FacebookScraper()
    print("Iniciando conexión con cuenta de Facebook y escaneo de grupos...")
    result = scraper.run_live_account_extraction(max_groups=10, headless=False)
    if result.get("success"):
        print(f"\n[OK] Se encontraron {result['total_groups']} grupos en la cuenta.")
        print(f"[OK] Total de vacantes y cotizaciones extraídas: {result['total_jobs_found']}")
        for g_name, j_list in result.get("jobs_by_group", {}).items():
            print(f"\n--- {g_name} ({len(j_list)} vacantes) ---")
            for j in j_list:
                print(f"  • {j.get('title')} | Contacto: {j.get('company')} | Tel: {j.get('phone')} | WhatsApp: {j.get('whatsapp_url')}")
    else:
        print(f"[ERROR] {result.get('error')}")