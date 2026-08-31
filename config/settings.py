import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
CV_DIR = DATA_DIR / "cv"
EXPORTS_DIR = DATA_DIR / "exports"
DB_PATH = DATA_DIR / "jobs.db"
KEYWORDS_PATH = CONFIG_DIR / "keywords.json"
ENV_PATH = BASE_DIR / ".env"

# Ensure runtime directories exist
CV_DIR.mkdir(parents=True, exist_ok=True)
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
load_dotenv(dotenv_path=ENV_PATH)

# OCC Credentials
OCC_EMAIL = os.getenv("OCC_EMAIL", "")
OCC_PASSWORD = os.getenv("OCC_PASSWORD", "")

# Facebook Credentials
FB_EMAIL = os.getenv("FB_EMAIL", "")
FB_PASSWORD = os.getenv("FB_PASSWORD", "")

# LinkedIn Credentials
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL", "")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD", "")

# CompuTrabajo Credentials
COMPUTRABAJO_EMAIL = os.getenv("COMPUTRABAJO_EMAIL", "")
COMPUTRABAJO_PASSWORD = os.getenv("COMPUTRABAJO_PASSWORD", "")

# Glassdoor Credentials
GLASSDOOR_EMAIL = os.getenv("GLASSDOOR_EMAIL", "")
GLASSDOOR_PASSWORD = os.getenv("GLASSDOOR_PASSWORD", "")

# Jobrapido Credentials
JOBRAPIDO_EMAIL = os.getenv("JOBRAPIDO_EMAIL", "")
JOBRAPIDO_PASSWORD = os.getenv("JOBRAPIDO_PASSWORD", "")

# JobLeads Credentials
JOBLEADS_EMAIL = os.getenv("JOBLEADS_EMAIL", "")
JOBLEADS_PASSWORD = os.getenv("JOBLEADS_PASSWORD", "")

# Jobsora Credentials
JOBSORA_EMAIL = os.getenv("JOBSORA_EMAIL", "")
JOBSORA_PASSWORD = os.getenv("JOBSORA_PASSWORD", "")

# WhatsApp Notification Settings
USER_WHATSAPP_PHONE = os.getenv("USER_WHATSAPP_PHONE", "")
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY", "")

# Candidate Profile and CV
CV_PATH = os.getenv("CV_PATH", str(CV_DIR / "mi_cv.pdf"))
TARGET_ROLES_RAW = os.getenv(
    "TARGET_ROLES",
    "Ingeniero Eléctrico, Oficial Eléctrico, Medio Oficial Eléctrico, Ayudante Electricista, Técnico Electricista, Ingeniero de RF, Ingeniero de Sistemas, Técnico Instalador de Fibra, Técnico en Telecomunicaciones"
)
TARGET_ROLES = [r.strip() for r in TARGET_ROLES_RAW.split(",") if r.strip()]

def get_keywords() -> dict:
    """Load search keywords categorized by specialty."""
    if KEYWORDS_PATH.exists():
        try:
            with open(KEYWORDS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_keywords(data: dict) -> bool:
    """Save keywords to configuration file."""
    try:
        with open(KEYWORDS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def update_env_variable(key: str, value: str):
    """Update or append an environment variable in .env file."""
    lines = []
    found = False
    if ENV_PATH.exists():
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            found = True
        else:
            new_lines.append(line)

    if not found:
        new_lines.append(f"{key}={value}\n")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    os.environ[key] = value