# 🚀 AutoJob Hunter & Tracker (OCC, LinkedIn, CompuTrabajo, Glassdoor, Jobrapido, JobLeads & Redes)

Sistema integral de automatización multiplataforma para la **búsqueda, extracción, análisis estadístico y postulación automática** a vacantes de empleo en las 7 plataformas laborales líderes en México (**LinkedIn**, **OCC Mundial**, **CompuTrabajo**, **Glassdoor**, **Jobrapido**, **JobLeads**) y redes sociales (**Facebook / Grupos de Empleo**), enfocado en perfiles estratégicos de ingeniería:

- 📡 **Ingeniero de RF / Optimización / Telecomunicaciones (4G/5G/RAN/MW)**
- ⚡ **Ingeniero Eléctrico / Media y Alta Tensión / Subestaciones / NOM-001**
- 💻 **Ingeniero de Sistemas / Software / DevOps / Cloud / Python**

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Plataformas de Empleo Integradas (7 Canales)](#-plataformas-de-empleo-integradas-7-canales)
- [Nuevo Dashboard de Estadísticas y Postulaciones Diarias](#-nuevo-dashboard-de-estadísticas-y-postulaciones-diarias)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
- [Variables de Entorno (.env)](#-variables-de-entorno-env)
- [Guía de Uso (CLI y Dashboard)](#-guía-de-uso)
- [Panel de Control Web (Streamlit)](#-panel-de-control-web-streamlit)
- [Estructura de Datos Extraídos](#-estructura-de-datos-extraídos)
- [Integración con WhatsApp](#-integración-con-whatsapp)
- [Próximas Mejoras](#-próximas-mejoras)

---

## ✨ Características Principales

### 1. 🌐 Rastreo y Extracción Multiplataforma (7 Portales)
Conexión en tiempo real con los principales portales de empleo de México:
- 💼 **LinkedIn Jobs México:** Búsqueda en vivo de ofertas públicas de ingeniería en corporativos globales.
- 🌐 **OCC Mundial:** Extracción de vacantes, filtrado avanzado y postulación con CV.
- 🟧 **CompuTrabajo:** Captura de ofertas técnicas e industriales en todo el territorio nacional.
- 🟢 **Glassdoor México:** Extracción de vacantes con estimaciones salariales y valoración de empresa.
- 🌐 **Jobrapido México:** Agregador masivo de vacantes de ingeniería y telecomunicaciones.
- 🎯 **JobLeads México:** Portal especializado en posiciones Senior, Lead y Arquitectos de ingeniería.
- 📱 **Redes Sociales (Facebook):** Escaneo inteligente en grupos de empleo y bolsa de trabajo.

### 2. 📊 Dashboard de Estadísticas y Control Diario de Postulaciones
- **Monitoreo de Postulaciones Diarias:** Registro cronológico exacto de la fecha y hora (`applied_at`) en que te postulas a cada vacante.
- **Métricas de Rendimiento:** KPIs en tiempo real para postulaciones de **Hoy**, **Esta Semana (7 días)**, **Este Mes** y **Total Histórico**.
- **Tasa de Conversión a Entrevistas:** Cálculo automático del porcentaje de éxito entre postulaciones realizadas y entrevistas conseguidas (`% de Conversión`).
- **Gráfica de Ritmo Diario:** Visualización cronológica en barras de las postulaciones acumuladas por día y promedio de ritmo diario.
- **Desglose Gráfico Multidimensional:** Gráficas comparativas de postulaciones por plataforma (LinkedIn, OCC, CompuTrabajo, Glassdoor, Jobrapido, JobLeads, Facebook), por especialidad y por modalidad (*Remoto*, *Híbrido*, *Presencial*).
- **Historial Completo de Postulaciones:** Tabla interactiva para dar seguimiento a cada vacante aplicada con su estado, fecha, contacto y notas.

### 3. 🎛️ Bolsa de Vacantes con Filtros y Gestión de Estado
- **Filtro por Plataforma:** Selector rápido para filtrar entre las 7 fuentes laborales.
- **Filtro por Ciudad / Ubicación:** Búsqueda inteligente con resolución de alias locales (*CDMX, Guadalajara/GDL, Monterrey/MTY, Querétaro/Qro, etc.*).
- **Botón de Aplicar Filtros:** Formulario interactivo con botón primario `🔍 Aplicar Filtros`.
- **Botones de Estado Sincronizados:** Los botones `⬜ Postularme` y `🎯 Entrevista` inician sin seleccionar por defecto y actualizan la base de datos en tiempo real al hacer clic (`✅ Postulado` o `🟣 En Entrevista`), permitiendo también desmarcarlos con un segundo clic.
- **Exportación de Datos:** Descarga de reportes completos en **Excel (`.xlsx`)** y **CSV** con columnas para `modality`, `phone`, `whatsapp_url` y `applied_at`.

### 4. 📲 Contacto Directo por WhatsApp
- **Generador de Enlaces `wa.me`:** Creación automática de enlaces directos al WhatsApp del reclutador con mensaje de presentación profesional personalizado según la especialidad de ingeniería.

---

## 🌐 Plataformas de Empleo Integradas (7 Canales)

| Plataforma | Módulo | Enfoque Principal |
| :--- | :--- | :--- |
| **💼 LinkedIn** | `core/linkedin_scraper.py` | Multinacionales de telecomunicaciones, software y manufactura avanzada |
| **🌐 OCC Mundial** | `core/occ_bot.py` | Ofertas corporativas y contratación formal en México con subida de CV |
| **🟧 CompuTrabajo** | `core/computrabajo_scraper.py` | Empleos técnicos, de campo (Drive Test / Planta Externa) e industriales |
| **🟢 Glassdoor** | `core/glassdoor_scraper.py` | Posiciones con insights de compensación salarial y empresas calificadas |
| **🌐 Jobrapido** | `core/jobrapido_scraper.py` | Agregador masivo de vacantes de ingeniería a nivel nacional |
| **🎯 JobLeads** | `core/jobleads_scraper.py` | Puestos ejecutivos, Senior Engineers, Tech Leads y Gerencias Técnicas |
| **📱 Facebook** | `core/facebook_scraper.py` | Reclutadores directos y grupos de empleo de ingeniería en redes |

---

## 📈 Dashboard de Estadísticas y Postulaciones Diarias

La **Pestaña 1 (📊 Estadísticas de Postulaciones)** ofrece un centro de control analítico:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 🎯 Total Postuladas │ 📅 Postuladas Hoy │ 🗓️ Esta Semana │ 📆 Este Mes │ 🟣 En Entrevista │
│        14           │         5         │       12       │     14      │  3 (Éxito: 21.4%) │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
                                               │
               ┌───────────────────────────────┴───────────────────────────────┐
               ▼                                                               ▼
 ┌──────────────────────────────────────────┐    ┌──────────────────────────────────────────┐
 │ 📈 Postulaciones Diarias (Gráfico Tiempo)│    │ 🌐 Desglose de Postulaciones             │
 │ [Barras por Fecha YYYY-MM-DD]            │    │ - Por Plataforma (7 Canales)             │
 │ Promedio diario: 4.2 postulaciones/día   │    │ - Por Especialidad (RF / Elec / Soft)    │
 └──────────────────────────────────────────┘    │ - Por Modalidad (Remoto / Híbrido / Pres)│
                                                 └──────────────────────────────────────────┘
                                               │
                                               ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────┐
 │ 📋 Tabla Detallada de Vacantes Postuladas (Fecha, Empresa, Puesto, Teléfono, WhatsApp,...)│
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
 │   LinkedIn / OCC  │        │ CompuTrabajo / GD │        │Jobrapido / JL / FB│
 │ (core/linkedin...)│        │(core/computrab...)│        │(core/jobrapido...)│
 └─────────┬─────────┘        └─────────┬─────────┘        └─────────┬─────────┘
           │                            │                            │
  [Postulación + CV]            [Ofertas en Vivo]           [Extracción Datos]
           │                            │                            │
           └────────────────────────────┼────────────────────────────┘
                                        │
                                        ▼
       ┌───────────────────────────────────────────────────────────┐
       │             Base de Datos (SQLite / jobs.db)              │
       │      - Vacantes (LinkedIn / OCC / CT / GD / JR / JL / FB) │
       │      - Métricas Diarias (applied_at, status, modality)    │
       │      - Historial de Entrevistas y Notas de Seguimiento    │
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
│   └── keywords.json            # Palabras clave por especialidad (RF, Eléctrica, Sistemas)
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
│   ├── facebook_scraper.py      # Scraper y extractor de vacantes en Facebook
│   └── notifier_whatsapp.py     # Generador de enlaces y mensajes para WhatsApp
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

## 🔐 Variables de Entorno (`.env`)

```ini
# --- Credenciales OCC Mundial ---
OCC_EMAIL=tu_correo@ejemplo.com
OCC_PASSWORD=tu_contraseña_occ

# --- Credenciales LinkedIn ---
LINKEDIN_EMAIL=tu_correo_linkedin@ejemplo.com
LINKEDIN_PASSWORD=tu_contraseña_linkedin

# --- Credenciales CompuTrabajo ---
COMPUTRABAJO_EMAIL=tu_correo_computrabajo@ejemplo.com
COMPUTRABAJO_PASSWORD=tu_contraseña_computrabajo

# --- Credenciales Glassdoor ---
GLASSDOOR_EMAIL=tu_correo_glassdoor@ejemplo.com
GLASSDOOR_PASSWORD=tu_contraseña_glassdoor

# --- Credenciales Jobrapido ---
JOBRAPIDO_EMAIL=tu_correo_jobrapido@ejemplo.com
JOBRAPIDO_PASSWORD=tu_contraseña_jobrapido

# --- Credenciales JobLeads ---
JOBLEADS_EMAIL=tu_correo_jobleads@ejemplo.com
JOBLEADS_PASSWORD=tu_contraseña_jobleads

# --- Credenciales Facebook ---
FB_EMAIL=tu_correo_facebook@ejemplo.com
FB_PASSWORD=tu_contraseña_facebook

# --- Configuración WhatsApp ---
USER_WHATSAPP_PHONE=+52XXXXXXXXXX
WHATSAPP_API_KEY=tu_api_key_opcional

# --- Configuración de Perfil y Archivos ---
CV_PATH=data/cv/mi_cv.pdf
TARGET_ROLES="Ingeniero de RF, Ingeniero de Optimización, Ingeniero Eléctrico, Ingeniero de Sistemas"
```

---

## 🖥️ Guía de Uso (CLI)

```bash
# Iniciar la interfaz web gráfica (Streamlit)
python main.py

# Escanear TODAS las 7 plataformas simultáneamente
python main.py --all

# Escanear plataformas individuales
python main.py --linkedin       # LinkedIn México
python main.py --occ            # OCC Mundial
python main.py --computrabajo   # CompuTrabajo México (alias: --ct)
python main.py --glassdoor      # Glassdoor México (alias: --gd)
python main.py --jobrapido      # Jobrapido México (alias: --jr)
python main.py --jobleads       # JobLeads México (alias: --jl)
python main.py --fb             # Publicaciones en Facebook

# Ver estadísticas de la base de datos
python main.py --stats

# Exportar reporte a Excel (.xlsx) y CSV
python main.py --export

# Cargar vacantes de demostración
python main.py --seed
```

---

## 🌐 Panel de Control Web (Streamlit)

| Pestaña | Funcionalidades Principales |
| :--- | :--- |
| **📊 Estadísticas de Postulaciones** | KPI cards de postulaciones (*Hoy*, *Semana*, *Mes*, *Total*), tasa de conversión a entrevistas, gráfico cronológico de postulaciones diarias, gráficos de desglose por plataforma, especialidad y modalidad, y tabla de vacantes aplicadas. |
| **💼 Bolsa de Vacantes** | Buscador por texto, filtro por ciudad/ubicación, selector de plataforma (**LinkedIn, OCC, CompuTrabajo, Glassdoor, Jobrapido, JobLeads, Facebook**), especialidad, estado y modalidad con botón **`🔍 Aplicar Filtros`**. Botones de postulación interactiva `⬜ Postularme` y `🎯 Entrevista`, y enlace directo a WhatsApp. |
| **🔍 Scraping & Extracción** | Panel de escaneo masivo (7 plataformas con 1 clic) + selectores específicos por portal + caja inteligente para pegar y extraer cualquier publicación. |
| **📄 Mi CV & Perfil** | Gestor de archivo de CV (PDF/Word), vista previa de perfil profesional y editor de plantillas de mensaje para WhatsApp. |
| **⚙️ Configuración & Exportación** | Descarga en 1 clic de reportes en **Excel (`.xlsx`)** y **CSV** con `modality`, `phone`, `whatsapp_url` y `applied_at`, editor de credenciales `.env` y visor de palabras clave JSON. |

---

## 📊 Estructura de Datos Extraídos

| Campo | Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| `title` | TEXT | Nombre del puesto | `Senior RF & Antenna Design Engineer` |
| `company` | TEXT | Empresa o reclutador | `Qualcomm México / Schneider Electric` |
| `category` | TEXT | Especialidad de ingeniería | `Ingeniero de RF / Optimización` |
| `source` | TEXT | Plataforma de origen | `LinkedIn` / `OCC` / `CompuTrabajo` / `Glassdoor` / `Jobrapido` / `JobLeads` / `Facebook` |
| `location` | TEXT | Ciudad o estado | `Ciudad de México / Guadalajara` |
| `modality` | TEXT | Modalidad de trabajo | `Híbrido` / `Remoto` / `Presencial` |
| `salary_raw` | TEXT | Sueldo ofertado | `$45,000 - $65,000 MXN mensuales` |
| `phone` | TEXT | Teléfono normalizado | `+523319024810` |
| `whatsapp_url`| TEXT | Enlace con mensaje predeterminado | `https://wa.me/523319024810?text=...` |
| `status` | TEXT | Estado del seguimiento | `Pendiente` / `Postulado` / `Entrevista` |
| `applied_at` | TEXT | Fecha y hora de postulación | `2026-08-30 13:00:00` |

---

## 📲 Integración con WhatsApp

Al pulsar el botón **"💬 WhatsApp"** en cualquier vacante con teléfono detectado, se abre directamente la conversación con un saludo profesional y personalizado según la disciplina:

> *"¡Hola! Buen día. Espero que te encuentres muy bien.*  
> *Te contacto con respecto a la vacante de **Ingeniero de Optimización RF** para **Empresa**.*  
> *Cuento con experiencia en ingeniería de RF, optimización RAN (4G/5G), Drive Test y herramientas como TEMS/Atoll.*  
> *Me interesa mucho la posición y postularme formalmente. ¿Sigue disponible? Con gusto te comparto mi CV detallado.*  
> *¡Muchas gracias!"*

---

## 🔮 Próximas Mejoras

- [ ] Integración con modelos de lenguaje (Gemini / Claude) para análisis de compatibilidad CV vs. Requisitos de la vacante.
- [ ] Soporte para Indeed México.
- [ ] Automatización de respuestas mediante WhatsApp Cloud API / Webhooks.
- [ ] Programador de tareas cron en segundo plano para escaneo periódico nocturno.

---

**Desarrollado para automatizar y optimizar la búsqueda de empleo en Ingeniería.**