# 🚀 AutoJob Hunter & Tracker (8 Canales Laborales, 8 Especialidades IT/Ingeniería, Frontend Nativo Bootstrap 5 & Bot de WhatsApp)

Sistema integral de automatización multiplataforma para la **búsqueda de empleo, extracción de vacantes, captura de solicitudes de cotizaciones y control total remoto desde tu WhatsApp** en las 8 plataformas líderes en México (**Facebook**, **LinkedIn**, **OCC Mundial**, **CompuTrabajo**, **Glassdoor**, **Jobrapido**, **JobLeads**, **Jobsora**).

Soporta **8 especialidades técnicas y de ingeniería**:
1. 📡 **Ingeniero de RF / Optimización**
2. ⚡ **Ingeniero Eléctrico** (incluyendo Oficial Eléctrico, Medio Oficial y Ayudante Electricista)
3. 💻 **Ingeniero de Sistemas / Software**
4. 📈 **Ingeniero Performance**
5. 🖥️ **Ingeniero NOC**
6. 🌐 **Desarrollador Web**
7. ⚙️ **Desarrollador Backend**
8. 🎨 **Desarrollador Frontend**

Cuenta con una **interfaz web moderna desarrollada 100% en HTML5, CSS3, JavaScript puro (Vanilla JS) y Bootstrap 5**, respaldada por una API REST en Flask, **eliminando cualquier dependencia de Streamlit** para un rendimiento ligero, flexible e integrable.

---

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Arquitectura del Sistema](#️-arquitectura-del-sistema)
- [Especialidades Técnicas y de Ingeniería (8 Áreas)](#-especialidades-técnicas-y-de-ingeniería-8-áreas)
- [Panel de Control Web (HTML5, CSS3, JS & Bootstrap 5)](#-panel-de-control-web-html5-css3-js--bootstrap-5)
- [Ranking y Distribución de Oportunidades Reales (215 Vacantes)](#-ranking-y-distribución-de-oportunidades-reales-215-vacantes)
- [Filtrado Interactivo por Estado (Postuladas, Gestionadas Hoy, En Cotización)](#-filtrado-interactivo-por-estado-postuladas-gestionadas-hoy-en-cotización)
- [Bot Interactivo de WhatsApp](#-módulo-especial-bot-interactivo-de-whatsapp-control-total-desde-tu-celular)
- [Módulo de Obras, Oficiales y Ayudantes Eléctricos](#-módulo-especial-captura-de-obras-clientes-y-categorías-eléctricas)
- [Plataformas de Empleo Integradas (8 Canales)](#-plataformas-de-empleo-integradas-8-canales)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación y Puesta en Marcha](#-instalación-y-puesta-en-marcha)
- [Endpoints de la API REST](#-endpoints-de-la-api-rest)
- [Depuración Total de Datos Demo y Política 100% Fuentes Reales](#️-depuración-total-de-datos-demo-y-política-100-fuentes-reales)
- [Guía de Uso por Terminal (CLI)](#-guía-de-uso-por-terminal-cli)
- [Configuración de Webhook de WhatsApp](#-configuración-de-webhook-de-whatsapp)
- [Plantilla de Mensaje de Cotización](#-plantilla-de-mensaje-de-cotización)

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

## 🎯 Especialidades Técnicas y de Ingeniería (8 Áreas)

El sistema clasifica automáticamente cada vacante y solicitud en una de las 8 especialidades configuradas en `config/keywords.json`, integrando badges visuales, filtros dedicados en la interfaz y palabras clave específicas en cada scraper:

| Especialidad | Icono & Badge | Tecnologías y Palabras Clave Principales | Ámbito de Aplicación |
| :--- | :---: | :--- | :--- |
| **Ingeniero de RF / Optimización** | 📡 `badge-rf` | Radiofrecuencia, Drive Test, Optimización RF, Telecomunicaciones, Fibra Óptica, FTTH, RAN, 4G LTE, 5G NR, Site Survey, Antenas, Microondas, Atoll, Ericsson, Huawei, Nokia. | Redes celulares, telecomunicaciones móviles, planta externa e inalámbrica. |
| **Ingeniero Eléctrico** | ⚡ `badge-electric` | Subestaciones, Media Tensión, Alta Tensión, Baja Tensión, Cuadros Eléctricos, Transformadores, NOM-001-SEDE, Protecciones Eléctricas, Plantas de Emergencia, Oficial Eléctrico, Medio Oficial, Ayudante Electricista. | Obras electromecánicas, instalaciones industriales, comerciales y residenciales. |
| **Ingeniero de Sistemas / Software** | 💻 `badge-software` | Soporte TI, Redes LAN, Cableado Estructurado, Cisco, MikroTik, DevOps, Cloud (AWS, Azure), Docker, Kubernetes, SQL, PostgreSQL, Python, Linux SysAdmin. | Infraestructura de TI corporativa, redes empresariales y desarrollo general. |
| **Ingeniero Performance** | 📈 `badge-performance` | JMeter, LoadRunner, K6, Locust, Rendimiento de Red, Capacidad de Red (Capacity Planning), Pruebas de Carga y Estrés, KPIs de Red, Latencia, Throughput, QoE, QoS. | Optimización del rendimiento de aplicaciones de alta concurrencia y tráfico de red. |
| **Ingeniero NOC** | 🖥️ `badge-noc` | Monitoreo 24/7, Centro de Operaciones de Red (NOC), Zabbix, PRTG, SolarWinds, Nagios, Grafana, Datadog, Gestión de Alarmas e Incidentes, ITIL, Troubleshooting L1/L2. | Supervisión continua de redes de telecomunicaciones, servidores y enlaces de datos. |
| **Desarrollador Web** | 🌐 `badge-web` | HTML5, CSS3, JavaScript, TypeScript, Bootstrap, Tailwind CSS, PHP, WordPress, Sitios Web Responsivos, Aplicaciones Web, SASS, UI/UX Web, SEO Técnico. | Construcción y mantenimiento de sitios, portales y aplicaciones web completas. |
| **Desarrollador Backend** | ⚙️ `badge-backend` | Python (FastAPI, Django, Flask), Node.js (Express, NestJS), Java (Spring Boot), Go (Golang), C# (.NET Core), APIs RESTful, GraphQL, Microservicios, PostgreSQL, Redis, RabbitMQ. | Lógica de negocio del lado del servidor, arquitectura de microservicios y bases de datos. |
| **Desarrollador Frontend** | 🎨 `badge-frontend` | React, Vue.js, Angular, Next.js, Nuxt, Svelte, TypeScript, JavaScript moderno (ES6+), HTML5 Semántico, CSS Grid / Flexbox, Redux, Zustand, Pinia, Core Web Vitals. | Creación de interfaces de usuario interactivas, responsivas y componentes SPA modernos. |

---

## 🌐 Panel de Control Web (HTML5, CSS3, JS & Bootstrap 5)

La interfaz gráfica reemplaza por completo a Streamlit y opera mediante un servidor Flask integrado. Se divide en 6 pestañas operativas:

### 1. 📊 Estadísticas de Postulaciones y Rendimiento
- **Tarjetas KPI Interactivas y Filtrables en tiempo real:**
  - `🎯 Total Postuladas`, `📅 Gestionadas Hoy` y `🟣 En Cotización / Entrevista` cuentan con interacción dinámica: **al hacer clic sobre cualquiera de ellas, se activa automáticamente el filtro correspondiente y muestra de inmediato la lista de oportunidades**.
  - Indicador visual hover y badge *"Ver lista"* en cada tarjeta interactiva.
- **Resumen de Estado Lateral (Sidebar) Interactivo:**
  - Enlaces directos en la barra lateral para filtrar con un clic: `🎯 Postuladas`, `📅 Gestionadas Hoy`, `🟣 En Cotización`, `🟢 Pendientes` o `📋 Total Base (215)`.
- **🏆 Ranking de Oportunidades Reales por Plataforma (215 vacantes):**
  - Panel visual de ranking interactivo con barras de progreso porcentuales calculadas en tiempo real.
  - Destacado con corona de oro para la plataforma líder (OCC Mundial con 104 vacantes, 48.4%).
  - Tabla comparativa completa (#1 al #8) con badges oficiales de marca, conteo exacto, porcentaje y botón de acceso rápido para filtrar la bolsa.
  - Desglose compacto en la barra lateral (*Sidebar*) para monitorear las fuentes sin cambiar de pestaña.
- **Gráfico de Historial Diario (Chart.js):** Cantidad de gestiones registradas por día calendario con tabla de resumen lateral y cálculo de promedio diario.
- **Gráficos de Desglose:**
  - Desglose por Plataforma con colores oficiales de cada marca.
  - Desglose por Especialidad (las 8 áreas IT y de Ingeniería).
  - Desglose por Modalidad (Presencial, Híbrido, Remoto).
- **Registro Detallado de Seguimiento con Filtros:**
  - Botones de filtrado rápido en la cabecera de la tabla: `[ Todas ]`, `[ 🎯 Postuladas ]`, `[ 📅 Gestionadas Hoy ]` y `[ 🟣 En Cotización ]` con contadores en tiempo real.
  - Historial detallado con fecha, empresa, contacto, teléfono, estado y chat de WhatsApp.

### 2. 💼 Bolsa de Vacantes & Cotizaciones de Instalaciones
- **Barra de Filtrado Rápido (Quick Filter Pills):**
  - Botones de acceso directo con contadores automáticos para filtrar en un clic: `🌐 Todas (215)`, `🎯 Postuladas`, `📅 Gestionadas Hoy`, `🟣 En Cotización / Entrevista` y `🟢 Pendientes`.
  - **Banner de Filtro Activo:** Muestra claramente qué estado está filtrado, el número de resultados encontrados y un botón rápido para restablecer la vista.
- **Filtros Avanzados:**
  - Selector de Estado sincronizado (`Todos los estados`, `🎯 Postuladas`, `📅 Gestionadas Hoy`, `🟣 En Cotización / Entrevista`, `🟢 Pendientes`, `⚪ Descartados`) que ejecuta la búsqueda automáticamente al cambiar la selección.
  - Búsqueda por texto (puesto, nombre de cliente, palabras clave).
  - Ubicación geográfica (Ciudad de México, Querétaro, Monterrey, Guadalajara, etc.).
  - Selector de Especialidad.
  - Selector de Plataforma origen (las 8 fuentes integradas).
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

## 🏆 Ranking y Distribución de Oportunidades Reales (215 Vacantes)

El sistema procesa, consolida y visualiza en tiempo real las **215 oportunidades laborales reales extraídas directamente de las plataformas oficiales**, categorizadas de mayor a menor volumen para identificar con exactitud la fuente más productiva para postulaciones:

| Posición | Plataforma Laboral Oficial | Vacantes Reales | % del Total | Volumen / Categoría | Impacto Estratégico y Perfil de Ofertas |
| :---: | :--- | :---: | :---: | :--- | :--- |
| 🥇 **#1** | **OCC Mundial** | **104** | **48.4%** | 🟢 Muy Alto (Líder principal) | Ofertas formales corporativas, ingeniería de telecomunicaciones, NOC, software y desarrollo web en México. |
| 🥈 **#2** | **LinkedIn** | **67** | **31.2%** | 🔵 Alto (Segundo canal) | Posiciones multinacionales, puestos senior, desarrolladores backend/frontend y corporativos de TI. |
| 🥉 **#3** | **Facebook** | **25** | **11.6%** | 🟡 Medio (Obras y Campo) | Contratación directa, solicitudes de contratistas, proyectos de instalaciones eléctricas, Oficiales y Ayudantes. |
| **#4** | **CompuTrabajo** | **6** | **2.8%** | 🟠 Focalizado | Puestos técnicos de campo, mantenimiento, instalaciones de planta externa y supervisión de obra. |
| **#5** | **Jobrapido** | **4** | **1.9%** | ⚪ Complementario | Agregador nacional de empleos técnicos y especialistas en redes e infraestructura. |
| **#6** | **Glassdoor** | **3** | **1.4%** | ⚪ Selectivo | Posiciones con referencias de compensación salarial, beneficios y calificaciones de empresas. |
| **#7** | **JobLeads** | **3** | **1.4%** | ⚪ Ejecutivo | Puestos de nivel gerencial, Tech Leads, Performance Engineers y jefaturas de proyecto. |
| **#8** | **Jobsora** | **3** | **1.4%** | ⚪ Complementario | Ofertas de infraestructura, soporte técnico, telecomunicaciones y electricidad. |
| **TOTAL** | **8 Plataformas Oficiales** | **215** | **100.0%** | **100% Datos Reales** | **Base de datos unificada, limpia y depurada sin registros sintéticos o demo.** |

### 💡 Análisis y Hallazgos Estratégicos del Ranking:
1. **Dominio de OCC Mundial y LinkedIn (79.6% del mercado):**
   - Juntas acumulan **171 de las 215 vacantes**, constituyendo los dos pilares fundamentales para vacantes profesionales, de oficina, ingeniería de software y telecomunicaciones.
2. **Facebook como canal exclusivo de trato directo e instalaciones (11.6%):**
   - Con **25 solicitudes reales**, es la plataforma ideal para contactar directamente a ingenieros de obra, contratistas y clientes de instalaciones eléctricas residenciales e industriales.
3. **Canales Complementarios de Alta Especificidad (8.8%):**
   - Las 19 vacantes restantes de CompuTrabajo, Jobrapido, Glassdoor, JobLeads y Jobsora proporcionan oportunidades de nicho con filtros salariales específicos y puestos de supervisión técnica.
4. **Visualización en Tiempo Real en el Panel:**
   - La interfaz muestra barras de progreso porcentuales calculadas dinámicamente, tarjetas con colores de identidad corporativa para cada bolsa, tabla con enlaces de filtrado directo y un widget permanente en el sidebar para tener siempre a la vista el rendimiento de cada plataforma.

---

## 🔍 Filtrado Interactivo por Estado (Postuladas, Gestionadas Hoy, En Cotización)

El sistema integra un mecanismo de **filtrado interactivo bidireccional y reactivo** que permite acceder a las listas filtradas de oportunidades con un solo clic desde múltiples puntos de la interfaz:

### 🎯 Puntos de Acceso para Filtrado Inmediato:
1. **Tarjetas KPI del Dashboard Principal (Pestaña 1):**
   - **`🎯 Total Postuladas`:** Al hacer clic en la tarjeta, navega automáticamente a la Bolsa de Vacantes (Pestaña 2) y despliega la lista filtrada de oportunidades con estado `Postulado`.
   - **`📅 Gestionadas Hoy`:** Al pulsar la tarjeta, filtra de forma inmediata las oportunidades cuya postulación, cotización o actualización se realizó durante la fecha actual (`applied_at` o `updated_at` = hoy).
   - **`🟣 En Cotización / Entrevista`:** Al hacer clic, muestra todas las oportunidades con presupuestos presentados o trámites de entrevista activos (`status = 'Entrevista'`).
2. **Barra de Filtrado Rápido (Quick Filter Pills) en el Explorador (Pestaña 2):**
   - Botones estilizados tipo *pill* con contadores en tiempo real ubicados en la cabecera de la bolsa de trabajo:
     - `[ 🌐 Todas (215) ]`: Restablece el listado completo de la base de datos.
     - `[ 🎯 Postuladas ]`: Filtra vacantes contactadas y postuladas.
     - `[ 📅 Gestionadas Hoy ]`: Filtra la actividad registrada durante el día de hoy.
     - `[ 🟣 En Cotización / Entrevista ]`: Filtra cotizaciones formales y procesos de entrevista.
     - `[ 🟢 Pendientes ]`: Muestra oportunidades nuevas por revisar y gestionar.
3. **Resumen de Estado en la Barra Lateral (Sidebar):**
   - Todos los elementos del bloque *"📊 Resumen de Estado"* son interactivos, cuentan con efectos hover y badges dinámicos para disparar el filtrado desde cualquier pestaña.
4. **Selector Desplegable de Estado en Formulario:**
   - El selector `<select id="filterStatus">` cuenta con opciones enriquecidas (`🎯 Postuladas`, `📅 Gestionadas Hoy`, `🟣 En Cotización / Entrevista`, `🟢 Pendientes`) y sincronización automática bidireccional con las pills y la API.
5. **Tabla de Historial de Seguimiento (Pestaña 1):**
   - Incorpora su propia barra de filtros: `[ Todas ]`, `[ 🎯 Postuladas ]`, `[ 📅 Gestionadas Hoy ]` y `[ 🟣 En Cotización ]` con contadores dinámicos para auditar gestiones sin cambiar de vista.

### 💡 Banner de Filtro Activo:
- Al seleccionar cualquier estado, aparece sobre las tarjetas un banner resaltado en azul suave indicando el filtro activo, la cantidad de oportunidades encontradas y un botón rápido para **Mostrar todas**.

### 🔌 Soporte en Backend y API REST:
- El endpoint `GET /api/jobs` soporta el parámetro `managed_today=true` y reconoce alias como `status=hoy`, realizando consultas SQL optimizadas sobre las marcas temporales `applied_at` y `updated_at` sin alterar los filtros de especialidad o ubicación.

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
| **📱 Facebook** | `core/facebook_scraper.py` | Automatización con Selenium y sesión persistente: extrae tus grupos (`/groups/joins/`), vacantes, Oficiales, Ayudantes y cotizaciones con contacto directo |
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

## 🛡️ Depuración Total de Datos Demo y Política 100% Fuentes Reales

Para garantizar la máxima confiabilidad operativa y profesionalismo en el seguimiento de vacantes y cotizaciones, **se eliminaron definitivamente todos los mecanismos de datos sintéticos o de prueba (`Cargar Demo` / `seed`)**:

1. **Eliminación de Módulos y Código de Prueba:**
   - **Backend (`core/database.py`):** Removida la función `seed_sample_jobs()` y la lista estática de vacantes demo.
   - **API REST (`ui/server.py`):** Eliminado el endpoint `POST /api/jobs/seed`.
   - **Frontend UI (`ui/templates/index.html`):** Removidos los botones *"Cargar Demo"* del navbar superior y *"Cargar Vacantes Demo"* del panel lateral de acciones rápidas.
   - **Lógica JavaScript (`ui/static/js/app.js`):** Eliminada la función `seedSampleJobs()`.
   - **Lanzador CLI (`main.py`):** Retirado el parámetro de ejecución `--seed`.

2. **Limpieza Completa de la Base de Datos (`data/jobs.db`):**
   - Se purgaron todos los registros artificiales existentes.
   - La base de datos opera con **100% datos genuinos** provenientes exclusivamente de las 8 plataformas integradas (**OCC**, **LinkedIn**, **Facebook**, **CompuTrabajo**, **Jobrapido**, **Glassdoor**, **JobLeads**, **Jobsora**) y del extractor inteligente de publicaciones.

3. **Optimización Responsiva y Ajuste Visual del Menú Lateral:**
   - Se rediseñaron los botones de escaneo rápido del panel lateral con la clase `.sidebar-scraper-btn` y la subclase `.btn-scraper-ct`.
   - Se corrigió el desbordamiento de la etiqueta **CompuTrabajo** ajustando el ancho de columnas del grid (`col-lg-3 col-xl-3`), espaciado tipográfico (`letter-spacing: -0.4px`), recorte semántico con elipsis (`text-truncate`) y texto descriptivo en tooltip (`title="CompuTrabajo"`), logrando un ajuste milimétrico dentro del marco del botón.

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

# 5. Escanear tus grupos de Facebook, vacantes y solicitudes de cotizaciones (Selenium interactivo)
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