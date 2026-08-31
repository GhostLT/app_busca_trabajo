import sys
import re
import urllib.parse
from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.append(str(Path(__file__).resolve().parent.parent))

from config import settings
import core.database as db
import core.notifier_whatsapp as notifier
from core.facebook_scraper import FacebookScraper
from core.linkedin_scraper import LinkedInScraper
from core.occ_bot import OCCBot
from core.computrabajo_scraper import CompuTrabajoScraper
from core.glassdoor_scraper import GlassdoorScraper
from core.jobrapido_scraper import JobrapidoScraper
from core.jobleads_scraper import JobLeadsScraper
from core.jobsora_scraper import JobsoraScraper

class WhatsAppBot:
    """
    Interactive WhatsApp bot for querying jobs, electrical quotation leads,
    updating vacancy statuses, and triggering remote scrapers via text commands.
    """

    HELP_MENU = """🤖 *AUTOJOB HUNTER - COMANDOS DE WHATSAPP* 🚀

📌 *CONSULTAS Y OPORTUNIDADES:*
• `!resumen` - Ver métricas y rendimiento de hoy (postulaciones/cotizaciones).
• `!cotizaciones` - Ver solicitudes de electricistas, obras y presupuestos.
• `!vacantes` - Ver últimas 5 vacantes encontradas.
• `!vacantes [rol]` - Filtrar (ej: `!vacantes oficial`, `!vacantes cdmx`).
• `!buscar [texto]` - Búsqueda libre (ej: `!buscar queretaro`).
• `!detalle [id]` - Ver ficha técnica completa de una vacante (ej: `!detalle 15`).

⚡ *GESTIÓN DE ESTADO Y ACCIONES:*
• `!contacto [id]` - Marcar como *En Contacto / Postulado* en la base de datos.
• `!cotizado [id]` - Marcar como *En Cotización / Entrevista*.
• `!descartar [id]` - Descartar una vacante/obra.

🔄 *ESCANEO REMOTO EN VIVO:*
• `!escanear fb` - Escanear solicitudes de electricistas en Facebook.
• `!escanear todas` - Rastrear las 8 plataformas simultáneamente.

Escribe cualquier comando para comenzar. ¡Éxito en tus proyectos! 💼"""

    def __init__(self):
        db.init_db()

    def process_message(self, text: str, sender_phone: Optional[str] = None) -> str:
        """
        Main entry point to parse text commands and generate the response message.
        """
        if not text or not text.strip():
            return self.HELP_MENU

        clean_text = text.strip()
        parts = clean_text.split()
        cmd = parts[0].lower()
        args = parts[1:]
        arg_str = " ".join(args).strip()

        # Handle commands with or without prefix '!'
        if cmd in ["!ayuda", "ayuda", "!menu", "menu", "!help", "help", "hola", "inicio"]:
            return self.HELP_MENU

        elif cmd in ["!resumen", "resumen", "!stats", "stats", "!metricas", "metricas"]:
            return self._cmd_summary()

        elif cmd in ["!cotizaciones", "cotizaciones", "!obras", "obras", "!presupuestos", "presupuestos"]:
            return self._cmd_quotations(arg_str)

        elif cmd in ["!vacantes", "vacantes", "!empleos", "empleos"]:
            return self._cmd_vacancies(arg_str)

        elif cmd in ["!buscar", "buscar", "!search", "search"]:
            if not arg_str:
                return "⚠️ Por favor especifica qué deseas buscar. Ejemplo: `!buscar oficial electricista`"
            return self._cmd_search(arg_str)

        elif cmd in ["!detalle", "detalle", "!ver", "ver"]:
            if not args or not args[0].isdigit():
                return "⚠️ Por favor indica el ID numérico de la vacante. Ejemplo: `!detalle 12`"
            return self._cmd_detail(int(args[0]))

        elif cmd in ["!contacto", "contacto", "!aplicar", "aplicar", "!postular", "postular"]:
            if not args or not args[0].isdigit():
                return "⚠️ Por favor indica el ID de la vacante a registrar. Ejemplo: `!contacto 12`"
            return self._cmd_update_status(int(args[0]), "Postulado", "En Contacto / Postulado")

        elif cmd in ["!cotizado", "cotizado", "!entrevista", "entrevista"]:
            if not args or not args[0].isdigit():
                return "⚠️ Por favor indica el ID de la vacante/cotización. Ejemplo: `!cotizado 12`"
            return self._cmd_update_status(int(args[0]), "Entrevista", "En Cotización / Entrevista")

        elif cmd in ["!descartar", "descartar", "!borrar", "borrar"]:
            if not args or not args[0].isdigit():
                return "⚠️ Por favor indica el ID de la vacante a descartar. Ejemplo: `!descartar 12`"
            return self._cmd_delete(int(args[0]))

        elif cmd in ["!escanear", "escanear", "!scan", "scan"]:
            target = args[0].lower() if args else "todas"
            return self._cmd_scan(target)

        else:
            # Default fallback: try searching text directly
            search_res = self._cmd_search(clean_text)
            return (
                f"ℹ️ Comando no reconocido. Te comparto los resultados de búsqueda para '*{clean_text}*':\n\n"
                f"{search_res}\n\n"
                f"*(Escribe `!ayuda` para ver todos los comandos disponibles)*"
            )

    def _cmd_summary(self) -> str:
        """Return executive KPIs and daily performance."""
        kpi = db.get_application_stats()
        gen = db.get_stats()
        now_str = datetime.now().strftime("%d/%m/%Y %H:%M")

        res = (
            f"📊 *RESUMEN EJECUTIVO DE OPORTUNIDADES* ({now_str})\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📂 *Total en Base de Datos:* {gen['total_jobs']} registros\n"
            f"⏳ *Pendientes de Contactar:* {gen['pending_count']}\n"
            f"📞 *Con Teléfono / WhatsApp:* {gen['with_phone_count']}\n"
            f"💰 *Presupuesto Promedio:* ${gen['avg_salary']:,.2f} MXN\n\n"
            f"🎯 *ACTIVIDAD Y GESTIÓN:* \n"
            f"• Contactadas / Postuladas: *{kpi['applied_count']}*\n"
            f"• Gestionadas Hoy: *{kpi['today_count']}*\n"
            f"• Esta Semana (7d): *{kpi['week_count']}*\n"
            f"• En Cotización / Entrevista: *{kpi['interview_count']}* (Éxito: *{kpi['conversion_rate']}%*)\n\n"
            f"💡 *Tip:* Escribe `!cotizaciones` para ver solicitudes de obra pendientes."
        )
        return res

    def _cmd_quotations(self, filter_str: str = "") -> str:
        """List electrical installation quotation leads with direct contact actions."""
        jobs = db.get_jobs(category="Ingeniero Eléctrico", order_by="id DESC")
        
        # Filter leads that have phones or are quote/installation leads
        quote_leads = [
            j for j in jobs 
            if (j.get("phone") or any(w in j["title"].lower() or w in j["description"].lower() for w in ["cotización", "cotizacion", "instalación", "instalacion", "presupuesto", "obra", "oficial", "ayudante", "tablero", "subestación"]))
        ]

        if filter_str:
            q = filter_str.lower()
            quote_leads = [j for j in quote_leads if q in j["title"].lower() or q in j["location"].lower() or q in j["company"].lower() or q in j["description"].lower()]

        if not quote_leads:
            return "🔍 No se encontraron solicitudes de cotizaciones con ese criterio. Escribe `!escanear fb` para buscar nuevas solicitudes en vivo."

        top_leads = quote_leads[:5]
        res = [f"⚡ *SOLICITUDES DE COTIZACIÓN Y OBRAS ELÉCTRICAS* ({len(quote_leads)} disponibles)\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]

        for idx, j in enumerate(top_leads, 1):
            j_id = j["id"]
            title = j["title"]
            contact = j["company"]
            loc = j["location"] or "México"
            sal = j["salary_raw"] or "A convenir"
            phone = j.get("phone", "")
            status = j.get("status", "Pendiente")

            # Generate direct pre-filled WhatsApp quotation link
            wa_link = notifier.generate_whatsapp_link(phone, title, contact, category="Ingeniero Eléctrico") if phone else ""

            item_text = (
                f"*{idx}. [ID #{j_id}] {title}*\n"
                f"👤 Contacto: *{contact}*\n"
                f"📍 Ubicación: {loc}\n"
                f"💰 Presupuesto: *{sal}*\n"
                f"📌 Estado: *{status}*\n"
            )
            if phone:
                item_text += f"📞 Teléfono: `{phone}`\n"
                item_text += f"💬 *Toca para cotizar:* {wa_link}\n"
            item_text += f"👉 *Registrar:* `!cotizado {j_id}` o `!detalle {j_id}`\n"
            res.append(item_text)

        res.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n💡 Escribe `!detalle [ID]` para ver alcance completo.")
        return "\n".join(res)

    def _cmd_vacancies(self, filter_str: str = "") -> str:
        """List vacancies matching optional filter."""
        jobs = db.get_jobs(search_query=filter_str if filter_str else None, order_by="id DESC")

        if not jobs:
            return f"🔍 No se encontraron vacantes con el filtro '*{filter_str}*'. Escribe `!vacantes` para ver todas."

        top_jobs = jobs[:5]
        res = [f"💼 *BOLSA DE VACANTES DISPONIBLES* (Mostrando {len(top_jobs)} de {len(jobs)})\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]

        for idx, j in enumerate(top_jobs, 1):
            j_id = j["id"]
            title = j["title"]
            comp = j["company"]
            src = j.get("source", "OCC")
            loc = j["location"] or "México"
            mod = j.get("modality", "No especificado")
            sal = j["salary_raw"] or "No especificado"
            phone = j.get("phone", "")
            status = j.get("status", "Pendiente")

            item_text = (
                f"*{idx}. [ID #{j_id}] {title}*\n"
                f"🏢 Empresa/Cliente: {comp} ({src})\n"
                f"📍 Ubicación: {loc} ({mod})\n"
                f"💰 Sueldo/Presupuesto: {sal}\n"
                f"📌 Estado: *{status}*\n"
            )
            if phone:
                wa_link = notifier.generate_whatsapp_link(phone, title, comp, category=j.get("category"))
                item_text += f"📞 Contacto: `{phone}` | 💬 {wa_link}\n"
            
            item_text += f"👉 *Acciones:* `!contacto {j_id}` | `!detalle {j_id}`\n"
            res.append(item_text)

        res.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n💡 Escribe `!contacto [ID]` para registrar tu postulación.")
        return "\n".join(res)

    def _cmd_search(self, query: str) -> str:
        """Perform text search across title, company, description, and location."""
        return self._cmd_vacancies(filter_str=query)

    def _cmd_detail(self, job_id: int) -> str:
        """Fetch full details and technical sheet of a specific vacancy."""
        job = db.get_job_by_id(job_id)
        if not job:
            return f"❌ No se encontró ninguna vacante u obra con el ID `#{job_id}`."

        title = job["title"]
        comp = job["company"]
        cat = job["category"]
        src = job.get("source", "OCC")
        loc = job["location"] or "México"
        mod = job.get("modality", "No especificado")
        sal = job["salary_raw"] or "No especificado"
        phone = job.get("phone", "")
        wa_url = job.get("whatsapp_url", "")
        desc = job.get("description", "Sin descripción.")
        url = job.get("url", "")
        status = job.get("status", "Pendiente")
        notes = job.get("notes", "")

        if not wa_url and phone:
            wa_url = notifier.generate_whatsapp_link(phone, title, comp, category=cat)

        res = (
            f"📋 *FICHA TÉCNICA Y DE CONTACTO [ID #{job_id}]*\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 *Puesto / Trabajo:* {title}\n"
            f"🏢 *Cliente / Empresa:* {comp}\n"
            f"🌐 *Plataforma:* {src} | 🏷️ *Área:* {cat}\n"
            f"📍 *Ubicación:* {loc} ({mod})\n"
            f"💰 *Sueldo / Presupuesto:* {sal}\n"
            f"📌 *Estado Actual:* *{status}*\n"
        )
        if phone:
            res += f"📞 *Teléfono para Llamada:* `{phone}`\n"
        if wa_url:
            res += f"💬 *WhatsApp Directo:* {wa_url}\n"
        if url:
            res += f"🔗 *Enlace Web:* {url}\n"

        res += f"\n📄 *DESCRIPCIÓN Y REQUERIMIENTOS:*\n{desc[:600]}...\n"

        if notes:
            res += f"\n📝 *Notas Personales:* {notes}\n"

        res += (
            f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"⚡ *GESTIONAR ESTE REGISTRO:*\n"
            f"• `!contacto {job_id}` - Marcar como *Postulado / En Contacto*\n"
            f"• `!cotizado {job_id}` - Marcar como *En Cotización / Entrevista*\n"
            f"• `!descartar {job_id}` - Descartar registro"
        )
        return res

    def _cmd_update_status(self, job_id: int, new_status: str, label: str) -> str:
        """Update the status of a job in SQLite and return confirmation."""
        job = db.get_job_by_id(job_id)
        if not job:
            return f"❌ No se encontró ninguna vacante con el ID `#{job_id}`."

        db.update_job_status(job_id, new_status)
        phone = job.get("phone", "")
        title = job["title"]
        comp = job["company"]

        res = [f"✅ *¡REGISTRO ACTUALIZADO EXITOSAMENTE!*\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"]
        res.append(f"📌 *Puesto/Obra:* {title}")
        res.append(f"🏢 *Cliente/Empresa:* {comp}")
        res.append(f"🏷️ *Nuevo Estado:* *{label}* (Guardado en base de datos)")

        if phone:
            wa_link = notifier.generate_whatsapp_link(phone, title, comp, category=job.get("category"))
            res.append(f"\n📞 *Teléfono:* `{phone}`")
            res.append(f"💬 *Toca para iniciar chat:* {wa_link}")

        res.append("\n💡 Escribe `!resumen` para ver tus estadísticas actualizadas.")
        return "\n".join(res)

    def _cmd_delete(self, job_id: int) -> str:
        """Delete or discard a job."""
        job = db.get_job_by_id(job_id)
        if not job:
            return f"❌ No se encontró la vacante `#{job_id}`."

        title = job["title"]
        db.delete_job(job_id)
        return f"🗑️ La vacante/obra `#{job_id}` (*{title}*) ha sido descartada y eliminada de tu base de datos."

    def _cmd_scan(self, target: str) -> str:
        """Trigger scrapers on demand from WhatsApp and return new counts."""
        res_msg = [f"🔄 *EJECUTANDO ESCANEO EN VIVO ({target.upper()})*..."]

        if target in ["fb", "facebook", "cotizaciones", "obras"]:
            r = FacebookScraper().run_scan_and_save()
            res_msg.append(f"✅ *Facebook:* Se procesaron {r['total_found']} publicaciones ({r['new_saved']} nuevas oportunidades guardadas).")
        elif target in ["linkedin", "lk"]:
            r = LinkedInScraper().run_search_and_save()
            res_msg.append(f"✅ *LinkedIn:* {r['total_new']} nuevas vacantes.")
        elif target in ["occ"]:
            r = OCCBot().run_search_and_save()
            res_msg.append(f"✅ *OCC:* {r['total_new']} nuevas vacantes.")
        elif target in ["computrabajo", "ct"]:
            r = CompuTrabajoScraper().run_search_and_save()
            res_msg.append(f"✅ *CompuTrabajo:* {r['total_new']} nuevas vacantes.")
        elif target in ["glassdoor", "gd"]:
            r = GlassdoorScraper().run_search_and_save()
            res_msg.append(f"✅ *Glassdoor:* {r['total_new']} nuevas vacantes.")
        elif target in ["jobrapido", "jr"]:
            r = JobrapidoScraper().run_search_and_save()
            res_msg.append(f"✅ *Jobrapido:* {r['total_new']} nuevas vacantes.")
        elif target in ["jobleads", "jl"]:
            r = JobLeadsScraper().run_search_and_save()
            res_msg.append(f"✅ *JobLeads:* {r['total_new']} nuevas vacantes.")
        elif target in ["jobsora", "js"]:
            r = JobsoraScraper().run_search_and_save()
            res_msg.append(f"✅ *Jobsora:* {r['total_new']} nuevas vacantes.")
        else:
            # Run all scrapers
            total_new = 0
            for sc_name, sc_cls in [
                ("Facebook", FacebookScraper),
                ("LinkedIn", LinkedInScraper),
                ("OCC", OCCBot),
                ("CompuTrabajo", CompuTrabajoScraper),
                ("Glassdoor", GlassdoorScraper),
                ("Jobrapido", JobrapidoScraper),
                ("JobLeads", JobLeadsScraper),
                ("Jobsora", JobsoraScraper)
            ]:
                try:
                    s = sc_cls()
                    if hasattr(s, "run_search_and_save"):
                        r = s.run_search_and_save()
                        total_new += r.get("total_new", 0)
                    elif hasattr(s, "run_scan_and_save"):
                        r = s.run_scan_and_save()
                        total_new += r.get("new_saved", 0)
                except Exception:
                    pass
            res_msg.append(f"✅ *Escaneo Global (8 Canales):* ¡Finalizado! Se encontraron e insertaron *{total_new}* nuevas oportunidades.")

        res_msg.append("\n💡 Escribe `!cotizaciones` o `!resumen` para ver las novedades.")
        return "\n".join(res_msg)

if __name__ == "__main__":
    bot = WhatsAppBot()
    print("=== TEST WHATSAPP BOT ===")
    print(bot.process_message("!ayuda"))
    print("\n--- TEST RESUMEN ---")
    print(bot.process_message("!resumen"))
    print("\n--- TEST COTIZACIONES ---")
    print(bot.process_message("!cotizaciones"))
