# 🚀 AutoJob Hunter & Tracker (8 Canales Laborales, Frontend Nativo Bootstrap 5 & Bot de WhatsApp)

Sistema integral de automatización multiplataforma para la **búsqueda de empleo, extracción de vacantes, captura de solicitudes de cotizaciones eléctricas y control total remoto desde tu WhatsApp** en las 8 plataformas líderes en México (**Facebook**, **LinkedIn**, **OCC Mundial**, **CompuTrabajo**, **Glassdoor**, **Jobrapido**, **JobLeads**, **Jobsora**).

Cuenta con una **interfaz web moderna desarrollada 100% en HTML5, CSS3, JavaScript puro (Vanilla JS) y Bootstrap 5**, respaldada por una API REST en Flask, **eliminando cualquier dependencia de Streamlit** para un rendimiento ligero, flexible e integrable.

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                            FRONTEND NATIVO (HTML5 + CSS3 + JS)                              │
│             [ Bootstrap 5.3.3 ]  •  [ Bootstrap Icons ]  •  [ Chart.js 4.4.2 ]              │
│      - 📊 Estadísticas Interactivas          - 🔍 Centro de Scraping y Extractor           │
│      - 💼 Explorador de Vacantes / Filtros   - 📄 Perfil, CV y Plantillas en un clic       │
│      - 📱 Simulador de Chat WhatsApp en vivo - ⚙️ Configuración (.env) y Exportación Excel  │
└──────────────────────────────────────────────┬──────────────────────────────────────────────┘
                                               │ Fetch / AJAX (JSON)
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                SERVIDOR WEB & API REST                                      │
│                                    (ui/server.py - Flask)                                   │
│   Endpoints: /api/stats • /api/jobs • /api/whatsapp/simulate • /api/scrapers • /api/export  │
└──────────────┬───────────────────────────────┬───────────────────────────────┬──────────────┘
               │                               │                               │
               ▼                               ▼                               ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐ ┌──────────────────────────────┐
│       BASE DE DATOS          │ │     8 SCRAPERS LABORALES     │ │    WHATSAPP BOT & WEBHOOK    │
│      (core/database.py)      │ │        (core/*_scraper)      │ │   (core/whatsapp_server.py)  │
│ SQLite Local (data/jobs.db)  │ │ FB, LinkedIn, OCC, CT, etc.  │ │ GreenAPI, Meta, Twilio, etc. │
└──────────────────────────────┘ └──────────────────────────────┘ └──────────────────────────────┘
```

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Panel de Control Web (HTML5, CSS3, JS & Bootstrap 5)](#-panel-de-control-web-html5-css3-js--bootstrap-5)
- [Bot Interactivo de WhatsApp](#-módulo-especial-bot-interactivo-de-whatsapp-control-total-desde-tu-celular)
- [Módulo de Obras, Oficiales y Ayudantes Eléctricos](#-módulo-especial-captura-de-obras-clientes-y-categorías-eléctricas)
- [Plataformas de Empleo Integradas (8 Canales)](#-plataformas-de-empleo-integradas-8-canales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
- [Endpoints de la API REST](#-endpoints-de-la-api-rest)
- [Guía de Uso por Terminal (CLI)](#-guía-de-uso-por-terminal-cli)
- [Configuración de Webhook de WhatsApp](#-configuración-de-webhook-de-whatsapp)
- [Plantilla de Mensaje de Cotización](#-plantilla-de-mensaje-de-cotización)

---

## 🌐 Panel de Control Web (HTML5, CSS3, JS & Bootstrap 5)

La interfaz gráfica reemplaza por completo a Streamlit y opera mediante un servidor Flask integrado. Se divide en 6 pestañas operativas:

### 1. 📊 Estadísticas de Postulaciones y Rendimiento
- **Tarjetas KPI en tiempo real:** Total de postulaciones/cotizaciones, gestionadas hoy, última semana, mes en curso y total en trámite/entrevista con porcentaje de conversión.
- **Gráfico de Historial Diario (Chart.js):** Cantidad de gestiones registradas por día calendario con tabla de resumen lateral y cálculo de promedio diario.
- **Gráficos de Desglose:**
  - Desglose por Plataforma (OCC, LinkedIn, CompuTrabajo, Facebook, etc.).
  - Desglose por Especialidad (Eléctrica, RF / Telecomunicaciones, Sistemas / Software).
  - Desglose por Modalidad (Presencial, Híbrido, Remoto).
- **Registro Detallado de Seguimiento:** Tabla con todas las oportunidades marcadas como *Postulado* o *En Cotización / Entrevista*, con acceso directo a llamada y chat de WhatsApp.

### 2. 💼 Bolsa de Vacantes & Cotizaciones de Instalaciones
- **Filtros Avanzados:**
  - Búsqueda por texto (puesto, nombre de cliente, palabras clave).
  - Ubicación geográfica (Ciudad de México, Querétaro, Monterrey, Guadalajara, etc.).
  - Selector de Especialidad.
  - Selector de Plataforma origen (las 8 fuentes integradas).
  - Selector de Estado (Todos, Pendiente, Postulado, Entrevista, Descartado).
  - Modalidad de trabajo.
  - Casilla de verificación *"Solo con Teléfono / WhatsApp"*.
- **Tarjetas de Oportunidades:**
  - Badges semánticos por área, fuente, sueldo/presupuesto y modalidad.
  - Nombre del cliente o contacto directo resaltado.
  - Botón **"💬 WhatsApp Directo"** con mensaje pre-redactado a través de `wa.me`.
  - Botón **"📞 Llamar"** (`tel:`) o enlace original.
  - Botón de cambio de estado: alterna con un clic entre **Pendiente**, **Postulado** y **En Cotización**.
  - Botón de descarte inmediato con eliminación en base de datos.
  - **Ficha Técnica Colapsable (Acordeón):** Información de contacto, desglose del requerimiento y campo para registrar notas y bitácora de seguimiento.

### 3. 📱 WhatsApp Bot & Control Remoto
- **Simulador Interactivo en Vivo:** Permite probar cualquier comando (`!resumen`, `!cotizaciones`, `!vacantes`, etc.) recibiendo la respuesta renderizada en una **burbuja de chat visual de WhatsApp**.
- **Botones de Acceso Rápido:** Ejecución con un solo clic de los comandos más frecuentes.
- **Guía de Comandos:** Tabla con la sintaxis y ejemplos de cada comando disponible.
- **Instrucciones de Despliegue:** Pasos detallados para conectar con Ngrok y proveedores oficiales (GreenAPI, Meta Cloud API, UltraMsg, Twilio).

### 4. 🔍 Centro de Scraping, Extracción y Captura de Obras
- **Botón Global:** Dispara el escaneo concurrente de las 8 plataformas con un solo clic.
- **Módulos Individuales por Plataforma:** Cada bolsa cuenta con su propia tarjeta, selector de categoría objetivo y botón de escaneo independiente.
- **Extractor Inteligente (Smart Paste):** Área de texto para pegar publicaciones o mensajes de WhatsApp sueltos; el parser procesa y extrae automáticamente el puesto, contacto, teléfono directo, sueldo y genera el enlace a WhatsApp guardándolo en la base de datos.

### 5. 📄 Mi CV & Plantillas de Cotización
- **Formulario de Perfil:** Configura el nombre del contratista/ingeniero, teléfono personal y correo electrónico.
- **Plantillas con Copia Rápida en un Clic:**
  - *Plantilla 1:* Mensaje formal de presentación para vacantes técnicas y de ingeniería.
  - *Plantilla 2:* Propuesta formal de cotización y presupuesto para obras e instalaciones eléctricas industriales y residenciales.
- **Gestor de CV en PDF:** Subida de currículum o portafolio de proyectos (PDF/DOCX), visualización de estado, peso del archivo y descarga directa.

### 6. ⚙️ Configuración & Exportación
- **Exportación de Datos:** Descarga de la base de datos completa con dos botones directos:
  - 📊 Descargar Reporte en Excel (`.xlsx`).
  - 📄 Descargar Reporte en CSV (`.csv`).
- **Editor de Variables de Entorno (`.env`):** Modificación gráfica del proveedor de WhatsApp, teléfonos y tokens de autenticación de GreenAPI y Meta.
- **Visor de Palabras Clave:** Muestra la configuración actual de `config/keywords.json`.

---

## 📱 Módulo Especial: Bot Interactivo de WhatsApp (Control Remoto)

Permite controlar todo el sistema desde tu celular mediante mensajes de WhatsApp:

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

Orientado a la prospección comercial de proyectos eléctricos e instalaciones:

- 👷 **Oficial Eléctrico / Oficial Electricista:** Doblado de conduit PG (1/2" a 2"), charola portacable, cableado de fuerza y control, peinado de tableros de 480V/220V e interpretación de diagramas unifilares.
- 🔧 **Medio Oficial Eléctrico:** Canalizaciones, jalado de conductores, fijación de cajas, ranurado y ponchado de terminales.
- 🧰 **Ayudante Electricista:** Acarreo de material, guiado con guía de acero/nylon, soportería y apoyo en obra.
- 👤 **Identificación de Contactos:** Detección de nombres y cargos de ingenieros de obra, arquitectos y contratistas.
- 📞 **Llamada Telefónica Inmediata:** Marcado rápido con enlaces `tel:+52...`.
- 💬 **Generador de Enlaces Directos `wa.me`:** Abre WhatsApp con el mensaje formal estructurado para presupuestos bajo la norma NOM-001-SEDE.

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
│   ├── app.py                   # Punto de entrada de la interfaz web
│   ├── server.py                # Servidor Flask y API REST del frontend
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css       # Estilos personalizados, badges y burbuja WhatsApp
│   │   └── js/
│   │       └── app.js           # Lógica JavaScript pura (AJAX, Chart.js, interactividad)
│   └── templates/
│       └── index.html           # Dashboard responsivo en HTML5 con Bootstrap 5
├── main.py                      # Lanzador unificado por línea de comandos (CLI)
├── .env.example                 # Plantilla de variables de entorno
├── requirements.txt             # Dependencias de Python (Flask, Pandas, Selenium, etc.)
└── README.md                    # Documentación técnica completa
```

---

## ⚙️ Requisitos Previos

- **Python 3.10+** (probado y 100% compatible con Python 3.12 y Python 3.14 en Windows, Linux y macOS).
- Navegador web moderno (Chrome, Edge, Firefox, Brave).
- Conexión a Internet para la descarga de dependencias y ejecución de scrapers.

---

## 🚀 Instalación y Puesta en Marcha

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/GhostLT/app_busca_trabajo.git
   cd app_busca_trabajo
   ```

2. **Crear y activar entorno virtual (opcional pero recomendado):**
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
   ```
   *Se abrirá automáticamente tu navegador en `http://127.0.0.1:8000` con el panel interactivo.*

---

## 🔌 Endpoints de la API REST

El servidor Flask en `ui/server.py` expone las siguientes rutas y servicios JSON:

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/` | Renderiza el frontend nativo en Bootstrap 5 (`index.html`) |
| `GET` | `/api/stats` | Devuelve estadísticas globales y métricas de postulaciones |
| `GET` | `/api/jobs` | Consulta vacantes con filtros (`search_query`, `location`, `category`, `source`, `status`, `modality`, `has_phone_only`) |
| `GET` | `/api/jobs/<id>` | Obtiene los detalles de una vacante por ID |
| `POST` | `/api/jobs/<id>/status` | Actualiza el estado de postulación (`Postulado`, `Entrevista`, `Pendiente`, `Descartado`) |
| `POST` | `/api/jobs/<id>/notes` | Guarda o actualiza notas de seguimiento |
| `DELETE` | `/api/jobs/<id>` | Elimina una vacante de la base de datos |
| `POST` | `/api/jobs/seed` | Carga el conjunto de vacantes de prueba / demo |
| `POST` | `/api/whatsapp/simulate` | Envía un comando al motor de WhatsApp Bot y devuelve su respuesta |
| `POST` | `/api/scrapers/run` | Ejecuta scrapers (`all` o individuales: `fb`, `linkedin`, `occ`, etc.) |
| `POST` | `/api/extract` | Extrae automáticamente entidades de un texto pegado y guarda en BD |
| `GET` | `/api/profile` | Obtiene los datos del perfil, estado del CV y plantillas de mensaje |
| `POST` | `/api/profile` | Guarda los cambios en nombre, teléfono y correo del perfil |
| `POST` | `/api/cv/upload` | Sube archivo de currículum en PDF o DOCX |
| `GET` | `/api/cv/download` | Descarga el archivo de CV actual |
| `GET` | `/api/export/excel` | Genera y descarga reporte en formato `.xlsx` |
| `GET` | `/api/export/csv` | Genera y descarga reporte en formato `.csv` |
| `GET` | `/api/settings` | Obtiene el estado de los ajustes `.env` y palabras clave |
| `POST` | `/api/settings` | Actualiza y persiste configuraciones en `.env` |

---

## 🖥️ Guía de Uso por Terminal (CLI)

```bash
# 1. Iniciar la interfaz gráfica web (HTML5, CSS3, JS & Bootstrap 5) en puerto predeterminado (8000)
python main.py

# 2. Iniciar la interfaz en un puerto personalizado
python main.py --ui --ui-port 8080

# 3. Iniciar la Consola Interactiva de comandos de WhatsApp en terminal
python main.py --chat

# 4. Iniciar el Servidor Webhook de WhatsApp
python main.py --bot --port 5000

# 5. Escanear solicitudes de electricistas y cotizaciones en Facebook
python main.py --fb

# 6. Escanear vacantes en LinkedIn
python main.py --linkedin

# 7. Escanear vacantes en OCC Mundial
python main.py --occ

# 8. Escanear vacantes en CompuTrabajo
python main.py --computrabajo

# 9. Escanear TODAS las 8 plataformas simultáneamente
python main.py --all

# 10. Ver estadísticas actuales en consola
python main.py --stats

# 11. Exportar datos a Excel y CSV
python main.py --export

# 12. Cargar vacantes demo en la base de datos
python main.py --seed
```

---

## 📲 Configuración de Webhook de WhatsApp

1. **Iniciar el servidor Webhook en segundo plano:**
   ```bash
   python main.py --bot --port 5000
   ```

2. **Exponer el puerto local con Ngrok:**
   ```bash
   ngrok http 5000
   ```

3. **Configurar la URL en tu proveedor (GreenAPI, Meta Cloud API o Twilio):**
   - URL de webhook: `https://tu-subdominio.ngrok-free.app/whatsapp/webhook`

4. **Interactuar desde WhatsApp:** Envía `!ayuda`, `!cotizaciones` o `!resumen` a tu línea para gestionar las ofertas.

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