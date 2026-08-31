# 🚀 AutoJob Hunter & Tracker (8 Canales Laborales & Bot Interactivo de WhatsApp)

Sistema integral de automatización multiplataforma para la **búsqueda de empleo, extracción de vacantes, captura de solicitudes de cotizaciones eléctricas y control total remoto desde tu WhatsApp** en las 8 plataformas líderes en México (**Facebook**, **LinkedIn**, **OCC Mundial**, **CompuTrabajo**, **Glassdoor**, **Jobrapido**, **JobLeads**, **Jobsora**).

---

## 📱 Módulo Especial: Bot Interactivo de WhatsApp (Control Total desde tu Celular)

Gestiona toda tu búsqueda y cotizaciones directamente desde un chat de WhatsApp sin necesidad de abrir la computadora:

```
                  ┌────────────────────────────────────────┐
                  │          Tu WhatsApp Personal          │
                  │   [ !cotizaciones / !contacto 15 ]     │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │    Servidor Webhook (FastAPI/HTTP)     │
                  │      (core/whatsapp_server.py)         │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │       Motor WhatsAppBot (NLP)          │
                  │        (core/whatsapp_bot.py)          │
                  └──────────────┬──────────────────┬──────┘
                                 │                  │
                                 ▼                  ▼
                    [Base de Datos SQLite]    [Scrapers en Vivo]
                    [ Métricas / Estados ]    [ Facebook / OCC ]
```

### 📋 Comandos Disponibles en WhatsApp:

| Comando | Descripción | Ejemplo de Uso |
| :--- | :--- | :--- |
| `!resumen` / `!stats` | Métricas de hoy: postuladas hoy, esta semana, pendientes y promedios | `!resumen` |
| `!cotizaciones` / `!obras` | Lista solicitudes de electricistas, obras y presupuestos para llamar | `!cotizaciones` |
| `!vacantes` | Lista las últimas vacantes encontradas con sueldo y ubicación | `!vacantes` |
| `!vacantes [filtro]` | Filtra por puesto, tecnología o ciudad | `!vacantes oficial cdmx` |
| `!buscar [texto]` | Búsqueda libre en toda la base de datos | `!buscar queretaro` |
| `!detalle [id]` | Ver ficha técnica completa, teléfono, cliente y enlace directo | `!detalle 15` |
| `!contacto [id]` | Marca como **Postulado / En Contacto** y devuelve enlace WhatsApp | `!contacto 15` |
| `!cotizado [id]` | Marca como **En Cotización / Entrevista** en la base de datos | `!cotizado 15` |
| `!descartar [id]` | Elimina o descarta una vacante de la base | `!descartar 15` |
| `!escanear [fuente]` | Dispara escaneo remoto en vivo (`fb`, `occ`, `linkedin`, `todas`) | `!escanear fb` |
| `!ayuda` / `!menu` | Despliega el menú de comandos en tu chat | `!ayuda` |

---

## ⚡ Módulo Especial: Captura de Obras, Clientes y Categorías Eléctricas

Diseñado especialmente para **ingenieros, contratistas, Oficiales Eléctricos, Medio Oficiales y Ayudantes Electricistas** que buscan vacantes de obra, prospectar trabajos, llamar directamente a constructores y enviar cotizaciones y presupuestos formales:

- 👷 **Oficial Eléctrico / Oficial Electricista:** Especialistas en doblado de conduit PG (1/2" a 2"), charola portacable, cableado de fuerza y control (calibres 8 a 500 MCM), peinado de tableros de 480V/220V e interpretación de diagramas unifilares.
- 🔧 **Medio Oficial Eléctrico:** Ayudantes avanzados con experiencia en canalizaciones, jalado de conductores, fijación de cajas, ranurado, ponchado de terminales y apoyo directo al oficial.
- 🧰 **Ayudante Electricista / Ayudante General Eléctrico:** Personal para acarreo de material, guiado de cableado con guía de acero/nylon, colocación de soportería y asistencia en obra.
- 👤 **Nombre y Cargo del Contacto:** Captura directa del encargado de la obra (*Ing. Mateo Carvajal, Ing. Sergio Valenzuela, Ing. Gerardo Albarrán, Arq. Brenda Salgado, Arq. Luis Fernando Ríos, Ing. David Sotomayor, Arq. Roberto Morales, Lic. Claudia Benítez*).
- 📞 **Teléfono Directo:** Enlace de marcado telefónico inmediato (`tel:+52...`) para llamadas rápidas de postulación o prospección.
- 💬 **Generador de Cotizaciones por WhatsApp:** Enlace con mensaje formal precargado para solicitar planos y agendar visitas técnicas para enviar presupuestos bajo norma NOM-001-SEDE.

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Bot Interactivo de WhatsApp](#-módulo-especial-bot-interactivo-de-whatsapp-control-total-desde-tu-celular)
- [Módulo de Obras, Oficiales y Ayudantes Eléctricos](#-módulo-especial-captura-de-obras-clientes-y-categorías-eléctricas)
- [Plataformas de Empleo Integradas (8 Canales)](#-plataformas-de-empleo-integradas-8-canales)
- [Grupos de Facebook Rastreados](#-grupos-de-facebook-rastreados)
- [Dashboard de Estadísticas y Postulaciones Diarias](#-dashboard-de-estadísticas-y-postulaciones-diarias)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
- [Configuración de Webhook de WhatsApp](#-configuración-de-webhook-de-whatsapp)
- [Guía de Uso (CLI, WhatsApp y Dashboard)](#-guía-de-uso)
- [Panel de Control Web (Streamlit)](#-panel-de-control-web-streamlit)
- [Estructura de Datos Extraídos](#-estructura-de-datos-extraídos)
- [Plantilla de Mensaje de Cotización](#-plantilla-de-mensaje-de-cotización)

---

## 🌐 Plataformas de Empleo Integradas (8 Canales)

| Plataforma | Módulo | Enfoque Principal |
| :--- | :--- | :--- |
| **📱 Facebook** | `core/facebook_scraper.py` | Solicitudes de electricistas, Oficiales, Ayudantes, obras y presupuestos |
| **💼 LinkedIn** | `core/linkedin_scraper.py` | Multinacionales de telecomunicaciones, software y manufactura avanzada |
| **🌐 OCC Mundial** | `core/occ_bot.py` | Ofertas corporativas y contratación formal en México con subida de CV |
| **🟧 CompuTrabajo** | `core/computrabajo_scraper.py` | Empleos técnicos, de campo (Drive Test / Planta Externa) e industriales |
| **🟢 Glassdoor** | `core/glassdoor_scraper.py` | Posiciones con insights de compensación salarial y empresas calificadas |
| **🌐 Jobrapido** | `core/jobrapido_scraper.py` | Agregador masivo de vacantes de ingeniería a nivel nacional |
| **🎯 JobLeads** | `core/jobleads_scraper.py` | Puestos ejecutivos, Senior Engineers, Tech Leads y Gerencias Técnicas |
| **🔴 Jobsora** | `core/jobsora_scraper.py` | Empleos de ingeniería, técnicos en telecomunicaciones, electricidad y redes |

---

## 📈 Dashboard de Estadísticas y Postulaciones Diarias

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🎯 Total Gestionadas │ 📅 Contactadas Hoy │ 🗓️ Esta Semana │ 📆 Este Mes │ 🟣 En Cotización │
│        14            │         5          │       12       │     14      │  3 (Éxito: 21.4%)│
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                                               │
               ┌───────────────────────────────┴───────────────────────────────┐
               ▼                                                               ▼
 ┌──────────────────────────────────────────┐    ┌──────────────────────────────────────────┐
 │ 📈 Actividad Diaria (Gráfico Tiempo)     │    │ 🌐 Desglose de Oportunidades             │
 │ [Barras por Fecha YYYY-MM-DD]            │    │ - Por Plataforma (8 Canales)             │
 │ Promedio diario: 4.2 gestiones/día       │    │ - Por Especialidad (Eléctrica, RF, Soft) │
 └──────────────────────────────────────────┘    │ - Por Modalidad (Presencial, Híbrido...) │
                                                 └──────────────────────────────────────────┘
```

---

## 📂 Estructura del Proyecto

```plaintext
app_busca_trabajo/
├── config/
│   ├── __init__.py
│   ├── settings.py              # Configuraciones generales, variables .env y rutas
│   └── keywords.json            # Palabras clave (RF, Eléctrica, Oficial, Medio Oficial, Ayudante)
├── core/
│   ├── __init__.py
│   ├── database.py              # SQLite (jobs.db), métricas diarias, filtros y exportaciones
│   ├── data_extractor.py        # Parser inteligente (Puesto, Teléfono, Salario, Modalidad)
│   ├── whatsapp_bot.py          # Motor interactivo de comandos NLP para WhatsApp
│   ├── whatsapp_server.py       # Servidor Webhook HTTP universal para WhatsApp
│   ├── occ_bot.py               # Automatizador y scraper para OCC Mundial
│   ├── linkedin_scraper.py      # Scraper de ofertas en tiempo real en LinkedIn
│   ├── computrabajo_scraper.py  # Scraper de ofertas en tiempo real en CompuTrabajo
│   ├── glassdoor_scraper.py     # Scraper de ofertas y sueldos en Glassdoor
│   ├── jobrapido_scraper.py     # Scraper de ofertas en Jobrapido
│   ├── jobleads_scraper.py      # Scraper de ofertas ejecutivas en JobLeads
│   ├── jobsora_scraper.py       # Scraper de ofertas en Jobsora
│   ├── facebook_scraper.py      # Scraper de solicitudes, Oficiales, Ayudantes y cotizaciones en FB
│   └── notifier_whatsapp.py     # Generador de enlaces y cotizaciones para WhatsApp
├── data/
│   ├── cv/                      # Almacenamiento de CVs en PDF
│   ├── exports/                 # Reportes generados en Excel (.xlsx) / CSV
│   └── jobs.db                  # Base de datos local SQLite con índices
├── ui/
│   ├── __init__.py
│   └── app.py                   # Dashboard interactivo con 6 pestañas en Streamlit
├── main.py                      # Lanzador unificado por línea de comandos (CLI)
├── .env.example                 # Plantilla de variables de entorno
├── requirements.txt             # Dependencias de Python
└── README.md                    # Documentación técnica completa
```

---

## ⚙️ Requisitos Previos

- **Python 3.10+** (probado y 100% compatible con Python 3.14 en Windows/Linux/macOS).
- Navegador web moderno (Chrome, Edge, Firefox, Brave).
- Conexión a Internet.

---

## 🚀 Instalación y Puesta en Marcha

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/GhostLT/app_busca_trabajo.git
   cd app_busca_trabajo
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   # En Linux / macOS:
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno (`.env`):**
   ```bash
   cp .env.example .env
   ```

---

## 📲 Configuración de Webhook de WhatsApp

1. **Iniciar el servidor Webhook en segundo plano:**
   ```bash
   python main.py --bot --port 5000
   ```

2. **Exponer el puerto local con Ngrok (gratuito):**
   ```bash
   ngrok http 5000
   ```

3. **Configurar tu URL de Webhook en tu proveedor (GreenAPI, Twilio o Meta Cloud API):**
   - URL: `https://tu-subdominio.ngrok-free.app/whatsapp/webhook`

4. **¡Listo!** Escribe `!ayuda` o `!cotizaciones` desde tu WhatsApp para interactuar.

---

## 🖥️ Guía de Uso (CLI)

```bash
# Iniciar la interfaz web gráfica (Streamlit)
python main.py

# Iniciar la Consola Interactiva para probar comandos de WhatsApp en tu terminal
python main.py --chat

# Iniciar el Servidor Webhook de WhatsApp
python main.py --bot --port 5000

# Escanear solicitudes de electricistas y cotizaciones en Facebook
python main.py --fb

# Escanear TODAS las 8 plataformas simultáneamente
python main.py --all

# Ver estadísticas de la base de datos
python main.py --stats

# Exportar reporte a Excel (.xlsx) y CSV
python main.py --export
```

---

## 💬 Plantilla de Mensaje de Cotización

Al pulsar el botón **"💬 Cotizar por WhatsApp"** o usar el comando `!contacto [id]`, se abre la conversación con una propuesta formal:

> *"¡Hola **[Nombre del Contacto]**! Buen día. Espero que se encuentre muy bien.*  
> *Vi su solicitud en Facebook requiriendo **[Oficial Eléctrico / Medio Oficial / Ayudante / Instalación Eléctrica]** en **[Ubicación]**.*  
> *Somos especialistas en **instalaciones eléctricas, canalizaciones con tubería conduit PG, cableado de fuerza, armado de tableros y subestaciones** bajo la norma NOM-001-SEDE.*  
> *Con gusto podemos proporcionarle personal calificado (Oficiales y Ayudantes) o realizar el levantamiento técnico para enviarle una **cotización formal y presupuesto detallado**.*  
> *¿Me podría compartir más detalles del trabajo o la dirección de la obra? ¡Quedo a sus órdenes!"*

---

**Desarrollado para automatizar la prospección, cotización y contratación en Ingeniería y Obras Eléctricas.**