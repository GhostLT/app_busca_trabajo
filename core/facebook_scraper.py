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
    Scraper, feed monitor, and text extractor for Facebook job posts and groups
    specializing in engineering and technical roles (Técnico Instalador, Técnico Electricista,
    Técnico en Sistemas, Técnico de Fibra Óptica, Técnico en Telecomunicaciones).
    """
    TARGET_GROUPS = [
        "Bolsa de Empleo Ingenieros de RF y Telecomunicaciones México",
        "Red de Ingenieros Eléctricos, Subestaciones y Potencia México",
        "Desarrolladores de Software y Empleos TI México (Remoto)",
        "Bolsa de Trabajo Técnicos Instaladores de Fibra Óptica y Telecomunicaciones México",
        "Técnicos Electricistas e Instalaciones Eléctricas Industriales México",
        "Técnicos en Sistemas, Soporte TI y Redes México",
        "Empleos Técnicos en Telecomunicaciones, Torres y Radiofrecuencia"
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
        Generate realistic engineering and technician posts from Mexican Facebook groups.
        """
        feed = [
            # 1. Técnico Instalador de Fibra Óptica
            {
                "group": "Bolsa de Trabajo Técnicos Instaladores de Fibra Óptica y Telecomunicaciones México",
                "text": """🚨 ¡CONTRATACIÓN INMEDIATA PARA PROYECTO FTTH!
📌 Puesto: TÉCNICO INSTALADOR DE FIBRA ÓPTICA Y EMPALMADOR
🏢 Contratista Autorizado Totalplay / Megacable
📍 Ubicación: Ciudad de México y Área Metropolitana (Norte / Oriente)
💰 Sueldo: $16,000 - $24,000 netos mensuales + Bono por mufa instalada + PSL
🔧 Requisitos:
- Experiencia en tendido aéreo y subterráneo de fibra óptica
- Manejo de máquina de empalme por fusión (Fujikura / Sumitomo) y equipo OTDR
- Manejo de escalera de extensión y herramientas de fibra
- Licencia de conducir vigente
📲 Manda mensaje por WhatsApp al 55 4819 3920 para entrevista inmediata.""",
                "category": "Ingeniero de RF / Optimización"
            },
            # 2. Técnico Electricista
            {
                "group": "Técnicos Electricistas e Instalaciones Eléctricas Industriales México",
                "text": """⚡ SOLICITO TÉCNICO ELECTRICISTA INDUSTRIAL
Empresa de Mantenimiento Eléctrico Industrial Bajío
📍 Zona de trabajo: Querétaro (Parque Industrial Benito Juárez)
💵 Salario: $18,000 a $26,000 pesos mensuales libres + Fondo de ahorro
Actividades:
- Armado y cableado de tableros de control y distribución
- Mantenimiento preventivo a transformadores y plantas de emergencia
- Canalizaciones con tubería conduit PG y charola portacable
- Conocimiento de la NOM-001-SEDE
📞 Interesados comunicarse al WhatsApp: 442 819 3048.""",
                "category": "Ingeniero Eléctrico"
            },
            # 3. Técnico en Sistemas
            {
                "group": "Técnicos en Sistemas, Soporte TI y Redes México",
                "text": """💻 VACANTE: TÉCNICO EN SISTEMAS Y SOPORTE DE SITIO
Empresa: Soluciones Corporativas IT México
📍 Ubicación: Guadalajara, Jalisco (Zona Zapopan / Híbrido)
💰 Sueldo: $15,000 a $20,000 netos al mes + Vales de despensa
Requisitos:
- Mantenimiento preventivo y correctivo a equipo de cómputo (hardware/software)
- Configuración de redes locales, routers, switches y access points
- Soporte a usuarios, impresoras y sistemas operativos Windows/Mac
- Ponchado de cables UTP y cableado estructurado Cat 6
📩 Postúlate enviando WhatsApp al 33 2910 4829 con la palabra 'TÉCNICO SISTEMAS'.""",
                "category": "Ingeniero de Sistemas / Software"
            },
            # 4. Técnico en Telecomunicaciones / Torrero
            {
                "group": "Empleos Técnicos en Telecomunicaciones, Torres y Radiofrecuencia",
                "text": """📡 SE BUSCA: TÉCNICO EN TELECOMUNICACIONES / TORRERO DE RADIOFRECUENCIA
Empresa de Infraestructura Celular para Red Compartida / Telcel
📍 Base: Monterrey, N.L. con disponibilidad para viajar en el norte del país
💵 Ofrecemos: $20,000 a $28,000 mensuales libres + Viáticos pagados al 100% + Bono por sitio
Requisitos:
- Experiencia en ascenso a torres arriostradas y autosoportadas (curso DC-3 vigente)
- Instalación de antenas sectoriales, RRUs, jumpers y cable coaxial
- Alineación de radioenlaces microondas
- Manejo de Site Master y mediciones de VSWR
📲 Enviar CV o datos al WhatsApp: +52 81 2940 8173.""",
                "category": "Ingeniero de RF / Optimización"
            },
            # 5. Técnico Instalador de CCTV y Redes
            {
                "group": "Bolsa de Trabajo Técnicos Instaladores de Fibra Óptica y Telecomunicaciones México",
                "text": """🔧 VACANTE: TÉCNICO INSTALADOR DE CABLEADO Y SEGURIDAD ELECTRÓNICA
Empresa de Seguridad y Redes México
📍 Lugar: Ciudad de México (Polanco / Cuauhtémoc)
💰 Sueldo: $14,000 - $19,000 MXN mensuales netos + Comisiones por instalación
Funciones:
- Instalación y configuración de cámaras de seguridad CCTV IP y análogas (Hikvision / Dahua)
- Instalación de control de acceso y alarmas
- Peinado y ponchado de racks y paneles de parcheo
Contacto directo vía WhatsApp: 55 9182 3019.""",
                "category": "Ingeniero de Sistemas / Software"
            },
            # 6. Ingeniero de RF (LinkedIn/FB)
            {
                "group": "Bolsa de Empleo Ingenieros de RF y Telecomunicaciones México",
                "text": """¡Buenas tardes grupo! Tenemos vacante abierta para:
📌 INGENIERO DE OPTIMIZACIÓN RF 4G / 5G
🏢 Empresa: Telecomm & Wireless Services México
📍 Ubicación: Ciudad de México (Esquema Híbrido 3 días oficina, 2 home office)
💰 Sueldo: $35,000 a $45,000 pesos mensuales libres + Prestaciones Superiores
🔧 Requisitos:
- Experiencia comprobable en optimización de clusters 4G/5G
- Manejo de KPIs (Drop call rate, HOSR, throughput)
- Experiencia con TEMS Investigation y Atoll
📲 Interesados enviar CV directamente a mi WhatsApp: 55 4819 2038 o https://wa.me/525548192038""",
                "category": "Ingeniero de RF / Optimización"
            },
            # 7. Ingeniero Eléctrico de Subestaciones
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
            # 8. Desarrollador Python Backend
            {
                "group": "Desarrolladores de Software y Empleos TI México (Remoto)",
                "text": """🚀 ¡Estamos contratando!
Posición: INGENIERO DE SOFTWARE BACKEND PYTHON / DJANGO / FASTAPI
Empresa: FinTech LatAm Hub
Modalidad: 100% Remoto (Home Office permanente en cualquier parte de México)
Rango Salarial: $45,000 a $65,000 pesos netos al mes
Stack: Python 3.11+, FastAPI, PostgreSQL, Redis, Docker, AWS
Manda tu CV o perfil al WhatsApp +52 55 9182 7364 para contacto rápido.""",
                "category": "Ingeniero de Sistemas / Software"
            }
        ]

        if category and category != "Todos":
            return [f for f in feed if f.get("category") == category]
        return feed

    def run_scan_and_save(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Scan feeds, parse technician and engineering jobs, and save all new postings into database.
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
    print("Escaneando publicaciones técnicas y de ingeniería en grupos de Facebook...")
    res = scraper.run_scan_and_save()
    print(f"Escaneo finalizado. Encontradas: {res['total_found']}, Nuevas guardadas: {res['new_saved']}")