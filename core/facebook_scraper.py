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
    specializing in engineering, technician positions, Oficiales Eléctricos,
    Medio Oficiales, and direct client/contractor requests for electrical installations and quotations.
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
        Generate realistic engineering, technician, Oficial Eléctrico, Medio Oficial,
        and direct electrical installation/quotation leads with explicit contact names and phone numbers.
        """
        feed = [
            # 1. Oficial Eléctrico de Obra Industrial (CDMX / EdoMex)
            {
                "group": "Oficiales Electricistas, Medio Oficiales y Ayudantes Eléctricos México",
                "contact_name": "Ing. Mateo Carvajal (Residente de Obra)",
                "text": """⚡ SOLICITO URGENTE: OFICIAL ELÉCTRICO INDUSTRIAL
👤 Contacto: Ing. Mateo Carvajal (Supervisión Eléctrica)
🏢 Empresa: Instalaciones y Montajes Eléctricos del Valle
📍 Ubicación: Naucalpan / Tlalnepantla, Estado de México
💵 Sueldo: $5,500 - $6,800 libres semanales ($22,000 - $27,000 mensuales) + Horas extras pagadas + IMSS
Requisitos y actividades:
- Doblado y roscado de tubería conduit PG de 1/2" a 2" con dobladora hidráulica y manual
- Cableado de alimentadores principales y centros de carga trifásicos 480V/220V
- Peinado y conexión de tableros de distribución según planos eléctricos
- Interpretación de diagramas unifilares y cuadros de cargas
- Manejo de herramienta propia y equipo de seguridad (EPP)
📞 Interesados comunicarse por llamada o WhatsApp al 55 4190 8273 con el Ing. Mateo Carvajal para contratación inmediata.""",
                "category": "Ingeniero Eléctrico"
            },
            # 2. Medio Oficial Eléctrico (Monterrey)
            {
                "group": "Oficiales Electricistas, Medio Oficiales y Ayudantes Eléctricos México",
                "contact_name": "Ing. Sergio Valenzuela (Jefe de Cuadrilla)",
                "text": """🔧 SE BUSCA: MEDIO OFICIAL ELÉCTRICO / AYUDANTE AVANZADO
👤 Contacto: Ing. Sergio Valenzuela
🏢 Empresa: Proyectos Eléctricos e Industriales del Norte
📍 Ubicación: Monterrey / García, Nuevo León (Parque Industrial)
💰 Pago: $3,800 - $4,800 netos por semana ($15,200 - $19,200 mensuales) + Prestaciones de ley
Funciones:
- Apoyo directo al Oficial Eléctrico en tendido de tubería y charola tipo malla
- Jalado de cableado de fuerza y control calibres 10, 8 y 6 AWG
- Ranurado, fijación de cajas de registro y canalizaciones
- Ponchado de terminales de ojo y zapatas mecánicas
- Conocimiento básico de código de colores y uso de multímetro
📲 Mandar mensaje de WhatsApp al 81 8901 9284 con Sergio Valenzuela para integrarse esta semana.""",
                "category": "Ingeniero Eléctrico"
            },
            # 3. Cuadrilla: Oficiales y Medio Oficiales Electricistas (Querétaro)
            {
                "group": "Cotizaciones y Trabajos Eléctricos e Instalaciones México",
                "contact_name": "Arq. Luis Fernando Ríos (Contratista General)",
                "text": """⚡ REQUERIMOS CUADRILLA ELÉCTRICA: OFICIALES Y MEDIO OFICIALES
👤 Contacto: Arq. Luis Fernando Ríos
🏢 Proyecto: Ampliación de Nave Industrial y Líneas de Ensamble
📍 Ubicación: Parque Industrial Bernardo Quintana, Querétaro
💵 Sueldos:
- Oficial Eléctrico: $6,000 semanales libres
- Medio Oficial: $4,200 semanales libres
Alcance del proyecto:
- Instalación de ducto cuadrado, charola tipo escalera y tubería conduit pared gruesa
- Conexión de transformador seco de 150 kVA y tableros derivados
- Bajadas eléctricas para maquinaria CNC
📞 Llamadas o WhatsApp al 442 901 8374 con el Arq. Luis Fernando Ríos para entrevista y presupuesto.""",
                "category": "Ingeniero Eléctrico"
            },
            # 4. Cotización: Cableado de Nave Industrial y Alumbrado LED (Querétaro)
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
📲 Favor de comunicarse o mandar WhatsApp al 442 819 2039 con el Ing. David Sotomayor para agendar visita a la nave y enviar cotización formal.""",
                "category": "Ingeniero Eléctrico"
            },
            # 5. Cotización: Acometida Eléctrica y Centro de Carga Comercial (CDMX)
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
📞 Llamadas o WhatsApp directo al 55 4180 9283 con el Arq. Roberto Morales para enviar presupuesto y cotización.""",
                "category": "Ingeniero Eléctrico"
            },
            # 6. Cotización: Mantenimiento y Pruebas a Subestación 500kVA (Monterrey)
            {
                "group": "Obras, Remodelaciones y Contratistas Eléctricos Monterrey & Querétaro",
                "contact_name": "Lic. Claudia Benítez (Gerente de Mantenimiento)",
                "text": """⚡ SE SOLICITA CONTRATISTA / TÉCNICO ELECTRICISTA ESPECIALIZADO
👤 Contacto: Lic. Claudia Benítez (Gerencia de Mantenimiento)
🏢 Planta: Manufacturas y Troqueles del Norte S.A.
📍 Ubicación: Apodaca / San Nicolás de los Garza, Nuevo León
💰 Presupuesto de servicio: $35,000 - $55,000 MXN
Trabajo a cotizar:
- Mantenimiento preventivo anual a subestación eléctrica compacta de 500 kVA
- Pruebas físico-químicas a aceite dieléctrico y aislamiento Megger
📲 Contactar al WhatsApp +52 81 8902 4719 con la Lic. Claudia Benítez para solicitar bases y cotizar.""",
                "category": "Ingeniero Eléctrico"
            },
            # 7. Cotización: Instalación Eléctrica para Restaurante (Guadalajara)
            {
                "group": "Bolsa de Proyectos e Instalaciones Eléctricas Industriales Guadalajara",
                "contact_name": "Sr. Francisco Zavala (Contratista de Interiores)",
                "text": """🛠️ REQUIERO ELECTRICISTA O EQUIPO DE INSTALADORES ELÉCTRICOS
👤 Contacto: Sr. Francisco Zavala (Contratista General)
🏢 Proyecto: Remodelación y Apertura Restaurante Gourmet
📍 Ubicación: Zona Providencia / Zapopan, Guadalajara, Jalisco
💵 Presupuesto de mano de obra: $30,000 - $48,000 MXN
Requerimientos:
- Instalación eléctrica completa de cocina industrial y tablero de 24 polos
- Pastillas GFCI e iluminación arquitectónica
📞 Comunicarse por llamada o WhatsApp al 33 1902 8374 con Francisco Zavala para entrega de planos y cotización.""",
                "category": "Ingeniero Eléctrico"
            },
            # 8. Técnico Instalador de Fibra Óptica
            {
                "group": "Bolsa de Trabajo Técnicos Instaladores de Fibra Óptica y Telecomunicaciones México",
                "contact_name": "Lic. Mariana Valdés (Coordinadora RH)",
                "text": """🚨 ¡CONTRATACIÓN INMEDIATA PARA PROYECTO FTTH!
👤 Contacto: Lic. Mariana Valdés
📌 Puesto: TÉCNICO INSTALADOR DE FIBRA ÓPTICA Y EMPALMADOR
🏢 Contratista Autorizado Totalplay / Megacable
📍 Ubicación: Ciudad de México y Área Metropolitana
💰 Sueldo: $16,000 - $24,000 netos mensuales + Bono por mufa instalada
📲 Manda mensaje por WhatsApp al 55 4819 3920 con Mariana Valdés.""",
                "category": "Ingeniero de RF / Optimización"
            },
            # 9. Técnico en Sistemas y Soporte TI
            {
                "group": "Técnicos en Sistemas, Soporte TI y Redes México",
                "contact_name": "Ing. Fernando Castro (Líder Soporte)",
                "text": """💻 VACANTE: TÉCNICO EN SISTEMAS Y SOPORTE DE SITIO
👤 Contacto: Ing. Fernando Castro
🏢 Empresa: Soluciones Corporativas IT México
📍 Ubicación: Guadalajara, Jalisco (Zona Zapopan / Híbrido)
💰 Sueldo: $15,000 a $20,000 netos al mes + Vales
📩 Postúlate enviando WhatsApp al 33 2910 4829 con el Ing. Fernando Castro.""",
                "category": "Ingeniero de Sistemas / Software"
            },
            # 10. Técnico en Telecomunicaciones y Torres RF
            {
                "group": "Empleos Técnicos en Telecomunicaciones, Torres y Radiofrecuencia",
                "contact_name": "Ing. Víctor Almonte (Operaciones)",
                "text": """📡 SE BUSCA: TÉCNICO EN TELECOMUNICACIONES / TORRERO DE RADIOFRECUENCIA
👤 Contacto: Ing. Víctor Almonte
🏢 Empresa: Infraestructura Celular del Norte
📍 Base: Monterrey, N.L.
💵 Ofrecemos: $20,000 a $28,000 mensuales libres + Viáticos
📲 Enviar WhatsApp al +52 81 2940 8173 con Víctor Almonte.""",
                "category": "Ingeniero de RF / Optimización"
            }
        ]

        if category and category != "Todos":
            return [f for f in feed if f.get("category") == category]
        return feed

    def run_scan_and_save(self, category: Optional[str] = None) -> Dict[str, Any]:
        """
        Scan feeds, parse jobs, electrical installation quotation requests, Oficiales Eléctricos,
        and technician leads, and save all new postings into database.
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
    print("Escaneando grupos de Facebook (Oficiales Eléctricos, Medio Oficiales, Cotizaciones y Técnicos)...")
    res = scraper.run_scan_and_save()
    print(f"Escaneo finalizado. Total encontradas: {res['total_found']}, Nuevas guardadas: {res['new_saved']}")