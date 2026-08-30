# 🚀 AutoJob Hunter & Tracker (OCC & Redes Sociales)

Sistema integral de automatización para la **búsqueda, extracción, seguimiento y postulación automática** a vacantes de empleo en plataformas laborales (**OCC Mundial**) y redes sociales (**Facebook / Grupos de Empleo**), enfocado en perfiles estratégicos de ingeniería:

- 📡 **Ingeniero de RF / Optimización / Telecomunicaciones**
- ⚡ **Ingeniero Eléctrico / Media y Alta Tensión / Subestaciones**
- 💻 **Ingeniero de Sistemas / Software / DevOps / Cloud**

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
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

### 1. 💼 Módulo OCC Mundial (Postulación y Registro)
- **Búsqueda Automatizada:** Filtrado por roles clave (*Ingeniero de RF*, *Optimización 4G/5G*, *Ingeniero Eléctrico*, *Ingeniero de Sistemas*).
- **Extracción de Detalles:** Captura puesto, empresa, sueldo ofertado, ubicación, modalidad (Remoto, Híbrido, Presencial) y descripción completa.
- **Subida de CV Automática:** Carga automática y gestión de tu currículum (`data/cv/mi_cv.pdf`).
- **Historial de Postulaciones:** Guarda de manera persistente el estado de la solicitud en base de datos SQLite (`Pendiente`, `Postulado`, `En Entrevista`, `Descartado`).

### 2. 📱 Módulo de Redes Sociales (Facebook Job Scraper & Extractor)
- **Escaneo de Grupos y Páginas de Empleo:** Rastreo inteligente de publicaciones laborales en Facebook y grupos de ingeniería.
- **Extractor Inteligente de Texto (NLP / Regex):**
  - 🏷️ **Nombre de la Posición** / Vacante
  - 📞 **Teléfono de Contacto** / WhatsApp del reclutador (formato mexicano `+52`)
  - 📍 **Dirección** / Ubicación / Modalidad
  - 💰 **Salario Ofertado** (rangos mensuales, netos/brutos)
- **Pegado Rápido de Ofertas:** Permite pegar cualquier texto de un post de Facebook, LinkedIn o WhatsApp para extraer los datos y guardarlos con 1 clic.

### 3. 📲 Contacto Directo por WhatsApp
- **Generador de Enlaces `wa.me`:** Creación automática de enlaces directos al WhatsApp del reclutador con mensaje de presentación profesional personalizado según la especialidad de ingeniería.
- **Alertas y Resúmenes:** Formato listo para enviar postulaciones inmediatas.

### 4. 📊 Panel Visual e Interactividad (Streamlit)
- Métricas en tiempo real: total de vacantes, postulaciones activas, promedio salarial y distribución por especialidad/fuente.
- Filtros interactivos por tecnología, modalidad, sueldo y contacto telefónico.
- Exportación instantánea a **Excel (`.xlsx`)** y **CSV** con un solo clic.

---

## 🛠️ Arquitectura del Sistema

```
                        ┌───────────────────────────────┐
                        │        Panel de Control       │
                        │    (Streamlit / CLI / Web)    │
                        └──────────────┬────────────────┘
                                       │
                 ┌─────────────────────┴─────────────────────┐
                 ▼                                           ▼
      ┌─────────────────────┐                     ┌─────────────────────┐
      │   Bot OCC Mundial   │                     │  Bot Redes Sociales │
      │  (core/occ_bot.py)  │                     │(core/facebook_sc...)│
      └──────────┬──────────┘                     └──────────┬──────────┘
                 │                                           │
       [Postulación + CV]                            [Extracción Datos]
                 │                                           │
                 ▼                                           ▼
      ┌───────────────────────────────────────────────────────────┐
      │             Base de Datos (SQLite / jobs.db)              │
      │      - Vacantes Encontradas                               │
      │      - Historial de Postulaciones y Notas                 │
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
│   ├── settings.py           # Configuraciones generales, variables .env y rutas
│   └── keywords.json         # Palabras clave por especialidad (RF, Eléctrica, Sistemas)
├── core/
│   ├── __init__.py
│   ├── database.py           # Gestión de SQLite (jobs.db), filtros y exportaciones
│   ├── data_extractor.py     # Parser de información (Puesto, Teléfono, Salario, Ubicación)
│   ├── occ_bot.py            # Automatizador y scraper para OCC Mundial
│   ├── facebook_scraper.py   # Scraper y extractor de vacantes en Facebook
│   └── notifier_whatsapp.py  # Integración de mensajes y enlaces para WhatsApp
├── data/
│   ├── cv/                   # Carpeta para almacenar tus CVs (PDF / Word)
│   ├── exports/              # Reportes generados en Excel (.xlsx) / CSV
│   └── jobs.db               # Base de datos local SQLite
├── ui/
│   ├── __init__.py
│   └── app.py                # Interfaz gráfica de usuario en Streamlit
├── main.py                   # Lanzador unificado por línea de comandos (CLI)
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Archivos ignorados por Git
├── requirements.txt          # Dependencias de Python
└── README.md                 # Documentación del proyecto
```

---

## ⚙️ Requisitos Previos

- **Python 3.10+** (probado y compatible con Python 3.14).
- Navegador web moderno (Chrome, Edge, Firefox).
- Cuenta activa en **OCC Mundial** y/o **Facebook** *(opcional para personalización)*.

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

4. **Configurar el archivo de entorno (`.env`):**
   ```bash
   # Copiar plantilla base
   cp .env.example .env
   ```

5. **Colocar tu Curriculum Vitae:**
   - Guarda tu archivo CV en formato PDF dentro de `data/cv/mi_cv.pdf` o súbelo directamente desde la pestaña **"Mi CV & Perfil"** en la interfaz web.

---

## 🔐 Variables de Entorno (`.env`)

```ini
# --- Credenciales OCC Mundial ---
OCC_EMAIL=tu_correo@ejemplo.com
OCC_PASSWORD=tu_contraseña_occ

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

## 🖥️ Guía de Uso

El sistema cuenta con un punto de entrada centralizado en `main.py` y soporte para ejecución de módulos independientes:

### 1. Iniciar el Panel Visual (Dashboard):
```bash
python main.py
# O alternativamente:
streamlit run ui/app.py
```
*Abre automáticamente la aplicación en [http://localhost:8501](http://localhost:8501).*

### 2. Ejecutar búsqueda y postulación en OCC Mundial (CLI):
```bash
python main.py --occ
# O mediante módulo:
python -m core.occ_bot
```
*Busca vacantes acordes a tus especialidades en OCC Mundial y las registra en la base de datos.*

### 3. Escanear ofertas de empleo en Facebook (CLI):
```bash
python main.py --fb
# O mediante módulo:
python -m core.facebook_scraper
```
*Extrae publicaciones de grupos de empleo de ingeniería y parsea teléfonos, sueldos y ubicación.*

### 4. Consultar estadísticas de la base de datos:
```bash
python main.py --stats
```

### 5. Exportar reporte de vacantes a Excel y CSV:
```bash
python main.py --export
```

### 6. Cargar vacantes de demostración:
```bash
python main.py --seed
```

---

## 🌐 Panel de Control Web (Streamlit)

La interfaz web organizada por pestañas incluye:

| Pestaña | Funcionalidad |
| :--- | :--- |
| **📊 Dashboard** | KPIs de vacantes encontradas, postulaciones activas, sueldo promedio y gráficos interactivos por especialidad y modalidad. |
| **💼 Bolsa de Vacantes** | Buscador y filtros dinámicos (Especialidad, Estado, Fuente, Sueldo, Teléfono). Tarjetas con botón directo para **Chatear por WhatsApp**, cambiar estado y agregar notas. |
| **🔍 Scraping & Extracción** | Botón para escaneo en vivo de OCC y Facebook + caja de texto para pegar posts de redes sociales y extraer sus datos al instante. |
| **📄 Mi CV & Perfil** | Subida y actualización de CV en PDF, vista previa de datos y personalización del mensaje de presentación para WhatsApp. |
| **⚙️ Configuración & Exportación** | Descarga en 1 clic de reportes en **Excel (`.xlsx`)** y **CSV**, editor de variables `.env` y visor de palabras clave `keywords.json`. |

---

## 📊 Estructura de Datos Extraídos

Las vacantes se registran en SQLite (`data/jobs.db`) con el siguiente esquema:

| Campo | Tipo | Descripción | Ejemplo |
| :--- | :--- | :--- | :--- |
| `title` | TEXT | Nombre del puesto | `Ingeniero de Optimización RF (4G/5G)` |
| `company` | TEXT | Empresa o grupo contratante | `Huawei Partner / OCC Mundial` |
| `category` | TEXT | Especialidad de ingeniería | `Ingeniero de RF / Optimización` |
| `source` | TEXT | Plataforma de origen | `OCC` / `Facebook` |
| `location` | TEXT | Ciudad o estado | `Ciudad de México (Santa Fe)` |
| `modality` | TEXT | Modalidad de trabajo | `Híbrido` / `Remoto` / `Presencial` |
| `salary_raw` | TEXT | Sueldo ofertado | `$35,000 - $45,000 MXN mensuales` |
| `phone` | TEXT | Teléfono normalizado | `+525541829301` |
| `whatsapp_url`| TEXT | Enlace directo con mensaje | `https://wa.me/525541829301?text=...` |
| `status` | TEXT | Estado del seguimiento | `Pendiente` / `Postulado` / `Entrevista` |

---

## 📲 Integración con WhatsApp

Al pulsar el botón **"💬 WhatsApp"** en cualquier vacante, el sistema abre la conversación con un mensaje redactado profesionalmente para reclutadores mexicanos:

> *"¡Hola! Buen día. Espero que te encuentres muy bien.*  
> *Te contacto con respecto a la vacante de **Ingeniero de Optimización RF** para **Empresa**.*  
> *Cuento con experiencia en ingeniería de RF, optimización RAN (4G/5G), Drive Test y herramientas como TEMS/Atoll.*  
> *Me interesa mucho la posición y postularme formalmente. ¿Sigue disponible? Con gusto te comparto mi CV detallado.*  
> *¡Muchas gracias!"*

---

## 🔮 Próximas Mejoras

- [ ] Integración con modelos de lenguaje (Gemini / Claude) para análisis de compatibilidad CV vs. Requisitos.
- [ ] Soporte para scraping directo en LinkedIn y Computrabajo.
- [ ] Respuestas automáticas vía WhatsApp Cloud API / Webhooks.
- [ ] Programador de tareas cron en segundo plano para escaneo periódico nocturno.

---

**Desarrollado con ❤️ para automatizar la búsqueda de empleo en Ingeniería.**