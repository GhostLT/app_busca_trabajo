# 🚀 AutoJob Hunter & Tracker (OCC, LinkedIn, CompuTrabajo & Redes Sociales)

Sistema integral de automatización para la **búsqueda, extracción, análisis estadístico y postulación automática** a vacantes de empleo en las principales plataformas laborales (**OCC Mundial**, **LinkedIn**, **CompuTrabajo**) y redes sociales (**Facebook / Grupos de Empleo**), enfocado en perfiles estratégicos de ingeniería:

- 📡 **Ingeniero de RF / Optimización / Telecomunicaciones (4G/5G/RAN/MW)**
- ⚡ **Ingeniero Eléctrico / Media y Alta Tensión / Subestaciones / NOM-001**
- 💻 **Ingeniero de Sistemas / Software / DevOps / Cloud / Python**

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
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

### 1. 📊 Dashboard de Estadísticas y Control Diario de Postulaciones
- **Monitoreo de Postulaciones Diarias:** Registro cronológico exacto de la fecha y hora (`applied_at`) en que te postulas a cada vacante.
- **Métricas de Rendimiento:** KPIs en tiempo real para postulaciones de **Hoy**, **Esta Semana (7 días)**, **Este Mes** y **Total Histórico**.
- **Tasa de Conversión a Entrevistas:** Cálculo automático del porcentaje de éxito entre postulaciones realizadas y entrevistas conseguidas (`% de Conversión`).
- **Gráfica de Ritmo Diario:** Visualización en gráfico de barras de las postulaciones acumuladas por día y promedio de ritmo diario.
- **Desglose Multidimensional:** Gráficas comparativas de postulaciones por plataforma (*LinkedIn*, *OCC*, *CompuTrabajo*, *Facebook*), por especialidad y por modalidad de trabajo (*Remoto*, *Híbrido*, *Presencial*).
- **Historial Completo de Postulaciones:** Tabla interactiva para dar seguimiento a cada vacante aplicada con su estado, fecha, contacto y notas.

### 2. 🟧 Módulo CompuTrabajo México (Búsqueda y Extracción en Vivo)
- **Extracción Directa:** Conexión con `mx.computrabajo.com` para capturar en tiempo real las ofertas publicadas para ingenieros.
- **Extracción de Salarios y Modalidad:** Parser inteligente para rangos salariales, ciudades (*CDMX, Guadalajara, Monterrey, Querétaro, etc.*) y esquemas de trabajo.
- **Enlace Limpio a la Oferta:** Enlace directo para postulación inmediata.

### 3. 🌐 Módulo LinkedIn Jobs (Búsqueda en Tiempo Real)
- **Extracción en Vivo:** Conexión con el buscador público de LinkedIn México para capturar vacantes de ingeniería en empresas líderes (Ericsson, Huawei, Qualcomm, Schneider Electric, Kiewit, etc.).
- **Detección Automática de Modalidad:** Identifica esquemas *Remoto*, *Híbrido* o *Presencial*.
- **Enlace Directo:** Guarda la URL limpia de la vacante para postularte con un solo clic.

### 4. 💼 Módulo OCC Mundial (Postulación y Registro)
- **Búsqueda Automatizada:** Filtrado por roles clave (*Ingeniero de RF*, *Optimización 4G/5G*, *Ingeniero Eléctrico*, *Ingeniero de Sistemas*).
- **Extracción de Detalles:** Captura puesto, empresa, sueldo ofertado, ubicación, modalidad y descripción completa.
- **Subida de CV Automática:** Carga automática y gestión de tu currículum (`data/cv/mi_cv.pdf`).
- **Historial de Postulaciones:** Guarda de manera persistente el estado de la solicitud en base de datos SQLite (`Pendiente`, `Postulado`, `Entrevista`, `Descartado`).

### 5. 📱 Módulo de Redes Sociales (Facebook Job Scraper & Extractor)
- **Escaneo de Grupos y Páginas de Empleo:** Rastreo inteligente de publicaciones laborales en Facebook y grupos de ingeniería en México.
- **Extractor Inteligente de Texto (NLP / Regex):**
  - 🏷️ **Nombre de la Posición** / Vacante
  - 📞 **Teléfono de Contacto** / WhatsApp del reclutador (formato `+52`)
  - 📍 **Dirección** / Ubicación / Modalidad
  - 💰 **Salario Ofertado** (rangos mensuales, netos/brutos)
- **Pegado Rápido de Ofertas:** Permite pegar cualquier texto de un post de Facebook, LinkedIn o WhatsApp para extraer los datos y guardarlos con 1 clic.

### 6. 📲 Contacto Directo por WhatsApp
- **Generador de Enlaces `wa.me`:** Creación automática de enlaces directos al WhatsApp del reclutador con mensaje de presentación profesional personalizado según la especialidad de ingeniería.

### 7. 🎛️ Bolsa de Vacantes con Filtros Avanzados y Gestión de Estado
- **Filtro por Plataforma:** Selector para filtrar instantáneamente entre **LinkedIn**, **OCC Mundial**, **CompuTrabajo** y **Redes Sociales (Facebook)**.
- **Filtro por Ciudad / Ubicación:** Búsqueda inteligente por ciudad con soporte para alias locales (*CDMX, Guadalajara/GDL, Monterrey/MTY, Querétaro/Qro, etc.*).
- **Formulario con Botón de Aplicar:** Panel de control de filtros con botón interactivo `🔍 Aplicar Filtros`.
- **Botones de Estado Sincronizados:** Los botones `⬜ Postularme` y `🎯 Entrevista` inician sin seleccionar por defecto; al hacer clic, se actualiza la base de datos en tiempo real y cambian a `✅ Postulado` o `🟣 En Entrevista`.
- **Exportación de Datos:** Descarga de reportes completos en **Excel (`.xlsx`)** y **CSV** con columnas para `modality`, `phone`, `whatsapp_url` y `applied_at`.

---

## 📈 Nuevo Dashboard de Estadísticas y Postulaciones Diarias

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
 │ [Barras por Fecha YYYY-MM-DD]            │    │ - Por Plataforma (LinkedIn / OCC / CT...)│
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
 │  Bot OCC Mundial  │        │  Scraper LinkedIn │        │Bot CompuTrabajo/FB│
 │ (core/occ_bot.py) │        │(core/linkedin_...)│        │(core/computrab...)│
 └─────────┬─────────┘        └─────────┬─────────┘        └─────────┬─────────┘
           │                            │                            │
  [Postulación + CV]            [Ofertas en Vivo]           [Extracción Datos]
           │                            │                            │
           └────────────────────────────┼────────────────────────────┘
                                        │
                                        ▼
       ┌───────────────────────────────────────────────────────────┐
       │             Base de Datos (SQLite / jobs.db)              │
       │      - Vacantes (OCC / LinkedIn / CompuTrabajo / FB)      │
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

# Escanear vacantes en LinkedIn México
python main.py --linkedin

# Escanear vacantes en CompuTrabajo México
python main.py --computrabajo

# Escanear vacantes en OCC Mundial
python main.py --occ

# Escanear publicaciones en Facebook
python main.py --fb

# Ver estadísticas rápidas en terminal
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
| **💼 Bolsa de Vacantes** | Buscador por texto, filtro por ciudad/ubicación, filtro por plataforma (**LinkedIn, OCC, CompuTrabajo, Redes Sociales**), especialidad, estado y modalidad con botón **`🔍 Aplicar Filtros`**. Botones de postulación interactiva `⬜ Postularme` y `🎯 Entrevista`, y enlace directo a WhatsApp. |
| **🔍 Scraping & Extracción** | 4 Paneles de escaneo en tiempo real (**LinkedIn Jobs**, **CompuTrabajo**, **OCC Mundial**, **Facebook**) + caja inteligente para pegar y extraer cualquier oferta laboral. |
| **📄 Mi CV & Perfil** | Gestor de archivo de CV (PDF/Word), vista previa de perfil profesional y editor de plantillas de mensaje para WhatsApp. |
| **⚙️ Configuración & Exportación** | Descarga en 1 clic de reportes en **Excel (`.xlsx`)** y **CSV** con `modality`, `phone`, `whatsapp_url` y `applied_at`, editor de credenciales `.env` y visor de palabras clave JSON. |

---

## 📊 Estructura de Datos Extraídos

| Campo | Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| `title` | TEXT | Nombre del puesto | `Senior RF & Antenna Design Engineer` |
| `company` | TEXT | Empresa o reclutador | `Qualcomm México / Schneider Electric` |
| `category` | TEXT | Especialidad de ingeniería | `Ingeniero de RF / Optimización` |
| `source` | TEXT | Plataforma de origen | `CompuTrabajo` / `LinkedIn` / `OCC` / `Facebook` |
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