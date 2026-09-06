import os
import sys
import json
import webbrowser
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename

import config.settings as settings
import core.database as db
import core.data_extractor as extractor
import core.notifier_whatsapp as notifier
from core.whatsapp_bot import WhatsAppBot

# Scraper imports
from core.occ_bot import OCCBot
from core.facebook_scraper import FacebookScraper
from core.linkedin_scraper import LinkedInScraper
from core.computrabajo_scraper import CompuTrabajoScraper
from core.glassdoor_scraper import GlassdoorScraper
from core.jobrapido_scraper import JobrapidoScraper
from core.jobleads_scraper import JobLeadsScraper
from core.jobsora_scraper import JobsoraScraper

app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent / "templates"),
    static_folder=str(Path(__file__).parent / "static")
)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file upload

bot_instance = WhatsAppBot()

# Initialize DB on start
db.init_db()


# -------------------------------------------------------------
# Frontend Routes
# -------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -------------------------------------------------------------
# API: Dashboard & KPIs
# -------------------------------------------------------------
@app.route("/api/stats", methods=["GET"])
def get_stats():
    try:
        gen_stats = db.get_stats()
        app_stats = db.get_application_stats()
        return jsonify({
            "success": True,
            "general": gen_stats,
            "applications": app_stats
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------------------------------------------------
# API: Jobs & Quotations
# -------------------------------------------------------------
@app.route("/api/jobs", methods=["GET"])
def list_jobs():
    try:
        category = request.args.get("category")
        source = request.args.get("source")
        status = request.args.get("status")
        modality = request.args.get("modality")
        location = request.args.get("location")
        search_query = request.args.get("search_query")
        has_phone_only = request.args.get("has_phone_only", "false").lower() in ("true", "1", "yes")

        jobs = db.get_jobs(
            category=category if category and category != "Todas" else None,
            source=source if source and source != "Todas" else None,
            status=status if status and status != "Todos" else None,
            modality=modality if modality and modality != "Todas" else None,
            location=location if location and location.strip() else None,
            search_query=search_query if search_query and search_query.strip() else None,
            has_phone_only=has_phone_only,
            order_by="id DESC"
        )

        # Enhance each job with wa.me link if phone exists
        enhanced_jobs = []
        for j in jobs:
            j_dict = dict(j)
            phone = j_dict.get("phone") or ""
            wa_url = j_dict.get("whatsapp_url") or ""
            if not wa_url and phone:
                wa_url = notifier.generate_whatsapp_link(
                    phone,
                    j_dict.get("title", ""),
                    j_dict.get("company", ""),
                    category=j_dict.get("category", "")
                )
            j_dict["whatsapp_url"] = wa_url
            enhanced_jobs.append(j_dict)

        return jsonify({"success": True, "count": len(enhanced_jobs), "jobs": enhanced_jobs})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/jobs/<int:job_id>", methods=["GET"])
def get_job(job_id: int):
    try:
        job = db.get_job_by_id(job_id)
        if not job:
            return jsonify({"success": False, "error": "Vacante no encontrada"}), 404
        return jsonify({"success": True, "job": job})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/jobs/<int:job_id>/status", methods=["POST"])
def update_status(job_id: int):
    try:
        data = request.get_json() or {}
        new_status = data.get("status")
        notes = data.get("notes")
        if not new_status:
            return jsonify({"success": False, "error": "status es requerido"}), 400

        ok = db.update_job_status(job_id, new_status, notes=notes)
        return jsonify({"success": ok, "job_id": job_id, "new_status": new_status})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/jobs/<int:job_id>/notes", methods=["POST"])
def update_notes(job_id: int):
    try:
        data = request.get_json() or {}
        notes = data.get("notes", "")
        ok = db.update_job_notes(job_id, notes)
        return jsonify({"success": ok, "job_id": job_id, "notes": notes})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id: int):
    try:
        ok = db.delete_job(job_id)
        return jsonify({"success": ok, "job_id": job_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/jobs/seed", methods=["POST"])
def seed_jobs():
    try:
        added = db.seed_sample_jobs()
        return jsonify({"success": True, "added": added})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------------------------------------------------
# API: WhatsApp Simulator
# -------------------------------------------------------------
@app.route("/api/whatsapp/simulate", methods=["POST"])
def whatsapp_simulate():
    try:
        data = request.get_json() or {}
        message = data.get("message", "").strip()
        if not message:
            return jsonify({"success": False, "error": "Mensaje no puede estar vacío"}), 400

        reply = bot_instance.process_message(message)
        return jsonify({"success": True, "message": message, "reply": reply})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------------------------------------------------
# API: Scrapers Execution
# -------------------------------------------------------------
@app.route("/api/scrapers/run", methods=["POST"])
def run_scraper():
    try:
        data = request.get_json() or {}
        scraper_name = data.get("scraper", "all").lower()
        cat = data.get("category")
        categories = [cat] if cat and cat != "Todos" else None

        results = {}
        total_new = 0

        scrapers_map = {
            "facebook": (FacebookScraper, "run_scan_and_save"),
            "fb": (FacebookScraper, "run_scan_and_save"),
            "linkedin": (LinkedInScraper, "run_search_and_save"),
            "occ": (OCCBot, "run_search_and_save"),
            "computrabajo": (CompuTrabajoScraper, "run_search_and_save"),
            "glassdoor": (GlassdoorScraper, "run_search_and_save"),
            "jobrapido": (JobrapidoScraper, "run_search_and_save"),
            "jobleads": (JobLeadsScraper, "run_search_and_save"),
            "jobsora": (JobsoraScraper, "run_search_and_save")
        }

        if scraper_name == "all":
            for name, (cls_obj, method_name) in scrapers_map.items():
                if name == "fb":
                    continue
                try:
                    s = cls_obj()
                    method = getattr(s, method_name)
                    if method_name == "run_search_and_save":
                        r = method(categories=categories)
                        saved = r.get("total_new", 0)
                    else:
                        r = method()
                        saved = r.get("new_saved", 0)
                    total_new += saved
                    results[name] = {"success": True, "new": saved}
                except Exception as ex:
                    results[name] = {"success": False, "error": str(ex)}
            return jsonify({
                "success": True,
                "scraper": "all",
                "total_new": total_new,
                "details": results
            })

        elif scraper_name in scrapers_map:
            cls_obj, method_name = scrapers_map[scraper_name]
            s = cls_obj()
            method = getattr(s, method_name)
            if method_name == "run_search_and_save":
                r = method(categories=categories)
                saved = r.get("total_new", 0)
            else:
                r = method()
                saved = r.get("new_saved", 0)

            return jsonify({
                "success": True,
                "scraper": scraper_name,
                "total_new": saved,
                "details": r
            })
        else:
            return jsonify({"success": False, "error": f"Scraper '{scraper_name}' desconocido"}), 400

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------------------------------------------------
# API: Smart Paste Extractor
# -------------------------------------------------------------
@app.route("/api/extract", methods=["POST"])
def extract_job():
    try:
        data = request.get_json() or {}
        text = data.get("text", "").strip()
        source = data.get("source", "Facebook")
        if not text:
            return jsonify({"success": False, "error": "El texto a extraer no puede estar vacío"}), 400

        parsed = extractor.parse_job_post(text, source=source)
        job_id, is_new = db.add_job(parsed)
        return jsonify({
            "success": True,
            "job_id": job_id,
            "is_new": is_new,
            "parsed": parsed
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------------------------------------------------
# API: Profile & Templates
# -------------------------------------------------------------
@app.route("/api/profile", methods=["GET"])
def get_profile():
    try:
        cand_name = os.getenv("CANDIDATE_NAME", "Ingeniero / Contratista Eléctrico")
        cand_phone = getattr(settings, "USER_WHATSAPP_PHONE", os.getenv("USER_WHATSAPP_PHONE", "+5255XXXXXXXX"))
        cand_email = getattr(settings, "OCC_EMAIL", os.getenv("OCC_EMAIL", "correo@ejemplo.com"))

        # Check CV
        cv_path_val = getattr(settings, "CV_PATH", str(settings.CV_DIR / "mi_cv.pdf"))
        cv_target_path = Path(cv_path_val)
        cv_exists = cv_target_path.exists()
        cv_info = {
            "exists": cv_exists,
            "filename": cv_target_path.name if cv_exists else None,
            "size_kb": round(cv_target_path.stat().st_size / 1024, 1) if cv_exists else 0
        }

        # Pre-fill templates
        template_application = notifier.generate_whatsapp_message(
            job_title="Instalaciones Eléctricas / Telecomunicaciones",
            company="Empresa / Cliente",
            candidate_name=cand_name,
            category="Ingeniero Eléctrico"
        )

        template_quotation = notifier.generate_quotation_message(
            service_title="Instalación Eléctrica / Tableros / Subestaciones",
            contact_name="Ing. David Sotomayor",
            location="Parque Industrial El Marqués, Querétaro",
            provider_name=cand_name
        )

        return jsonify({
            "success": True,
            "profile": {
                "name": cand_name,
                "phone": cand_phone,
                "email": cand_email
            },
            "cv": cv_info,
            "templates": {
                "application": template_application,
                "quotation": template_quotation
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/profile", methods=["POST"])
def update_profile():
    try:
        data = request.get_json() or {}
        if "name" in data:
            settings.update_env_variable("CANDIDATE_NAME", data["name"].strip())
        if "phone" in data:
            settings.update_env_variable("USER_WHATSAPP_PHONE", data["phone"].strip())
        if "email" in data:
            settings.update_env_variable("OCC_EMAIL", data["email"].strip())

        return jsonify({"success": True, "message": "Perfil actualizado correctamente"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/cv/upload", methods=["POST"])
def upload_cv():
    try:
        if "file" not in request.files:
            return jsonify({"success": False, "error": "No se envió ningún archivo"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"success": False, "error": "Nombre de archivo vacío"}), 400

        filename = secure_filename(file.filename)
        save_path = settings.CV_DIR / filename
        file.save(str(save_path))

        settings.update_env_variable("CV_PATH", str(save_path))
        size_kb = round(save_path.stat().st_size / 1024, 1)

        return jsonify({
            "success": True,
            "filename": filename,
            "size_kb": size_kb
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/cv/download", methods=["GET"])
def download_cv():
    try:
        cv_path_val = getattr(settings, "CV_PATH", str(settings.CV_DIR / "mi_cv.pdf"))
        cv_target_path = Path(cv_path_val)
        if not cv_target_path.exists():
            return jsonify({"success": False, "error": "CV no encontrado"}), 404
        return send_file(str(cv_target_path), as_attachment=True, download_name=cv_target_path.name)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------------------------------------------------
# API: Exports
# -------------------------------------------------------------
@app.route("/api/export/excel", methods=["GET"])
def export_excel():
    try:
        excel_path = db.export_to_excel()
        return send_file(
            excel_path,
            as_attachment=True,
            download_name=f"vacantes_y_cotizaciones_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/export/csv", methods=["GET"])
def export_csv():
    try:
        csv_path = db.export_to_csv()
        return send_file(
            csv_path,
            as_attachment=True,
            download_name=f"vacantes_y_cotizaciones_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mimetype="text/csv"
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# -------------------------------------------------------------
# API: Settings & Keywords
# -------------------------------------------------------------
@app.route("/api/settings", methods=["GET"])
def get_settings():
    try:
        kw_data = settings.get_keywords()
        env_info = {
            "whatsapp_provider": getattr(settings, "WHATSAPP_PROVIDER", "greenapi"),
            "user_whatsapp_phone": getattr(settings, "USER_WHATSAPP_PHONE", ""),
            "greenapi_instance_id": getattr(settings, "GREENAPI_INSTANCE_ID", ""),
            "has_greenapi_token": bool(getattr(settings, "GREENAPI_API_TOKEN", "")),
            "meta_phone_number_id": getattr(settings, "META_PHONE_NUMBER_ID", ""),
            "has_meta_token": bool(getattr(settings, "META_ACCESS_TOKEN", ""))
        }
        return jsonify({"success": True, "settings": env_info, "keywords": kw_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/settings", methods=["POST"])
def save_settings():
    try:
        data = request.get_json() or {}
        if "whatsapp_provider" in data:
            settings.update_env_variable("WHATSAPP_PROVIDER", data["whatsapp_provider"])
        if "user_whatsapp_phone" in data:
            settings.update_env_variable("USER_WHATSAPP_PHONE", data["user_whatsapp_phone"])
        if "greenapi_instance_id" in data:
            settings.update_env_variable("GREENAPI_INSTANCE_ID", data["greenapi_instance_id"])
        if "greenapi_api_token" in data and data["greenapi_api_token"].strip():
            settings.update_env_variable("GREENAPI_API_TOKEN", data["greenapi_api_token"].strip())
        if "meta_phone_number_id" in data:
            settings.update_env_variable("META_PHONE_NUMBER_ID", data["meta_phone_number_id"])
        if "meta_access_token" in data and data["meta_access_token"].strip():
            settings.update_env_variable("META_ACCESS_TOKEN", data["meta_access_token"].strip())

        return jsonify({"success": True, "message": "Configuración guardada correctamente"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


def start_server(host: str = "127.0.0.1", port: int = 8000, open_browser: bool = True):
    """Start the Flask web application."""
    url = f"http://{host}:{port}"
    print("\n" + "=" * 65)
    print(f"  🚀 AutoJob Hunter - Servidor Web Activo (HTML5 + Bootstrap 5)")
    print(f"  🌐 URL Local: {url}")
    print("=" * 65 + "\n")

    if open_browser:
        threading.Timer(1.2, lambda: webbrowser.open_new_tab(url)).start()

    app.run(host=host, port=port, debug=False)


if __name__ == "__main__":
    start_server()
