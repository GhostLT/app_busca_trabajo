import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import time
import random
from typing import List, Dict, Any, Optional
from datetime import datetime

import core.database as db
import core.data_extractor as extractor
import core.notifier_whatsapp as notifier

class FacebookScraper:
    """
    Scraper, feed monitor, and text extractor for Facebook job posts.
    """
    TARGET_GROUPS = [
        "Bolsa de Empleo Ingenieros de RF y Telecomunicaciones México",
        "Red de Ingenieros Eléctricos, Subestaciones y Potencia México",
        "Desarrolladores de Software y Empleos TI México (Remoto)"
    ]

    def parse_and_save_post(
        self,
        post_text: str,
        group_name: str = "Facebook Grupos de Empleo",
        custom_title: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Parse unstructured Facebook text, extract metadata and save to DB.
        """
        parsed = extractor.parse_job_post(
            text=post_text,
            source="Facebook",
            fallback_title=custom_title,
            company=group_name
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

    def get_simulated_group_feed(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate realistic engineering posts from Mexican Facebook groups.
        """
        feed = [
            {
                "group": "Bolsa de Empleo Ingenieros de RF y Telecomunicaciones México",
                "text": """¡Buenas tardes grupo! Tenemos vacante abierta para:
📌 INGENIERO DE OPTIMIZACIÓN RF 4G / 5G
🏢 Empresa: Telecomm & Wireless Services México
📍 Ubicación: Ciudad de México (Esquema Híbrido 3 días oficina, 2 home office)
💰 Sueldo: $35,000 a $45,000 pesos mensuales libres + Prestaciones Superiores (SGMM, fondo de ahorro)
🔧 Requisitos:
- Experiencia comprobable en optimización de clusters 4G/5G
- Manejo de KPIs (Drop call rate, HOSR, throughput)
- Experiencia con TEMS Investigation y Atoll
- Disponibilidad para iniciar en septiembre
📲 Interesados enviar CV directamente a mi WhatsApp: 55 4819 2038 o al link https://wa.me/525548192038 indicando en el asunto 'Vacante RF'.""",
                "category": "Ingeniero de RF / Optimización"
            },
            {
                "group": "Bolsa de Empleo Ingenieros de RF y Telecomunicaciones México",
                "text": """Solicito con carácter de URGENTE:
📡 INGENIERO DE DRIVE TEST Y RADIOFRECUENCIA
Empresa contratista de Telcel / AT&T
📍 Zona de trabajo: Monterrey y área metropolitana (100% Campo / Presencial)
💵 Ofrecemos: $22,000 - $28,000 netos + Viáticos + Camioneta utilitaria
Requisitos: Licencia de conducir vigente, experiencia mínima de 1 año en mediciones con Nemo Outdoor / Swissqual, entrega de reportes post-procesamiento.
📞 Mandar mensaje de WhatsApp al 81 2940 1827 para agendar entrevista técnica hoy mismo.""",
                "category": "Ingeniero de RF / Optimización"
            },
            {
                "group": "Red de Ingenieros Eléctricos, Subestaciones y Potencia México",
                "text": """⚡ CONVOCATORIA LABORAL:
Puesto: INGENIERO ELÉCTRICO DE SUBESTACIONES Y PROTECCIONES
Contratista Eléctrico Industrial
📍 Lugar: Querétaro (Parque Industrial El Marqués)
Sueldo mensual: $32,000 a $42,000 MXN libres + Bono de productividad
Actividades:
- Coordinación de relevadores de protección (SEL, Siemens)
- Pruebas a transformadores de potencia y TPs/TCs
- Elaboración de protocolos de puesta en servicio y apego a NOM-001-SEDE
WhatsApp de Recursos Humanos: +52 442 819 4059. ¡Contratación inmediata!""",
                "category": "Ingeniero Eléctrico"
            },
            {
                "group": "Red de Ingenieros Eléctricos, Subestaciones y Potencia México",
                "text": """Se busca:
⚡ INGENIERO ELECTRICISTA / ELECTROMECÁNICO RESIDENTE DE OBRA
Empresa: Desarrollos Energéticos Bajío
📍 Ubicación: Guanajuato / San Luis Potosí
Sueldo: $28,000 - $36,000 netos mensuales
Supervisión de tendido de cable en media tensión 13.8kV y 34.5kV, cuadros de distribución, tableros generales.
Contacto directo vía WhatsApp: 477 192 8374.""",
                "category": "Ingeniero Eléctrico"
            },
            {
                "group": "Desarrolladores de Software y Empleos TI México (Remoto)",
                "text": """🚀 ¡Estamos contratando!
Posición: INGENIERO DE SOFTWARE BACKEND PYTHON / DJANGO / FASTAPI
Empresa: FinTech LatAm Hub
Modalidad: 100% Remoto (Home Office permanente en cualquier parte de México)
Rango Salarial: $45,000 a $65,000 pesos netos al mes
Stack: Python 3.11+, FastAPI, PostgreSQL, Redis, Docker, AWS (Lambda, ECS)
Ofrecemos: 20 días de vacaciones, bono anual, apoyo para equipo de cómputo y SGMM.
Si te interesa manda tu CV o perfil de LinkedIn al WhatsApp +52 55 9182 7364 para contacto rápido.""",
                "category": "Ingeniero de Sistemas / Software"
            },
            {
                "group": "Desarrolladores de Software y Empleos TI México (Remoto)",
                "text": """Oportunidad laboral:
💻 INGENIERO DE SISTEMAS / DEVOPS ENGINEER JUNIOR - MID
Startup Mexicana de Inteligencia Artificial
Modalidad: Remoto / Híbrido CDMX
Sueldo: $38,000 a $48,000 MXN
Conocimientos en Linux, CI/CD con GitHub Actions, Docker y despliegue de modelos de IA.
Postúlate enviando WhatsApp al 55 3829 1048.""",
                "category": "Ingeniero de Sistemas / Software"
            }
        ]

        if category and category != "Todos":
            return [f for f in feed if f.get("category") == category]
        return feed

    def run_scan_and_save(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Scan feeds, parse jobs, and save all new postings into database.
        """
        feed = self.get_simulated_group_feed(category)
        total_found = len(feed)
        new_saved = 0

        for post in feed:
            res = self.parse_and_save_post(
                post_text=post["text"],
                group_name=post["group"]
            )
            if res.get("is_new"):
                new_saved += 1

        return {
            "success": True,
            "total_found": total_found,
            "new_saved": new_saved,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

if __name__ == "__main__":
    scraper = FacebookScraper()
    print("Escaneando publicaciones en grupos de Facebook...")
    res = scraper.run_scan_and_save()
    print(f"Escaneo finalizado. Encontradas: {res['total_found']}, Nuevas guardadas: {res['new_saved']}")