import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

from config.settings import DB_PATH, EXPORTS_DIR

def get_connection() -> sqlite3.Connection:
    """Get SQLite database connection with row dictionary access."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables if they do not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                source TEXT DEFAULT 'OCC',
                category TEXT DEFAULT 'Ingeniero de RF / Optimización',
                location TEXT,
                modality TEXT DEFAULT 'No especificado',
                salary_min REAL,
                salary_max REAL,
                salary_raw TEXT,
                phone TEXT,
                whatsapp_url TEXT,
                description TEXT,
                url TEXT,
                status TEXT DEFAULT 'Pendiente',
                created_at TEXT NOT NULL,
                updated_at TEXT,
                applied_at TEXT,
                notes TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                action TEXT NOT NULL,
                details TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (job_id) REFERENCES jobs (id) ON DELETE CASCADE
            )
        """)

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_category ON jobs (category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs (status)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_source ON jobs (source)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_applied_at ON jobs (applied_at)")
        conn.commit()

def add_job(job_data: Dict[str, Any]) -> Tuple[int, bool]:
    """
    Insert a job or update if already exists (by URL or title+company).
    Returns (job_id, is_new).
    """
    init_db()
    title = (job_data.get("title") or "Vacante sin título").strip()
    company = (job_data.get("company") or "Empresa Confidencial").strip()
    url = (job_data.get("url") or "").strip()
    source = job_data.get("source", "OCC")
    category = job_data.get("category", "Ingeniero de RF / Optimización")
    location = job_data.get("location", "México")
    modality = job_data.get("modality", "No especificado")
    salary_min = job_data.get("salary_min")
    salary_max = job_data.get("salary_max")
    salary_raw = job_data.get("salary_raw") or ""
    phone = job_data.get("phone") or ""
    whatsapp_url = job_data.get("whatsapp_url") or ""
    description = job_data.get("description") or ""
    status = job_data.get("status", "Pendiente")
    notes = job_data.get("notes", "")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = conn.cursor()
        
        existing = None
        if url and len(url) > 5:
            cursor.execute("SELECT id FROM jobs WHERE url = ?", (url,))
            existing = cursor.fetchone()

        if not existing:
            cursor.execute(
                "SELECT id FROM jobs WHERE LOWER(title) = LOWER(?) AND LOWER(company) = LOWER(?)",
                (title, company)
            )
            existing = cursor.fetchone()

        if existing:
            job_id = existing["id"]
            cursor.execute("""
                UPDATE jobs SET
                    category = COALESCE(NULLIF(?, ''), category),
                    location = COALESCE(NULLIF(?, ''), location),
                    modality = COALESCE(NULLIF(?, ''), modality),
                    salary_min = COALESCE(?, salary_min),
                    salary_max = COALESCE(?, salary_max),
                    salary_raw = COALESCE(NULLIF(?, ''), salary_raw),
                    phone = COALESCE(NULLIF(?, ''), phone),
                    whatsapp_url = COALESCE(NULLIF(?, ''), whatsapp_url),
                    description = COALESCE(NULLIF(?, ''), description),
                    updated_at = ?
                WHERE id = ?
            """, (category, location, modality, salary_min, salary_max, salary_raw, phone, whatsapp_url, description, now_str, job_id))
            conn.commit()
            return job_id, False
        else:
            cursor.execute("""
                INSERT INTO jobs (
                    title, company, source, category, location, modality,
                    salary_min, salary_max, salary_raw, phone, whatsapp_url,
                    description, url, status, created_at, updated_at, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                title, company, source, category, location, modality,
                salary_min, salary_max, salary_raw, phone, whatsapp_url,
                description, url, status, now_str, now_str, notes
            ))
            job_id = cursor.lastrowid
            conn.commit()
            return job_id, True

def get_jobs(
    category: Optional[str] = None,
    source: Optional[str] = None,
    status: Optional[str] = None,
    modality: Optional[str] = None,
    location: Optional[str] = None,
    search_query: Optional[str] = None,
    has_phone_only: bool = False,
    order_by: str = "id DESC"
) -> List[Dict[str, Any]]:
    """Retrieve jobs matching filters, with flexible platform mapping and city/location filtering."""
    init_db()
    query = "SELECT * FROM jobs WHERE 1=1"
    params: List[Any] = []

    if category and category not in ("Todos", "Todas", "Todas las especialidades"):
        query += " AND category = ?"
        params.append(category)

    if source and source not in ("Todos", "Todas", "Todas las plataformas"):
        if source in ("LinkedIn", "linkedin", "💼 LinkedIn"):
            query += " AND source = 'LinkedIn'"
        elif source in ("OCC", "OCC Mundial", "occ", "🌐 OCC Mundial"):
            query += " AND source = 'OCC'"
        elif source in ("CompuTrabajo", "computrabajo", "Computrabajo", "🟧 CompuTrabajo", "💼 CompuTrabajo"):
            query += " AND (source = 'CompuTrabajo' OR source LIKE '%CompuTrabajo%')"
        elif source in ("Facebook", "Red Social", "Redes Sociales", "Redes Sociales (Facebook)", "Red Social (Facebook)", "📱 Red Social (Facebook)", "facebook"):
            query += " AND (source = 'Facebook' OR source LIKE '%Facebook%' OR source LIKE '%Red%')"
        else:
            query += " AND source = ?"
            params.append(source)

    if status and status not in ("Todos", "Todas"):
        query += " AND status = ?"
        params.append(status)

    if modality and modality not in ("Todos", "Todas"):
        query += " AND modality = ?"
        params.append(modality)

    if location and location not in ("Todos", "Todas", "Todas las ciudades", ""):
        loc_clean = location.strip().lower()
        if loc_clean in ("cdmx", "ciudad de mexico", "ciudad de méxico", "df", "distrito federal"):
            query += " AND (LOWER(location) LIKE '%cdmx%' OR LOWER(location) LIKE '%ciudad de m%' OR LOWER(location) LIKE '%distrito federal%' OR LOWER(location) LIKE '%santa fe%')"
        elif loc_clean in ("gdl", "guadalajara", "jalisco", "zapopan"):
            query += " AND (LOWER(location) LIKE '%guadalajara%' OR LOWER(location) LIKE '%gdl%' OR LOWER(location) LIKE '%jalisco%' OR LOWER(location) LIKE '%zapopan%')"
        elif loc_clean in ("mty", "monterrey", "nuevo leon", "nuevo león", "apodaca", "san pedro"):
            query += " AND (LOWER(location) LIKE '%monterrey%' OR LOWER(location) LIKE '%mty%' OR LOWER(location) LIKE '%nuevo le%' OR LOWER(location) LIKE '%apodaca%')"
        elif loc_clean in ("qro", "queretaro", "querétaro"):
            query += " AND (LOWER(location) LIKE '%quer%')"
        else:
            query += " AND LOWER(location) LIKE ?"
            params.append(f"%{loc_clean}%")

    if has_phone_only:
        query += " AND (phone IS NOT NULL AND phone != '')"

    if search_query:
        query += " AND (title LIKE ? OR company LIKE ? OR description LIKE ? OR location LIKE ? OR phone LIKE ?)"
        term = f"%{search_query}%"
        params.extend([term, term, term, term, term])

    query += f" ORDER BY {order_by}"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_job_by_id(job_id: int) -> Optional[Dict[str, Any]]:
    """Fetch a single job by its ID."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_job_status(job_id: int, new_status: str, notes: Optional[str] = None) -> bool:
    """Update status of a job (e.g., Postulado, En Proceso, Entrevista, Pendiente)."""
    init_db()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = conn.cursor()
        if new_status == "Postulado":
            cursor.execute("""
                UPDATE jobs
                SET status = ?, updated_at = ?, applied_at = COALESCE(applied_at, ?), notes = COALESCE(?, notes)
                WHERE id = ?
            """, (new_status, now_str, now_str, notes, job_id))
        elif new_status == "Pendiente":
            cursor.execute("""
                UPDATE jobs
                SET status = ?, updated_at = ?, applied_at = NULL, notes = COALESCE(?, notes)
                WHERE id = ?
            """, (new_status, now_str, notes, job_id))
        elif new_status == "Entrevista":
            cursor.execute("""
                UPDATE jobs
                SET status = ?, updated_at = ?, applied_at = COALESCE(applied_at, ?), notes = COALESCE(?, notes)
                WHERE id = ?
            """, (new_status, now_str, now_str, notes, job_id))
        else:
            cursor.execute("""
                UPDATE jobs
                SET status = ?, updated_at = ?, notes = COALESCE(?, notes)
                WHERE id = ?
            """, (new_status, now_str, notes, job_id))

        cursor.execute("""
            INSERT INTO activity_log (job_id, action, details, created_at)
            VALUES (?, ?, ?, ?)
        """, (job_id, f"Cambio de estado a: {new_status}", notes or "", now_str))

        conn.commit()
        return cursor.rowcount > 0

def update_job_notes(job_id: int, notes: str) -> bool:
    """Update notes for a specific job."""
    init_db()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE jobs SET notes = ?, updated_at = ? WHERE id = ?", (notes, now_str, job_id))
        conn.commit()
        return cursor.rowcount > 0

def delete_job(job_id: int) -> bool:
    """Delete a job by ID."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()
        return cursor.rowcount > 0

def get_stats() -> Dict[str, Any]:
    """Calculate summary statistics for dashboard."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM jobs")
        total = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Postulado'")
        applied = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Pendiente'")
        pending = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Entrevista'")
        interviews = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM jobs WHERE phone != '' AND phone IS NOT NULL")
        with_phone = cursor.fetchone()[0]

        cursor.execute("SELECT category, COUNT(*) as c FROM jobs GROUP BY category")
        by_category = {row["category"]: row["c"] for row in cursor.fetchall()}

        cursor.execute("SELECT source, COUNT(*) as c FROM jobs GROUP BY source")
        by_source = {row["source"]: row["c"] for row in cursor.fetchall()}

        cursor.execute("SELECT modality, COUNT(*) as c FROM jobs GROUP BY modality")
        by_modality = {row["modality"]: row["c"] for row in cursor.fetchall()}

        cursor.execute("SELECT AVG((COALESCE(salary_min, salary_max) + COALESCE(salary_max, salary_min)) / 2.0) FROM jobs WHERE salary_min > 0 OR salary_max > 0")
        avg_sal = cursor.fetchone()[0] or 0.0

        return {
            "total_jobs": total,
            "applied_count": applied,
            "pending_count": pending,
            "interview_count": interviews,
            "with_phone_count": with_phone,
            "by_category": by_category,
            "by_source": by_source,
            "by_modality": by_modality,
            "avg_salary": round(avg_sal, 2)
        }

def get_application_stats() -> Dict[str, Any]:
    """Detailed statistics specifically for applications: daily counts, conversion, breakdown by platform and specialty."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()

        # Total vacancies in DB
        cursor.execute("SELECT COUNT(*) FROM jobs")
        total_jobs = cursor.fetchone()[0]

        # Total registered as Postulado
        cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Postulado'")
        applied_count = cursor.fetchone()[0]

        # Total registered in Entrevista
        cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'Entrevista'")
        interview_count = cursor.fetchone()[0]

        # Total active applications (Postulado + Entrevista)
        total_active_applied = applied_count + interview_count

        # Applications made today
        today_str = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            SELECT COUNT(*) FROM jobs 
            WHERE status IN ('Postulado', 'Entrevista') 
            AND SUBSTR(applied_at, 1, 10) = ?
        """, (today_str,))
        today_count = cursor.fetchone()[0]

        # Applications made this week (last 7 days)
        cursor.execute("""
            SELECT COUNT(*) FROM jobs 
            WHERE status IN ('Postulado', 'Entrevista') 
            AND applied_at >= datetime('now', '-7 days')
        """)
        week_count = cursor.fetchone()[0]

        # Applications made this month (current YYYY-MM)
        month_prefix = datetime.now().strftime("%Y-%m")
        cursor.execute("""
            SELECT COUNT(*) FROM jobs 
            WHERE status IN ('Postulado', 'Entrevista') 
            AND SUBSTR(applied_at, 1, 7) = ?
        """, (month_prefix,))
        month_count = cursor.fetchone()[0]

        # Daily applications series (sorted chronologically)
        cursor.execute("""
            SELECT 
                SUBSTR(applied_at, 1, 10) as day,
                COUNT(*) as count
            FROM jobs 
            WHERE status IN ('Postulado', 'Entrevista') AND applied_at IS NOT NULL
            GROUP BY day 
            ORDER BY day ASC
        """)
        daily_rows = cursor.fetchall()
        daily_applications = {row["day"]: row["count"] for row in daily_rows}

        # Applications by platform
        cursor.execute("""
            SELECT source, COUNT(*) as count 
            FROM jobs 
            WHERE status IN ('Postulado', 'Entrevista') 
            GROUP BY source
        """)
        applied_by_source = {row["source"]: row["count"] for row in cursor.fetchall()}

        # Applications by specialty
        cursor.execute("""
            SELECT category, COUNT(*) as count 
            FROM jobs 
            WHERE status IN ('Postulado', 'Entrevista') 
            GROUP BY category
        """)
        applied_by_category = {row["category"]: row["count"] for row in cursor.fetchall()}

        # Applications by modality
        cursor.execute("""
            SELECT modality, COUNT(*) as count 
            FROM jobs 
            WHERE status IN ('Postulado', 'Entrevista') 
            GROUP BY modality
        """)
        applied_by_modality = {row["modality"]: row["count"] for row in cursor.fetchall()}

        # Success / Conversion Rate (% of applied that reached interview)
        conversion_rate = round((interview_count / total_active_applied) * 100.0, 1) if total_active_applied > 0 else 0.0

        return {
            "total_jobs": total_jobs,
            "applied_count": applied_count,
            "interview_count": interview_count,
            "total_active_applied": total_active_applied,
            "today_count": today_count,
            "week_count": week_count,
            "month_count": month_count,
            "conversion_rate": conversion_rate,
            "daily_applications": daily_applications,
            "applied_by_source": applied_by_source,
            "applied_by_category": applied_by_category,
            "applied_by_modality": applied_by_modality
        }

def export_to_excel(filepath: Optional[str] = None) -> str:
    """Export all jobs to an Excel spreadsheet with modality, phone, and whatsapp_url."""
    init_db()
    if not filepath:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = str(EXPORTS_DIR / f"vacantes_export_{timestamp}.xlsx")

    jobs = get_jobs(order_by="created_at DESC")
    df = pd.DataFrame(jobs)
    if not df.empty:
        cols_rename = {
            "id": "ID",
            "title": "Puesto / Posición",
            "company": "Empresa / Contacto",
            "category": "Especialidad",
            "source": "Plataforma / Fuente",
            "location": "Ubicación",
            "modality": "Modalidad (modality)",
            "salary_raw": "Sueldo Ofertado",
            "phone": "Teléfono (phone)",
            "whatsapp_url": "WhatsApp URL (whatsapp_url)",
            "status": "Estado Postulación",
            "url": "Enlace Vacante",
            "created_at": "Fecha Detección",
            "applied_at": "Fecha Postulación",
            "notes": "Notas"
        }
        existing_cols = [c for c in cols_rename.keys() if c in df.columns]
        df_export = df[existing_cols].rename(columns=cols_rename)
        df_export.to_excel(filepath, index=False, engine="openpyxl")
    else:
        df.to_excel(filepath, index=False, engine="openpyxl")
    return filepath

def export_to_csv(filepath: Optional[str] = None) -> str:
    """Export all jobs to a CSV file with modality, phone, and whatsapp_url."""
    init_db()
    if not filepath:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = str(EXPORTS_DIR / f"vacantes_export_{timestamp}.csv")

    jobs = get_jobs(order_by="created_at DESC")
    df = pd.DataFrame(jobs)
    if not df.empty:
        cols_rename = {
            "id": "ID",
            "title": "Puesto / Posición",
            "company": "Empresa / Contacto",
            "category": "Especialidad",
            "source": "Plataforma / Fuente",
            "location": "Ubicación",
            "modality": "Modalidad (modality)",
            "salary_raw": "Sueldo Ofertado",
            "phone": "Teléfono (phone)",
            "whatsapp_url": "WhatsApp URL (whatsapp_url)",
            "status": "Estado Postulación",
            "url": "Enlace Vacante",
            "created_at": "Fecha Detección",
            "applied_at": "Fecha Postulación",
            "notes": "Notas"
        }
        existing_cols = [c for c in cols_rename.keys() if c in df.columns]
        df_export = df[existing_cols].rename(columns=cols_rename)
        df_export.to_csv(filepath, index=False, encoding="utf-8-sig")
    else:
        df.to_csv(filepath, index=False, encoding="utf-8-sig")
    return filepath

def seed_sample_jobs():
    """Populate database with sample job vacancies for instant testing (all default to Pendiente)."""
    samples = [
        {
            "title": "Ingeniero de Optimización RF (4G/5G) - Drive Test",
            "company": "Telecom Solutions México / Ericsson Partner",
            "source": "OCC",
            "category": "Ingeniero de RF / Optimización",
            "location": "Ciudad de México (Santa Fe)",
            "modality": "Híbrido",
            "salary_min": 28000,
            "salary_max": 38000,
            "salary_raw": "$28,000 - $38,000 MXN mensuales libres",
            "phone": "+525541829301",
            "whatsapp_url": "https://wa.me/525541829301",
            "description": "Buscamos Ingeniero de RF con experiencia en análisis de Drive Test, herramientas Nemo/TEMS, optimización de parámetros RAN 4G LTE y 5G NR. Manejo de KPIs de accesibilidad, retención y throughput. Prestaciones superiores de ley.",
            "url": "https://www.occ.com.mx/empleo/oferta/ingeniero-rf-optimizacion-cdmx",
            "status": "Pendiente",
            "notes": "Requiere disponibilidad para traslados ocasionales a sitios celulares."
        },
        {
            "title": "Ingeniero de Radiofrecuencia y Microondas (MW)",
            "company": "Huawei Technologies de México",
            "source": "OCC",
            "category": "Ingeniero de RF / Optimización",
            "location": "Querétaro / Home Office",
            "modality": "Híbrido",
            "salary_min": 35000,
            "salary_max": 48000,
            "salary_raw": "$35,000 - $48,000 MXN al mes",
            "phone": "+524428192034",
            "whatsapp_url": "https://wa.me/524428192034",
            "description": "Diseño de enlaces microondas, cálculo de disponibilidad, presupuestos de potencia de enlace, configuración de equipos RTN y antenas. Inglés intermedio-avanzado.",
            "url": "https://www.occ.com.mx/empleo/oferta/ingeniero-rf-mw-huawei",
            "status": "Pendiente",
            "notes": "Postulación prioritaria."
        },
        {
            "title": "Ingeniero Eléctrico - Proyectos de Media y Alta Tensión",
            "company": "Grupo Electro-Construcciones del Centro",
            "source": "Facebook",
            "category": "Ingeniero Eléctrico",
            "location": "Monterrey, N.L. (Parque Industrial Apodaca)",
            "modality": "Presencial",
            "salary_min": 30000,
            "salary_max": 42000,
            "salary_raw": "$30,000 - $42,000 netos + Bonos",
            "phone": "+528114567890",
            "whatsapp_url": "https://wa.me/528114567890",
            "description": "Supervisión de obras eléctricas industriales, subestaciones eléctricas 13.8kV/115kV, cálculo de alimentadores, cuadros de cargas y cumplimiento de NOM-001-SEDE. Interesados enviar CV por WhatsApp.",
            "url": "https://facebook.com/groups/empleos.ingenieria.mexico/permalink/9182371",
            "status": "Pendiente",
            "notes": "Contacto directo con el jefe de proyectos por WhatsApp."
        },
        {
            "title": "Ingeniero de Instalaciones y Mantenimiento Eléctrico",
            "company": "Schneider Electric Solutions",
            "source": "OCC",
            "category": "Ingeniero Eléctrico",
            "location": "Guadalajara, Jalisco",
            "modality": "Presencial",
            "salary_min": 25000,
            "salary_max": 32000,
            "salary_raw": "$25,000 - $32,000 brutos",
            "phone": "+523319028374",
            "whatsapp_url": "https://wa.me/523319028374",
            "description": "Mantenimiento preventivo y correctivo a transformadores, plantas de emergencia diésel, sistemas UPS y tableros de transferencia automática. Tarjeta profesional indispensable.",
            "url": "https://www.occ.com.mx/empleo/oferta/ingeniero-electrico-mantenimiento-gdl",
            "status": "Pendiente",
            "notes": "Mantenimiento eléctrico industrial."
        },
        {
            "title": "Ingeniero de Software Backend (Python / FastAPI / Cloud)",
            "company": "TechInnovate Cloud Solutions",
            "source": "OCC",
            "category": "Ingeniero de Sistemas / Software",
            "location": "Ciudad de México / 100% Remoto",
            "modality": "Remoto",
            "salary_min": 45000,
            "salary_max": 65000,
            "salary_raw": "$45,000 - $65,000 MXN mensuales",
            "phone": "+525588371920",
            "whatsapp_url": "https://wa.me/525588371920",
            "description": "Desarrollo de microservicios en Python (FastAPI/Django), APIs REST, bases de datos PostgreSQL, contenedores Docker y despliegue en AWS/GCP. Seguro de gastos médicos mayores y horario flexible.",
            "url": "https://www.occ.com.mx/empleo/oferta/ingeniero-software-python-remoto",
            "status": "Pendiente",
            "notes": "Vacante remota de Python."
        },
        {
            "title": "Ingeniero de Sistemas y DevOps Junior/Mid",
            "company": "Bolsa de Empleo IT Facebook",
            "source": "Facebook",
            "category": "Ingeniero de Sistemas / Software",
            "location": "Remoto (México)",
            "modality": "Remoto",
            "salary_min": 32000,
            "salary_max": 40000,
            "salary_raw": "$32,000 - $40,000 libres",
            "phone": "+525598765432",
            "whatsapp_url": "https://wa.me/525598765432",
            "description": "Se busca ingeniero de sistemas con conocimientos en Linux, pipelines CI/CD, Kubernetes y monitoreo con Prometheus/Grafana. Mandar CV directamente al WhatsApp de RH para agendar entrevista.",
            "url": "https://facebook.com/groups/devs.mexico.empleos/permalink/4829104",
            "status": "Pendiente",
            "notes": "Vacante remota muy atractiva."
        }
    ]

    count_added = 0
    for s in samples:
        _, is_new = add_job(s)
        if is_new:
            count_added += 1
    return count_added