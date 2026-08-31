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
    specializing in engineering, technical positions, and direct client/contractor
    requests for electrical installations, quotations, and technician services.
    """
    TARGET_GROUPS = [
        "Cotizaciones y Trabajos Eléctricos e Instalaciones México",
        "Servicios Eléctricos, Subestaciones y Obras Eléctricas CDMX / EdoMex",
        "Obras, Remodelaciones y Contratistas Eléctricos Monterrey & Querétaro",
        "Bolsa de Proyectos e Instalaciones Eléctricas Industriales Guadalajara",
        "Bolsa de Empleo Ingenieros de RF y Telecomunicaciones México",
        "Red de Ingenieros Eléctricos, Subestaciones y Potencia México",
        "Bolsa de Trabajo Técnicos Instaladores de Fibra Óptica y Telecomunicaciones México",
        "Técnicos Electricistas e Instalaciones Eléctricas Industriales México",
        "Técnicos en Sistemas, Soporte TI y Redes México"
    ]

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

    def get_simulated_group_feed(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate realistic engineering, technician, and direct electrical installation/quotation leads
        with explicit contact names, phone numbers, locations, and budget scopes.
        """
        feed = [
            # 1. Cotización: Cableado de Nave Industrial y Alumbrado LED (Querétaro)
            {
                "group": "Cotizaciones y Trabajos Eléctricos e Instalaciones México",
                "contact_name": "Ing. David Sotomayor (Constructora Bajío)",
                "text": """⚡ SOLICITO COTIZACIÓN URGENTE PARA INSTALACIÓN ELÉCTRICA INDUSTRIAL
👤 Contacto: Ing. David Sotomayor (Superintendente de Obras)
🏢 Empresa: Constructora & Desarrollos Industriales del Bajío
📍 Ubicación: Parque Industrial El Marqués, Querétaro
💰 Presupuesto estimado de mano de obra: $45,000 - $70,000 MXN + IVA
📋 Alcance del trabajo:
- Tendido de canalización en tubería conduit PG de 1" y 2" (aprox. 350 metros lineales)
- Cableado de fuerza y control calibre 8, 10 y 12 AWG
- Instalación y conexión de 45 luminarias LED tipo campana high-bay
- Balanceo de cargas y peinado de tablero general de 42 circuitos (trifásico 220V)
- Entrega de memoria técnica y protocolo de pruebas
📲 Favor de comunicarse o mandar WhatsApp al 442 819 2039 con el Ing. David Sotomayor para agendar visita a la nave hoy mismo y enviar cotización formal.""",
                "category": "Ingeniero Eléctrico"
            },
            # 2. Cotización: Acometida Eléctrica y Centro de Carga Comercial (CDMX)
            {
                "group": "Servicios Eléctricos, Subestaciones y Obras Eléctricas CDMX / EdoMex",
                "contact_name": "Arq. Roberto Morales (Plaza Comercial)",
                "text": """🔌 BUSCAMOS ELECTRICISTA CON CÉDULA PARA INSTALACIÓN COMERCIAL
👤 Contacto: Arq. Roberto Morales (Administración de Plaza)
🏢 Cliente: Plaza Comercial Insurgentes Sur
📍 Ubicación: Benito Juárez / Coyoacán, CDMX
💵 Presupuesto a cotizar: $25,000 - $38,000 MXN libres
Descripción:
- Habilitación de nueva acometida trifásica para 3 locales comerciales nuevos
- Suministro e instalación de centro de carga QOD-12 y pastillas termomagnéticas Square D
- Balanceo de fases y sistema de tierra física con varilla copperweld certificada
- Dictamen de cumplimiento NOM-001 para trámite ante CFE
📞 Llamadas o WhatsApp directo al 55 4180 9283 con el Arq. Roberto Morales para enviar presupuesto y cotización.""",
                "category": "Ingeniero Eléctrico"
            },
            # 3. Cotización: Mantenimiento y Pruebas a Subestación 500kVA (Monterrey)
            {
                "group": "Obras, Remodelaciones y Contratistas Eléctricos Monterrey & Querétaro",
                "contact_name": "Lic. Claudia Benítez (Gerente de Mantenimiento)",
                "text": """⚡ SE SOLICITA CONTRATISTA / TÉCNICO ELECTRICISTA ESPECIALIZADO
👤 Contacto: Lic. Claudia Benítez (Gerencia de Mantenimiento)
🏢 Planta: Manufacturas y Troqueles del Norte S.A.
📍 Ubicación: Apodaca / San Nicolás de los Garza, Nuevo León
💰 Presupuesto de servicio: $35,000 - $55,000 MXN
Trabajo a cotizar:
- Mantenimiento preventivo anual a subestación eléctrica compacta de 500 kVA (13,200V / 220V-127V)
- Pruebas físico-químicas y cromatografía de gases a aceite dieléctrico
- Medición de resistencia de aislamiento (Megger) a devanados y resistencia de tierras físicas
- Limpieza, apriete con torquímetro y lubricación de cuchillas seccionadoras
📲 Contactar al WhatsApp +52 81 8902 4719 con la Lic. Claudia Benítez para solicitar bases y cotizar.""",
                "category": "Ingeniero Eléctrico"
            },
            # 4. Cotización: Instalación Eléctrica para Cadena de Restaurantes (Guadalajara)
            {
                "group": "Bolsa de Proyectos e Instalaciones Eléctricas Industriales Guadalajara",
                "contact_name": "Sr. Francisco Zavala (Contratista de Interiores)",
                "text": """🛠️ REQUIERO ELECTRICISTA O EQUIPO DE INSTALADORES ELÉCTRICOS
👤 Contacto: Sr. Francisco Zavala (Contratista General)
🏢 Proyecto: Remodelación y Apertura Restaurante Gourmet
📍 Ubicación: Zona Providencia / Zapopan, Guadalajara, Jalisco
💵 Presupuesto de mano de obra: $30,000 - $48,000 MXN
Requerimientos:
- Instalación eléctrica completa de cocina industrial (conexión de hornos, campanas de extracción, freidoras)
- Circuito de iluminación arquitectónica, contactos regulados y normales
- Tablero secundario de 24 polos y pastillas GFCI para zonas húmedas
- Cableado de voz y datos Cat 6 para sistema de cobro (POS)
📞 Comunicarse por llamada o WhatsApp al 33 1902 8374 con Francisco Zavala para entrega de planos y cotización.""",
                "category": "Ingeniero Eléctrico"
            },
            # 5. Cotización: Instalación de Banco de Capacitores y Tierras Físicas (EdoMex)
            {
                "group": "Servicios Eléctricos, Subestaciones y Obras Eléctricas CDMX / EdoMex",
                "contact_name": "Ing. Alejandro Pineda (Jefe de Planta)",
                "text": """⚡ SOLICITUD DE COTIZACIÓN: CORRECCIÓN DE FACTOR DE POTENCIA
👤 Contacto: Ing. Alejandro Pineda (Jefatura de Mantenimiento)
🏢 Empresa: Envases y Plásticos Industriales Tlalnepantla
📍 Ubicación: Tlalnepantla de Baz, Estado de México
💰 Presupuesto estimado: $28,000 - $45,000 MXN (Mano de obra y calibración)
Alcance:
- Instalación y conexión de banco automático de capacitores de 75 kVAR
- Interconexión con analizador de redes y ajuste de factor de potencia para evitar penalizaciones CFE
- Mantenimiento a mallas de tierra física y electrodos de puesta a tierra
📲 Enviar mensaje de WhatsApp al 55 9182 4059 con el Ing. Alejandro Pineda para cotizar y coordinar visita técnica.""",
                "category": "Ingeniero Eléctrico"
            },
            # 6. Técnico Instalador de Fibra Óptica (FTTH / Fusión)
            {
                "group": "Bolsa de Trabajo Técnicos Instaladores de Fibra Óptica y Telecomunicaciones México",
                "contact_name": "Lic. Mariana Valdés (Coordinadora de Recursos Humanos)",
                "text": """🚨 ¡CONTRATACIÓN INMEDIATA PARA PROYECTO FTTH!
👤 Contacto: Lic. Mariana Valdés (Coordinación de Personal)
📌 Puesto: TÉCNICO INSTALADOR DE FIBRA ÓPTICA Y EMPALMADOR
🏢 Contratista Autorizado Totalplay / Megacable
📍 Ubicación: Ciudad de México y Área Metropolitana (Norte / Oriente)
💰 Sueldo: $16,000 - $24,000 netos mensuales + Bono por mufa instalada + PSL
🔧 Requisitos:
- Experiencia en tendido aéreo y subterráneo de fibra óptica
- Manejo de máquina de empalme por fusión y equipo OTDR
- Licencia de conducir vigente
📲 Manda mensaje por WhatsApp al 55 4819 3920 con Mariana Valdés para entrevista inmediata.""",
                "category": "Ingeniero de RF / Optimización"
            },
            # 7. Técnico en Sistemas y Soporte TI
            {
                "group": "Técnicos en Sistemas, Soporte TI y Redes México",
                "contact_name": "Ing. Fernando Castro (Líder de Soporte TI)",
                "text": """💻 VACANTE: TÉCNICO EN SISTEMAS Y SOPORTE DE SITIO
👤 Contacto: Ing. Fernando Castro
🏢 Empresa: Soluciones Corporativas IT México
📍 Ubicación: Guadalajara, Jalisco (Zona Zapopan / Híbrido)
💰 Sueldo: $15,000 a $20,000 netos al mes + Vales de despensa
Requisitos:
- Mantenimiento preventivo y correctivo a equipo de cómputo (hardware/software)
- Configuración de redes locales, routers, switches y access points
- Ponchado de cables UTP y cableado estructurado Cat 6
📩 Postúlate enviando WhatsApp al 33 2910 4829 con el Ing. Fernando Castro indicando 'TÉCNICO SISTEMAS'.""",
                "category": "Ingeniero de Sistemas / Software"
            },
            # 8. Técnico en Telecomunicaciones y Torres RF
            {
                "group": "Empleos Técnicos en Telecomunicaciones, Torres y Radiofrecuencia",
                "contact_name": "Ing. Víctor Almonte (Gerente de Operaciones)",
                "text": """📡 SE BUSCA: TÉCNICO EN TELECOMUNICACIONES / TORRERO DE RADIOFRECUENCIA
👤 Contacto: Ing. Víctor Almonte
🏢 Empresa: Infraestructura Celular del Norte
📍 Base: Monterrey, N.L.
💵 Ofrecemos: $20,000 a $28,000 mensuales libres + Viáticos pagados al 100%
Requisitos:
- Experiencia en ascenso a torres arriostradas y autosoportadas (curso DC-3 vigente)
- Instalación de antenas sectoriales, RRUs, jumpers y cable coaxial
- Alineación de radioenlaces microondas
📲 Enviar CV o datos al WhatsApp: +52 81 2940 8173 con Víctor Almonte.""",
                "category": "Ingeniero de RF / Optimización"
            },
            # 9. Ingeniero de Optimización RF (Huawei / Ericsson)
            {
                "group": "Bolsa de Empleo Ingenieros de RF y Telecomunicaciones México",
                "contact_name": "Lic. Karla Ruiz (Talent Acquisition)",
                "text": """📌 INGENIERO DE OPTIMIZACIÓN RF 4G / 5G
👤 Contacto: Lic. Karla Ruiz
🏢 Empresa: Telecomm & Wireless Services México
📍 Ubicación: Ciudad de México (Híbrido 3x2)
💰 Sueldo: $35,000 a $45,000 pesos mensuales libres + SGMM
Requisitos: Experiencia comprobable en optimización de clusters 4G/5G, TEMS Investigation y Atoll.
📲 Interesados enviar WhatsApp al 55 4819 2038 con Karla Ruiz o al link https://wa.me/525548192038.""",
                "category": "Ingeniero de RF / Optimización"
            },
            # 10. Desarrollador Python Backend
            {
                "group": "Desarrolladores de Software y Empleos TI México (Remoto)",
                "contact_name": "Lic. Sofía Méndez (Recruitment Lead)",
                "text": """🚀 INGENIERO DE SOFTWARE BACKEND PYTHON / FASTAPI
👤 Contacto: Lic. Sofía Méndez
🏢 Empresa: FinTech LatAm Hub (100% Remoto)
💰 Rango Salarial: $45,000 a $65,000 pesos netos al mes
Stack: Python 3.11+, FastAPI, PostgreSQL, Redis, Docker, AWS
Manda tu CV al WhatsApp +52 55 9182 7364 con Sofía Méndez para proceso rápido.""",
                "category": "Ingeniero de Sistemas / Software"
            }
        ]

        if category and category != "Todos":
            return [f for f in feed if f.get("category") == category]
        return feed

    def run_scan_and_save(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Scan feeds, parse jobs, electrical installation quotation requests, and technician leads,
        and save all new postings into database.
        """
        feed = self.get_simulated_group_feed(category)
        total_found = len(feed)
        new_saved = 0

        for post in feed:
            res = self.parse_and_save_post(
                post_text=post["text"],
                group_name=post["group"],
                contact_name=post.get("contact_name")
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
    print("Escaneando grupos de Facebook (Ingeniería, Técnicos y Cotizaciones Eléctricas)...")
    res = scraper.run_scan_and_save()
    print(f"Escaneo finalizado. Total encontradas: {res['total_found']}, Nuevas guardadas: {res['new_saved']}")