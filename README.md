# 🚀 AutoJob Hunter & Tracker (8 Canales Laborales & Cotizador de Instalaciones Eléctricas)

Sistema integral de automatización multiplataforma para la **búsqueda de empleo, extracción de vacantes y captura de solicitudes de cotizaciones de obras e instalaciones eléctricas** en las 8 plataformas líderes en México (**Facebook**, **LinkedIn**, **OCC Mundial**, **CompuTrabajo**, **Glassdoor**, **Jobrapido**, **JobLeads**, **Jobsora**).

---

## ⚡ Módulo Especial: Captura de Clientes, Obras y Puestos Eléctricos

Diseñado especialmente para **ingenieros, contratistas, Oficiales Eléctricos y Medio Oficiales** que buscan vacantes de obra, prospectar trabajos, llamar directamente a constructores y enviar cotizaciones y presupuestos formales:

- 👷 **Oficial Eléctrico / Oficial Electricista:** Especialistas en doblado de conduit PG (1/2" a 2"), charola portacable, cableado de fuerza y control (calibres 8 a 500 MCM), peinado de tableros de 480V/220V e interpretación de diagramas unifilares.
- 🔧 **Medio Oficial Eléctrico:** Ayudantes avanzados con experiencia en canalizaciones, jalado de conductores, fijación de cajas, ranurado, ponchado de terminales y apoyo directo al oficial.
- 👤 **Nombre y Cargo del Contacto:** Captura directa del encargado de la obra (*Ing. Mateo Carvajal, Ing. Sergio Valenzuela, Arq. Luis Fernando Ríos, Ing. David Sotomayor, Arq. Roberto Morales, Lic. Claudia Benítez*).
- 📞 **Teléfono Directo:** Enlace de marcado telefónico inmediato (`tel:+52...`) para llamadas rápidas.
- 💬 **Generador de Cotizaciones por WhatsApp:** Enlace con mensaje formal precargado para solicitar planos y agendar visitas técnicas para enviar presupuestos bajo norma NOM-001-SEDE.
- 💰 **Presupuestos y Salarios:** Rangos semanales (*$5,500 - $6,800 libres para Oficiales; $3,800 - $4,800 para Medio Oficiales*) y presupuestos de obra (*$25,000 - $70,000 MXN*).

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Módulo de Obras, Oficiales y Cotizaciones](#-módulo-especial-captura-de-clientes-obras-y-puestos-eléctricos)
- [Plataformas de Empleo Integradas (8 Canales)](#-plataformas-de-empleo-integradas-8-canales)
- [Grupos de Facebook Rastreados](#-grupos-de-facebook-rastreados)
- [Dashboard de Estadísticas y Postulaciones Diarias](#-dashboard-de-estadísticas-y-postulaciones-diarias)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
- [Variables de Entorno (.env)](#-variables-de-entorno-env)
- [Guía de Uso (CLI y Dashboard)](#-guía-de-uso)
- [Panel de Control Web (Streamlit)](#-panel-de-control-web-streamlit)
- [Estructura de Datos Extraídos](#-estructura-de-datos-extraídos)
- [Plantilla de Mensaje de Cotización](#-plantilla-de-mensaje-de-cotización)
- [Próximas Mejoras](#-próximas-mejoras)

---

## ✨ Características Principales

### 1. 🌐 Rastreo y Extracción Multiplataforma (8 Canales)
- 📱 **Facebook (Grupos, Obras y Oficiales):** Solicitudes de Oficiales Eléctricos, Medio Oficiales, electricistas industriales, técnicos instaladores de fibra, CCTV y telecomunicaciones.
- 💼 **LinkedIn Jobs México:** Vacantes corporativas de ingeniería en empresas globales.
- 🌐 **OCC Mundial:** Extracción de ofertas técnicas y postulación con CV.
- 🟧 **CompuTrabajo:** Empleos técnicos, de campo e industriales.
- 🟢 **Glassdoor México:** Estimaciones salariales, valoraciones de empresa y vacantes Tech.
- 🌐 **Jobrapido México:** Agregador nacional de ofertas de ingeniería y telecomunicaciones.
- 🎯 **JobLeads México:** Oportunidades Senior, Lead y de nivel ejecutivo.
- 🔴 **Jobsora México:** Cobertura de vacantes técnicas y de ingeniería.

### 2. 📊 Dashboard de Estadísticas y Control Diario
- **Monitoreo Diario:** Registro cronológico exacto de la fecha y hora (`applied_at`) en que contactas o postulas a cada vacante/obra.
- **Métricas de Rendimiento:** KPIs en tiempo real para postulaciones de **Hoy**, **Esta Semana (7 días)**, **Este Mes** y **Total Histórico**.
- **Tasa de Conversión:** Porcentaje de éxito entre contactos realizados y entrevistas/cotizaciones enviadas (`% de Éxito`).
- **Gráfica de Ritmo Diario:** Visualización en barras de la actividad diaria acumulada.
- **Desglose Multidimensional:** Gráficas comparativas por plataforma (8 Canales), por especialidad y por modalidad (*Remoto*, *Híbrido*, *Presencial*).
- **Historial Completo:** Tabla interactiva para dar seguimiento a cada contacto con su estado, fecha, teléfono y notas.

### 3. 🎛️ Bolsa de Vacantes & Cotizaciones con Filtros Avanzados
- **Filtro por Plataforma:** Selector rápido para filtrar entre las 8 fuentes laborales.
- **Filtro por Ciudad / Ubicación:** Búsqueda inteligente con resolución de alias locales (*Querétaro/Qro, CDMX, Monterrey/MTY, Guadalajara/GDL, etc.*).
- **Botón de Aplicar Filtros:** Formulario interactivo con botón primario `🔍 Aplicar Filtros`.
- **Botones de Estado Sincronizados:** Los botones `⬜ Postular / Contactar` y `🎯 Cotizar / Entrevista` inician sin seleccionar por defecto y actualizan la base de datos en tiempo real al hacer clic (`✅ En Contacto` o `🟣 En Cotización`), permitiendo también desmarcarlos con un segundo clic.
- **Exportación de Datos:** Descarga de reportes completos en **Excel (`.xlsx`)** y **CSV** con columnas para `company` (contacto), `phone`, `whatsapp_url`, `modality` y `applied_at`.

---

## 👥 Grupos de Facebook Rastreados

El módulo `core/facebook_scraper.py` monitorea activamente:
1. **Oficiales Electricistas, Medio Oficiales y Ayudantes Eléctricos México** (Obras industriales, cuadrillas, cableado).
2. **Cotizaciones y Trabajos Eléctricos e Instalaciones México** (Naves industriales, acometidas, tableros).
3. **Servicios Eléctricos, Subestaciones y Obras Eléctricas CDMX / EdoMex** (Plazas comerciales, CFE, media tensión).
4. **Obras, Remodelaciones y Contratistas Eléctricos Monterrey & Querétaro** (Mantenimiento de subestaciones, parques industriales).
5. **Bolsa de Proyectos e Instalaciones Eléctricas Industriales Guadalajara** (Restaurantes, bancos de capacitores, control).
6. **Bolsa de Trabajo Técnicos Instaladores de Fibra Óptica y Telecomunicaciones México** (FTTH, Empalmes por fusión).
7. **Técnicos en Sistemas, Soporte TI y Redes México** (Cableado estructurado, racks, redes).

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
                                               │
                                               ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────┐
 │ 📋 Tabla Detallada de Oportunidades (Fecha, Contacto/Cliente, Puesto, Teléfono, WhatsApp)│
 └──────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Arquitectura del Sistema

```
                         ┌───────────────────────────────┐
                         │   Panel de Control Visual     │
                         │   (Streamlit / CLI / Web)     │
                         └──────────────┬────────────────┘
                                        │
           ┌────────────────────────────┼────────────────────────────┐
           ▼                            ▼                            ▼
 ┌───────────────────┐        ┌───────────────────┐        ┌───────────────────┐
 │   Facebook / FB   │        │   LinkedIn / OCC  │        │CT / GD / JR / JS  │
 │ (core/facebook...)│        │(core/linkedin...) │        │(core/jobsora_sc..)│
 └─────────┬─────────┘        └─────────┬─────────┘        └─────────┬─────────┘
           │                            │                            │
[Oficiales & Cotizaciones]      [Ofertas en Vivo]           [Extracción Datos]
           │                            │                            │
           └────────────────────────────┼────────────────────────────┘
                                        │
                                        ▼
       ┌───────────────────────────────────────────────────────────┐
       │             Base de Datos (SQLite / jobs.db)              │
       │      - Vacantes y Cotizaciones (8 Canales Laborales)      │
       │      - Métricas Diarias (applied_at, status, modality)    │
       │      - Historial de Cotizaciones y Notas de Seguimiento   │
       └────────────────────────────┬──────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │    Notificaciones WhatsApp    │
                    │  (core/notifier_whatsapp.py)  │
                    └───────────────────────────────┘
```

---

## 📂 Estructura del Proyecto

```plaintext
app_busca_trabajo/
├── config/
│   ├── __init__.py
│   ├── settings.py              # Configuraciones generales, variables .env y rutas
│   └── keywords.json            # Palabras clave (RF, Eléctrica, Oficial Eléctrico, Medio Oficial, Sistemas)
├── core/
│   ├── __init__.py
│   ├── database.py              # SQLite (jobs.db), métricas diarias, filtros y exportaciones
│   ├── data_extractor.py        # Parser inteligente (Puesto, Teléfono, Salario, Modalidad)
│   ├── occ_bot.py               # Automatizador y scraper para OCC Mundial
│   ├── linkedin_scraper.py      # Scraper de ofertas en tiempo real en LinkedIn
│   ├── computrabajo_scraper.py  # Scraper de ofertas en tiempo real en CompuTrabajo
│   ├── glassdoor_scraper.py     # Scraper de ofertas y sueldos en Glassdoor
│   ├── jobrapido_scraper.py     # Scraper de ofertas en Jobrapido
│   ├── jobleads_scraper.py      # Scraper de ofertas ejecutivas en JobLeads
│   ├── jobsora_scraper.py       # Scraper de ofertas en Jobsora
│   ├── facebook_scraper.py      # Scraper de solicitudes, Oficiales Eléctricos y cotizaciones en Facebook
│   └── notifier_whatsapp.py     # Generador de enlaces y cotizaciones para WhatsApp
├── data/
│   ├── cv/                      # Almacenamiento de CVs en PDF
│   ├── exports/                 # Reportes generados en Excel (.xlsx) / CSV
│   └── jobs.db                  # Base de datos local SQLite con índices
├── ui/
│   ├── __init__.py
│   └── app.py                   # Dashboard interactivo con 5 pestañas en Streamlit
├── main.py                      # Lanzador unificado por línea de comandos (CLI)
├── .env.example                 # Plantilla de variables de entorno
├── .gitignore                   # Archivos ignorados por Git
├── requirements.txt             # Dependencias de Python
└── README.md                    # Documentación técnica completa
```

---

## ⚙️ Requisitos Previos

- **Python 3.10+** (probado y 100% compatible con Python 3.14 en Windows/Linux/macOS).
- Navegador web moderno (Chrome, Edge, Firefox, Brave).
- Conexión a Internet para la consulta en vivo de vacantes.

---

## 🚀 Instalación y Puesta en Marcha

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/GhostLT/app_busca_trabajo.git
   cd app_busca_trabajo
   ```

2. **Crear y activar un entorno virtual:**
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

5. **Iniciar la aplicación:**
   ```bash
   python main.py
   # O directamente con Streamlit:
   streamlit run ui/app.py
   ```
   *Accede desde tu navegador en **[http://localhost:8501](http://localhost:8501)**.*

---

## 🖥️ Guía de Uso (CLI)

```bash
# Iniciar la interfaz web gráfica (Streamlit)
python main.py

# Escanear Oficiales Eléctricos, Medio Oficiales y cotizaciones en Facebook
python main.py --fb

# Escanear TODAS las 8 plataformas simultáneamente
python main.py --all

# Escanear plataformas individuales
python main.py --linkedin       # LinkedIn México
python main.py --occ            # OCC Mundial
python main.py --computrabajo   # CompuTrabajo México (alias: --ct)
python main.py --glassdoor      # Glassdoor México (alias: --gd)
python main.py --jobrapido      # Jobrapido México (alias: --jr)
python main.py --jobleads       # JobLeads México (alias: --jl)
python main.py --jobsora        # Jobsora México (alias: --js)

# Ver estadísticas de la base de datos
python main.py --stats

# Exportar reporte a Excel (.xlsx) y CSV
python main.py --export

# Cargar vacantes de demostración
python main.py --seed
```

---

## 💬 Plantilla de Mensaje de Cotización y Contacto

Al pulsar el botón **"💬 Cotizar por WhatsApp"** en cualquier solicitud de obra, se abre directamente la conversación con una propuesta formal:

> *"¡Hola **[Nombre del Contacto]**! Buen día. Espero que se encuentre muy bien.*  
> *Vi su solicitud en Facebook requiriendo **[Oficial Eléctrico / Medio Oficial / Instalación Eléctrica]** en **[Ubicación]**.*  
> *Somos especialistas en **instalaciones eléctricas, canalizaciones con tubería conduit PG, cableado de fuerza, armado de tableros y subestaciones** bajo la norma NOM-001-SEDE.*  
> *Con gusto podemos proporcionarle personal calificado o realizar el levantamiento técnico para enviarle una **cotización formal y presupuesto detallado**.*  
> *¿Me podría compartir más detalles del trabajo o la dirección de la obra? ¡Quedo a sus órdenes!"*

---

## 🔮 Próximas Mejoras

- [ ] Generador automático de presupuestos en PDF con membrete personalizado.
- [ ] Integración con modelos de lenguaje (Gemini / Claude) para análisis de compatibilidad y generación de memorias de cálculo.
- [ ] Notificaciones automáticas por WhatsApp Cloud API / Webhooks.

---

**Desarrollado para automatizar la prospección, cotización y contratación en Ingeniería, Obras y Puestos de Oficial Eléctrico y Medio Oficial.**