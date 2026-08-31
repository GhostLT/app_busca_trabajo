import sys
import argparse
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

import core.database as db
from core.occ_bot import OCCBot
from core.facebook_scraper import FacebookScraper
from core.linkedin_scraper import LinkedInScraper
from core.computrabajo_scraper import CompuTrabajoScraper
from core.glassdoor_scraper import GlassdoorScraper
from core.jobrapido_scraper import JobrapidoScraper
from core.jobleads_scraper import JobLeadsScraper
from core.jobsora_scraper import JobsoraScraper

BANNER = """
=============================================================================
  AUTOJOB HUNTER & TRACKER (LINKEDIN, OCC, COMPUTRABAJO, GLASSDOOR, ETC.)
  Especialidades: RF / Telecom, Eléctrica, Sistemas / Software & Técnicos
=============================================================================
"""

def print_stats():
    stats = db.get_stats()
    app_stats = db.get_application_stats()
    print("\n[+] ESTADÍSTICAS ACTUALES DE VACANTES:")
    print(f"  • Total Vacantes:         {stats['total_jobs']}")
    print(f"  • Postuladas:             {app_stats['applied_count']}")
    print(f"  • Postuladas Hoy:         {app_stats['today_count']}")
    print(f"  • En Entrevista:          {app_stats['interview_count']} (Éxito: {app_stats['conversion_rate']}%)")
    print(f"  • Pendientes de Contacto: {stats['pending_count']}")
    print(f"  • Con Teléfono/WhatsApp:  {stats['with_phone_count']}")
    print(f"  • Salario Promedio:       ${stats['avg_salary']:,.2f} MXN")
    print("\n[+] Por Especialidad:")
    for cat, count in stats["by_category"].items():
        print(f"    - {cat}: {count}")
    print("\n[+] Por Fuente / Plataforma:")
    for src, count in stats["by_source"].items():
        print(f"    - {src}: {count}")
    print("=" * 63 + "\n")

def run_occ():
    print("\n[+] Iniciando búsqueda automática en OCC Mundial...")
    bot = OCCBot()
    res = bot.run_search_and_save()
    print(f"[OK] Búsqueda OCC terminada. Encontradas: {res['total_found']} | Nuevas registradas: {res['total_new']}")
    print_stats()

def run_linkedin():
    print("\n[+] Iniciando búsqueda automática en LinkedIn México...")
    lk = LinkedInScraper()
    res = lk.run_search_and_save()
    print(f"[OK] Búsqueda LinkedIn terminada. Encontradas: {res['total_found']} | Nuevas registradas: {res['total_new']}")
    print_stats()

def run_computrabajo():
    print("\n[+] Iniciando búsqueda automática en CompuTrabajo México...")
    ct = CompuTrabajoScraper()
    res = ct.run_search_and_save()
    print(f"[OK] Búsqueda CompuTrabajo terminada. Encontradas: {res['total_found']} | Nuevas registradas: {res['total_new']}")
    print_stats()

def run_glassdoor():
    print("\n[+] Iniciando búsqueda automática en Glassdoor México...")
    gd = GlassdoorScraper()
    res = gd.run_search_and_save()
    print(f"[OK] Búsqueda Glassdoor terminada. Encontradas: {res['total_found']} | Nuevas registradas: {res['total_new']}")
    print_stats()

def run_jobrapido():
    print("\n[+] Iniciando búsqueda automática en Jobrapido México...")
    jr = JobrapidoScraper()
    res = jr.run_search_and_save()
    print(f"[OK] Búsqueda Jobrapido terminada. Encontradas: {res['total_found']} | Nuevas registradas: {res['total_new']}")
    print_stats()

def run_jobleads():
    print("\n[+] Iniciando búsqueda automática en JobLeads México...")
    jl = JobLeadsScraper()
    res = jl.run_search_and_save()
    print(f"[OK] Búsqueda JobLeads terminada. Encontradas: {res['total_found']} | Nuevas registradas: {res['total_new']}")
    print_stats()

def run_jobsora():
    print("\n[+] Iniciando búsqueda automática en Jobsora México...")
    js = JobsoraScraper()
    res = js.run_search_and_save()
    print(f"[OK] Búsqueda Jobsora terminada. Encontradas: {res['total_found']} | Nuevas registradas: {res['total_new']}")
    print_stats()

def run_fb():
    print("\n[+] Iniciando escaneo de ofertas en grupos de Facebook (Ingeniería y Técnicos)...")
    fb = FacebookScraper()
    res = fb.run_scan_and_save()
    print(f"[OK] Escaneo Facebook terminado. Procesadas: {res['total_found']} | Nuevas registradas: {res['new_saved']}")
    print_stats()

def run_all_scrapers():
    print("\n[⚡] INICIANDO ESCANEO COMPLETO EN TODAS LAS PLATAFORMAS (8 CANALES)...")
    for scraper_func, name in [
        (run_linkedin, "LinkedIn"),
        (run_occ, "OCC Mundial"),
        (run_computrabajo, "CompuTrabajo"),
        (run_glassdoor, "Glassdoor"),
        (run_jobrapido, "Jobrapido"),
        (run_jobleads, "JobLeads"),
        (run_jobsora, "Jobsora"),
        (run_fb, "Facebook")
    ]:
        try:
            scraper_func()
        except Exception as e:
            print(f"[!] Error en {name}: {e}")
    print("\n[✓] ¡ESCANEO GLOBAL DE TODAS LAS PLATAFORMAS FINALIZADO!")

def run_export():
    print("\n[+] Generando reportes de exportación...")
    excel_path = db.export_to_excel()
    csv_path = db.export_to_csv()
    print(f"[OK] Reporte Excel guardado en: {excel_path}")
    print(f"[OK] Reporte CSV guardado en:   {csv_path}\n")

def launch_ui():
    print("\n[+] Iniciando interfaz gráfica Streamlit...")
    app_path = BASE_DIR / "ui" / "app.py"
    subprocess.run(["streamlit", "run", str(app_path)])

def main():
    print(BANNER)
    db.init_db()

    parser = argparse.ArgumentParser(description="AutoJob Hunter & Tracker CLI")
    parser.add_argument("--ui", action="store_true", help="Iniciar el Dashboard visual de Streamlit (por defecto)")
    parser.add_argument("--occ", action="store_true", help="Ejecutar búsqueda en OCC Mundial")
    parser.add_argument("--linkedin", action="store_true", help="Ejecutar búsqueda en LinkedIn")
    parser.add_argument("--computrabajo", "--ct", action="store_true", help="Ejecutar búsqueda en CompuTrabajo")
    parser.add_argument("--glassdoor", "--gd", action="store_true", help="Ejecutar búsqueda en Glassdoor")
    parser.add_argument("--jobrapido", "--jr", action="store_true", help="Ejecutar búsqueda en Jobrapido")
    parser.add_argument("--jobleads", "--jl", action="store_true", help="Ejecutar búsqueda en JobLeads")
    parser.add_argument("--jobsora", "--js", action="store_true", help="Ejecutar búsqueda en Jobsora")
    parser.add_argument("--fb", action="store_true", help="Ejecutar escaneo en Facebook (Ingeniería y Técnicos)")
    parser.add_argument("--all", action="store_true", help="Ejecutar escaneo en TODAS las plataformas simultáneamente")
    parser.add_argument("--stats", action="store_true", help="Ver estadísticas de la base de datos")
    parser.add_argument("--export", action="store_true", help="Exportar vacantes a Excel y CSV")
    parser.add_argument("--seed", action="store_true", help="Cargar vacantes de ejemplo en la base de datos")

    args = parser.parse_args()

    if args.all:
        run_all_scrapers()
    elif args.occ:
        run_occ()
    elif args.linkedin:
        run_linkedin()
    elif args.computrabajo:
        run_computrabajo()
    elif args.glassdoor:
        run_glassdoor()
    elif args.jobrapido:
        run_jobrapido()
    elif args.jobleads:
        run_jobleads()
    elif args.jobsora:
        run_jobsora()
    elif args.fb:
        run_fb()
    elif args.stats:
        print_stats()
    elif args.export:
        run_export()
    elif args.seed:
        added = db.seed_sample_jobs()
        print(f"[OK] Se cargaron {added} vacantes de prueba.")
        print_stats()
    else:
        launch_ui()

if __name__ == "__main__":
    main()