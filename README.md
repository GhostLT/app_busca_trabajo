# 🚀 AutoJob Hunter & Tracker (OCC & Redes Sociales)

Sistema integral de automatización para la búsqueda, extracción y postulación automática a vacantes de empleo en plataformas laborales (**OCC Mundial**) y redes sociales (**Facebook**), enfocado en perfiles de ingeniería:
- 📡 **Ingeniero de RF / Optimización**
- ⚡ **Ingeniero Eléctrico**
- 💻 **Ingeniero de Sistemas / Software**

---

## 📋 Tabla de Contenidos
- [Características Principales](#-características-principales)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Variables de Entorno (.env)](#-variables-de-entorno-env)
- [Guía de Uso](#-guía-de-uso)
- [Estructura de Datos Extraídos](#-estructura-de-datos-extraídos)
- [Próximas Mejoras](#-próximas-mejoras)

---

## ✨ Características Principales

### 1. 💼 Módulo OCC Mundial (Postulación y Registro)
- **Búsqueda Automatizada:** Filtrado por roles clave (*Ingeniero de RF*, *Optimización*, *Ingeniero Eléctrico*, *Ingeniero de Sistemas*).
- **Subida de CV Automática:** Carga automática de tu currículum (PDF/Word) en cada postulación.
- **Historial de Postulaciones:** Guarda de manera persistente el nombre de la posición, empresa, fecha, enlace y estado de la solicitud.
- **Contacto por WhatsApp:** Envío de alertas y confirmaciones a tu WhatsApp personal ante postulaciones exitosas o contacto de reclutadores.

### 2. 📱 Módulo de Redes Sociales (Facebook Job Scraper & Extractor)
- **Escaneo de Grupos y Páginas de Empleo:** Rastreo inteligente de publicaciones laborales en Facebook.
- **Extracción de Datos Clave (NLP / Regex / IA):**
  - 🏷️ **Nombre de la Posición** / Vacante
  - 📞 **Teléfono de Contacto** / WhatsApp del reclutador
  - 📍 **Dirección** / Ubicación / Modalidad (Remoto, Híbrido, Presencial)
  - 💰 **Salario Posible** / Rango Salarial ofertado
- **Generación de Listados:** Exportación automática a base de datos (SQLite), Excel (`.xlsx`) y CSV.

### 3. 📲 Notificaciones en WhatsApp
- Alertas en tiempo real cuando se detecta una vacante de alto interés o cuando un reclutador responde.
- Enlace directo con un solo clic para contactar al reclutador por WhatsApp.

---

## 🛠️ Arquitectura del Sistema

```
                        ┌───────────────────────────────┐
                        │        Panel de Control       │
                        │    (Streamlit / CLI / Web)    │
                        └──────────────┬────────────────┘
                                       │
                ┌──────────────────────┴──────────────────────┐
                ▼                                             ▼
     ┌─────────────────────┐                       ┌─────────────────────┐
     │   Bot OCC Mundial   │                       │  Bot Redes Sociales │
     │  (Selenium / API)   │                       │     (Facebook)      │
     └──────────┬──────────┘                       └──────────┬──────────┘
                │                                             │
      [Postulación + CV]                              [Extracción Datos]
                │                                             │
                ▼                                             ▼
     ┌───────────────────────────────────────────────────────────┐
     │             Base de Datos (SQLite / PostgreSQL)           │
     │      - Vacantes Encontradas                               │
     │      - Historial de Postulaciones                         │
     └─────────────────────────────┬─────────────────────────────┘
                                   │
                                   ▼
                   ┌───────────────────────────────┐
                   │    Notificaciones WhatsApp    │
                   │    (Twilio / WhatsApp API)    │
                   └───────────────────────────────┘
```

---

## 📂 Estructura del Proyecto

```plaintext
app_busca_trabajo/
├── config/
│   ├── settings.py           # Configuraciones generales y constantes
│   └── keywords.json         # Palabras clave por especialidad (RF, Eléctrica, Sistemas)
├── core/
│   ├── occ_bot.py            # Automatizador y postulador para OCC Mundial
│   ├── facebook_scraper.py   # Scraper y extractor de vacantes en Facebook
│   ├── data_extractor.py     # Parser de información (Puesto, Teléfono, Salario, Ubicación)
│   ├── notifier_whatsapp.py  # Integración de mensajes y alertas a WhatsApp
│   └── database.py           # Gestión de base de datos SQLite y exportaciones
├── data/
│   ├── cv/                   # Carpeta para almacenar tus CVs (PDF)
│   ├── exports/              # Reportes generados en Excel / CSV
│   └── jobs.db               # Base de datos local
├── ui/
│   └── app.py                # Interfaz gráfica opcional (Streamlit)
├── .env.example              # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt          # Dependencias de Python
└── README.md                 # Documentación del proyecto
```

---

## ⚙️ Requisitos Previos

- **Python 3.10+** instalado en el sistema.
- **Google Chrome** o navegador compatible con WebDriver.
- Cuenta activa en **OCC Mundial** y **Facebook**.
- *(Opcional)* Cuenta o credenciales para API de WhatsApp (Twilio / WhatsApp Cloud API / pywhatkit).

---

## 🚀 Instalación y Configuración

1. **Clonar o descargar el repositorio:**
   ```bash
   cd c:\proyectos\app_busca_trabajo
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   .\venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Colocar tu Curriculum Vitae (CV):**
   - Guarda tu archivo en `data/cv/mi_cv.pdf`.

---

## 🔐 Variables de Entorno (`.env`)

Crea un archivo `.env` en la raíz del proyecto a partir de `.env.example`:

```ini
# --- Credenciales OCC Mundial ---
OCC_EMAIL=tu_correo@ejemplo.com
OCC_PASSWORD=tu_contraseña_occ

# --- Credenciales Facebook ---
FB_EMAIL=tu_correo_facebook@ejemplo.com
FB_PASSWORD=tu_contraseña_facebook

# --- Configuración de WhatsApp ---
USER_WHATSAPP_PHONE=+52XXXXXXXXXX
WHATSAPP_API_KEY=tu_api_key_opcional

# --- Perfil y CV ---
CV_PATH=data/cv/mi_cv.pdf
TARGET_ROLES="Ingeniero de RF, Ingeniero de Optimización, Ingeniero Eléctrico, Ingeniero de Sistemas"
```

---

## 🖥️ Guía de Uso

### 1. Ejecutar búsqueda y postulación en OCC Mundial:
```bash
python -m core.occ_bot
```
*El bot iniciará sesión, buscará vacantes acordes a tus áreas de ingeniería, subirá tu CV y registrará la posición en la base de datos.*

### 2. Escanear ofertas de empleo en Facebook:
```bash
python -m core.facebook_scraper
```
*Extraerá publicaciones de grupos de empleo y generará la lista de vacantes con teléfono, sueldo y ubicación.*

### 3. Iniciar el Panel Visual (Dashboard):
```bash
streamlit run ui/app.py
```
*Permite ver en tiempo real las vacantes encontradas, filtrar por sueldo o ubicación, postular con un clic y contactar a reclutadores por WhatsApp.*

---

## 📊 Estructura de Datos Extraídos

Las vacantes encontradas en Facebook y OCC se almacenan con el siguiente esquema:

| Campo | Descripción | Ejemplo |
| :--- | :--- | :--- |
| **Puesto / Posición** | Título de la vacante | `Ingeniero de Optimización RF Jr/Sr` |
| **Empresa / Fuente** | Empresa contratante o grupo | `OCC / Grupo Facebook Ingenieros México` |
| **Teléfono de Contacto** | Número o enlace directo a WhatsApp | `+52 55 1234 5678` |
| **Dirección / Ubicación**| Ciudad, estado o modalidad | `Ciudad de México / Híbrido` |
| **Salario Estimado** | Rango o sueldo mensual propuesto | `$25,000 - $35,000 MXN` |
| **Fecha de Registro** | Timestamp de extracción | `2026-08-30 10:30:00` |
| **Estado** | Estado de la postulación | `Postulado` / `Pendiente de Contacto` |

---

## 🔮 Próximas Mejoras
- [ ] Integración con modelos de lenguaje (LLMs / Gemini) para análisis semántico del CV vs. Requisitos de la vacante.
- [ ] Auto-redacción de cartas de presentación personalizadas.
- [ ] Soporte para LinkedIn y CompuTrabajo.
- [ ] Bot conversacional de WhatsApp para respuesta automática a reclutadores.
