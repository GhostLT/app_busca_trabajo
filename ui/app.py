import sys
import os
import textwrap
import importlib
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import json
from datetime import datetime

import config.settings as settings
# Ensure modules are freshly reloaded in hot-reloading Streamlit runtime
try:
    importlib.reload(settings)
except Exception:
    pass

import core.database as db
try:
    importlib.reload(db)
except Exception:
    pass

import core.data_extractor as extractor
import core.notifier_whatsapp as notifier
from core.occ_bot import OCCBot
from core.facebook_scraper import FacebookScraper
from core.linkedin_scraper import LinkedInScraper
from core.computrabajo_scraper import CompuTrabajoScraper
from core.glassdoor_scraper import GlassdoorScraper
from core.jobrapido_scraper import JobrapidoScraper
from core.jobleads_scraper import JobLeadsScraper

# Page Configuration
st.set_page_config(
    page_title="AutoJob Hunter & Tracker | Multiplataforma México",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Clean UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .job-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .job-card:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
        border-color: #CBD5E1;
    }
    .badge-rf {
        background-color: #DBEAFE;
        color: #1D4ED8;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem;
        display: inline-block;
    }
    .badge-electric {
        background-color: #FEF3C7;
        color: #B45309;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem;
        display: inline-block;
    }
    .badge-software {
        background-color: #D1FAE5;
        color: #047857;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem;
        display: inline-block;
    }
    .badge-general {
        background-color: #F1F5F9;
        color: #475569;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem;
        display: inline-block;
    }
    .badge-source-occ {
        background-color: #EEF2FF;
        color: #4338CA;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
    }
    .badge-source-linkedin {
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
    }
    .badge-source-computrabajo {
        background-color: #FFF7ED;
        color: #C2410C;
        border: 1px solid #FFEDD5;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
    }
    .badge-source-glassdoor {
        background-color: #ECFDF5;
        color: #047857;
        border: 1px solid #A7F3D0;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
    }
    .badge-source-jobrapido {
        background-color: #F0F9FF;
        color: #0284C7;
        border: 1px solid #BAE6FD;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
    }
    .badge-source-jobleads {
        background-color: #FAF5FF;
        color: #7E22CE;
        border: 1px solid #E9D5FF;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
    }
    .badge-source-fb {
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
        display: inline-block;
    }
    .badge-modality {
        background-color: #F8FAFC;
        color: #334155;
        border: 1px solid #CBD5E1;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.82rem;
        display: inline-block;
    }
    .badge-phone {
        background-color: #F0FDF4;
        color: #15803D;
        border: 1px solid #BBF7D0;
        padding: 3px 9px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.82rem;
        display: inline-block;
    }
    .badge-salary {
        background-color: #ECFDF5;
        color: #065F46;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.88rem;
        display: inline-block;
    }
    .badge-whatsapp {
        background-color: #25D366;
        color: white !important;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.78rem;
        text-decoration: none;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize DB
db.init_db()

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3850/3850285.png", width=64)
    st.title("AutoJob Hunter")
    st.caption("OCC, LinkedIn, CompuTrabajo, Glassdoor, Jobrapido, JobLeads & FB")
    st.divider()

    st.subheader("⚡ Acciones Rápidas")
    
    if st.button("🚀 Escanear TODAS las Plataformas", use_container_width=True, type="primary"):
        with st.spinner("Escaneando en tiempo real en todas las bolsas laborales..."):
            total_saved = 0
            for scraper_cls in [LinkedInScraper, OCCBot, CompuTrabajoScraper, GlassdoorScraper, JobrapidoScraper, JobLeadsScraper, FacebookScraper]:
                try:
                    s = scraper_cls()
                    if hasattr(s, "run_search_and_save"):
                        r = s.run_search_and_save()
                        total_saved += r.get("total_new", 0)
                    elif hasattr(s, "run_scan_and_save"):
                        r = s.run_scan_and_save()
                        total_saved += r.get("new_saved", 0)
                except Exception:
                    pass
            st.success(f"¡Escaneo completo finalizado! {total_saved} nuevas vacantes registradas.")
            st.rerun()

    sc_col_a, sc_col_b = st.columns(2)
    with sc_col_a:
        if st.button("💼 LinkedIn", use_container_width=True):
            with st.spinner("LinkedIn..."):
                r = LinkedInScraper().run_search_and_save()
                st.success(f"LinkedIn: {r['total_new']} nuevas")
                st.rerun()

        if st.button("🌐 OCC", use_container_width=True):
            with st.spinner("OCC..."):
                r = OCCBot().run_search_and_save()
                st.success(f"OCC: {r['total_new']} nuevas")
                st.rerun()

        if st.button("🟧 CompuTrabajo", use_container_width=True):
            with st.spinner("CompuTrabajo..."):
                r = CompuTrabajoScraper().run_search_and_save()
                st.success(f"CompuTrabajo: {r['total_new']} nuevas")
                st.rerun()

    with sc_col_b:
        if st.button("🟢 Glassdoor", use_container_width=True):
            with st.spinner("Glassdoor..."):
                r = GlassdoorScraper().run_search_and_save()
                st.success(f"Glassdoor: {r['total_new']} nuevas")
                st.rerun()

        if st.button("🌐 Jobrapido", use_container_width=True):
            with st.spinner("Jobrapido..."):
                r = JobrapidoScraper().run_search_and_save()
                st.success(f"Jobrapido: {r['total_new']} nuevas")
                st.rerun()

        if st.button("🎯 JobLeads", use_container_width=True):
            with st.spinner("JobLeads..."):
                r = JobLeadsScraper().run_search_and_save()
                st.success(f"JobLeads: {r['total_new']} nuevas")
                st.rerun()

    if st.button("📱 Redes Sociales (FB)", use_container_width=True):
        with st.spinner("Facebook..."):
            r = FacebookScraper().run_scan_and_save()
            st.success(f"Facebook: {r['new_saved']} nuevas")
            st.rerun()

    if st.button("🧪 Cargar Vacantes Demo", use_container_width=True):
        added = db.seed_sample_jobs()
        st.info(f"Se verificaron y cargaron {added} vacantes de demostración.")
        st.rerun()

    st.divider()
    app_kpi = db.get_application_stats()
    st.subheader("📊 Mis Postulaciones")
    st.write(f"✅ **Total Postuladas:** {app_kpi['applied_count']}")
    st.write(f"📅 **Postuladas Hoy:** {app_kpi['today_count']}")
    st.write(f"🟣 **En Entrevista:** {app_kpi['interview_count']}")
    st.write(f"📁 **Total Bolsa:** {app_kpi['total_jobs']}")

# Main Header
st.markdown('<div class="main-header">🚀 AutoJob Hunter & Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Plataforma integral de búsqueda, extracción y postulación automática para Ingenieros de <b>RF / Telecomunicaciones</b>, <b>Eléctricos</b> y <b>Sistemas / Software</b> en <b>LinkedIn</b>, <b>OCC</b>, <b>CompuTrabajo</b>, <b>Glassdoor</b>, <b>Jobrapido</b>, <b>JobLeads</b> y <b>Redes Sociales</b></div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Estadísticas de Postulaciones",
    "💼 Bolsa de Vacantes",
    "🔍 Scraping & Extracción",
    "📄 Mi CV & Perfil",
    "⚙️ Configuración & Exportación"
])

# -------------------------------------------------------------
# TAB 1: DASHBOARD DE ESTADÍSTICAS Y POSTULACIONES DIARIAS
# -------------------------------------------------------------
with tab1:
    st.subheader("📊 Panel de Rendimiento y Control de Postulaciones")
    
    app_stats = db.get_application_stats()
    gen_stats = db.get_stats()

    # TOP METRICS ROW: Total postuladas, hoy, semana, mes, entrevistas
    m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
    
    with m_col1:
        st.metric(
            label="🎯 Total Postuladas",
            value=app_stats["applied_count"],
            delta=f"{(app_stats['applied_count']/app_stats['total_jobs']*100):.1f}% de la bolsa" if app_stats['total_jobs'] > 0 else "0%"
        )
    with m_col2:
        st.metric(
            label="📅 Postuladas Hoy",
            value=app_stats["today_count"],
            delta="Hoy" if app_stats["today_count"] > 0 else "Sin actividad hoy"
        )
    with m_col3:
        st.metric(
            label="🗓️ Esta Semana (7d)",
            value=app_stats["week_count"],
            delta="Últimos 7 días"
        )
    with m_col4:
        st.metric(
            label="📆 Este Mes",
            value=app_stats["month_count"],
            delta=datetime.now().strftime("%B %Y")
        )
    with m_col5:
        st.metric(
            label="🟣 En Entrevista",
            value=app_stats["interview_count"],
            delta=f"Éxito: {app_stats['conversion_rate']}%"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # DAILY APPLICATIONS CHART & TIMELINE
    st.markdown("### 📈 Cantidad de Postulaciones Realizadas Diariamente")
    
    daily_dict = app_stats["daily_applications"]
    
    if daily_dict:
        df_daily = pd.DataFrame(list(daily_dict.items()), columns=["Fecha", "Postulaciones"]).sort_values("Fecha")
        
        c_chart, c_table = st.columns([2.5, 1.2])
        
        with c_chart:
            st.markdown("##### 📊 Historial Diario de Postulaciones")
            st.bar_chart(df_daily.set_index("Fecha"), color="#2563EB")
            
        with c_table:
            st.markdown("##### 📋 Resumen por Fecha")
            st.dataframe(df_daily, use_container_width=True, hide_index=True)
            avg_per_day = df_daily["Postulaciones"].mean()
            st.caption(f"Promedio diario en días activos: **{avg_per_day:.1f} postulaciones/día**")
    else:
        st.info("💡 **Aún no has registrado postulaciones.** Ve a la pestaña **💼 Bolsa de Vacantes** y haz clic en el botón **`⬜ Postularme`** de cualquier vacante para comenzar a registrar tu actividad diaria.")

    st.divider()

    # BREAKDOWN CHARTS ROW
    st.markdown("### 🌐 Desglose de Tus Postulaciones")
    b_col1, b_col2, b_col3 = st.columns(3)

    with b_col1:
        st.markdown("#### 💼 Por Plataforma")
        if app_stats["applied_by_source"]:
            df_src_app = pd.DataFrame(list(app_stats["applied_by_source"].items()), columns=["Plataforma", "Postuladas"])
            st.bar_chart(df_src_app.set_index("Plataforma"), color="#0284C7")
        else:
            st.caption("Sin postulaciones por plataforma.")

    with b_col2:
        st.markdown("#### 📡 Por Especialidad")
        if app_stats["applied_by_category"]:
            df_cat_app = pd.DataFrame(list(app_stats["applied_by_category"].items()), columns=["Especialidad", "Postuladas"])
            st.bar_chart(df_cat_app.set_index("Especialidad"), color="#10B981")
        else:
            st.caption("Sin postulaciones por especialidad.")

    with b_col3:
        st.markdown("#### 🏢 Por Modalidad")
        if app_stats["applied_by_modality"]:
            df_mod_app = pd.DataFrame(list(app_stats["applied_by_modality"].items()), columns=["Modalidad", "Postuladas"])
            st.bar_chart(df_mod_app.set_index("Modalidad"), color="#F59E0B")
        else:
            st.caption("Sin postulaciones por modalidad.")

    st.divider()

    # DETAILED TABLE OF APPLIED VACANCIES
    st.markdown("### 📋 Registro Completo de Vacantes Postuladas")
    applied_jobs = db.get_jobs(status="Postulado", order_by="applied_at DESC")
    interview_jobs = db.get_jobs(status="Entrevista", order_by="applied_at DESC")
    all_tracked = applied_jobs + interview_jobs

    if all_tracked:
        df_tracked = pd.DataFrame(all_tracked)
        cols_tracked = ["applied_at", "title", "company", "category", "source", "modality", "phone", "whatsapp_url", "status", "notes"]
        existing_cols = [c for c in cols_tracked if c in df_tracked.columns]
        df_tracked_display = df_tracked[existing_cols].copy()
        
        col_names = {
            "applied_at": "Fecha Postulación",
            "title": "Puesto",
            "company": "Empresa",
            "category": "Especialidad",
            "source": "Plataforma",
            "modality": "Modalidad",
            "phone": "Teléfono",
            "whatsapp_url": "WhatsApp",
            "status": "Estado",
            "notes": "Notas"
        }
        df_tracked_display.rename(columns=col_names, inplace=True)
        st.dataframe(df_tracked_display, use_container_width=True)
    else:
        st.info("No hay vacantes registradas en estado 'Postulado' o 'Entrevista' todavía.")

    st.divider()

    # GLOBAL OVERVIEW OF TOTAL DATABASE
    with st.expander("📁 Ver Estadísticas Globales de la Base de Vacantes (Disponibles vs Postuladas)"):
        g_c1, g_c2, g_c3 = st.columns(3)
        with g_c1:
            st.write(f"📂 **Total Vacantes Detectadas:** {gen_stats['total_jobs']}")
            st.write(f"⏳ **Vacantes Pendientes:** {gen_stats['pending_count']}")
        with g_c2:
            st.write(f"📞 **Vacantes con WhatsApp Directo:** {gen_stats['with_phone_count']}")
            st.write(f"💰 **Sueldo Promedio Detectado:** ${gen_stats['avg_salary']:,.0f} MXN")
        with g_c3:
            if gen_stats["by_category"]:
                st.write("**Distribución Total por Especialidad:**")
                for k, v in gen_stats["by_category"].items():
                    st.write(f"- {k}: **{v}**")

# -------------------------------------------------------------
# TAB 2: BOLSA DE VACANTES (CON FILTROS MULTIPLATAFORMA)
# -------------------------------------------------------------
with tab2:
    st.subheader("💼 Explorador y Gestión de Vacantes")

    # Interactive Filter Form with Submit Button (All 7 platforms support)
    with st.form(key="job_filter_form"):
        st.markdown("#### 🎯 Filtros de Búsqueda")
        f_col1, f_col2, f_col3, f_col4 = st.columns([2.2, 1.6, 1.6, 1.4])
        
        with f_col1:
            search_query = st.text_input(
                "🔍 Puesto / Tecnología / Empresa:",
                placeholder="Ej: Python, RF, Subestaciones, Huawei..."
            )
        
        with f_col2:
            city_filter = st.text_input(
                "📍 Ciudad / Ubicación:",
                placeholder="Ej: CDMX, Guadalajara, Monterrey, Querétaro..."
            )

        with f_col3:
            cat_filter = st.selectbox("Especialidad:", [
                "Todas las especialidades",
                "Ingeniero de RF / Optimización",
                "Ingeniero Eléctrico",
                "Ingeniero de Sistemas / Software"
            ])
        
        with f_col4:
            source_filter = st.selectbox("🌐 Plataforma:", [
                "Todas las plataformas",
                "LinkedIn",
                "OCC Mundial",
                "CompuTrabajo",
                "Glassdoor",
                "Jobrapido",
                "JobLeads",
                "Redes Sociales (Facebook)"
            ])

        f_col5, f_col6, f_col7, f_col8 = st.columns([1.5, 1.5, 1.8, 1.8])
        
        with f_col5:
            status_filter = st.selectbox("Estado:", ["Todos", "Pendiente", "Postulado", "Entrevista", "Descartado"])

        with f_col6:
            modality_filter = st.selectbox("Modalidad:", ["Todas", "Remoto", "Híbrido", "Presencial"])

        with f_col7:
            st.write("")
            st.write("")
            phone_only = st.checkbox("Solo con WhatsApp 📱", value=False)

        with f_col8:
            st.write("")
            st.write("")
            apply_filter_btn = st.form_submit_button("🔍 Aplicar Filtros", type="primary", use_container_width=True)

    # Fetch Filtered Jobs
    jobs = db.get_jobs(
        category=cat_filter if cat_filter != "Todas las especialidades" else None,
        source=source_filter,
        status=status_filter if status_filter != "Todos" else None,
        modality=modality_filter if modality_filter != "Todas" else None,
        location=city_filter if city_filter.strip() else None,
        search_query=search_query if search_query.strip() else None,
        has_phone_only=phone_only,
        order_by="id DESC"
    )

    filter_info_parts = [f"Plataforma: {source_filter}"]
    if city_filter.strip():
        filter_info_parts.append(f"Ciudad: '{city_filter.strip()}'")
    filter_info_str = " | ".join(filter_info_parts)

    st.markdown(f"**Resultados:** Se encontraron **{len(jobs)}** vacantes con los filtros aplicados (*{filter_info_str}*):")

    if not jobs:
        st.info("No se encontraron vacantes con los criterios seleccionados.")
    else:
        for job in jobs:
            j_id = job["id"]
            j_title = job["title"]
            j_comp = job["company"]
            j_cat = job["category"]
            j_src = job.get("source", "OCC")
            j_loc = job["location"] or "México"
            j_mod = job["modality"] or "No especificado"
            j_sal = job["salary_raw"] or "No especificado"
            j_phone = job["phone"] or ""
            j_wa = job["whatsapp_url"] or ""
            j_desc = job["description"] or ""
            j_url = job["url"] or ""
            j_status = job.get("status", "Pendiente")
            j_notes = job["notes"] or ""

            # Category Badge styling
            if "RF" in j_cat:
                cat_badge = f'<span class="badge-rf">📡 {j_cat}</span>'
            elif "Eléctric" in j_cat:
                cat_badge = f'<span class="badge-electric">⚡ {j_cat}</span>'
            elif "Sistemas" in j_cat or "Software" in j_cat:
                cat_badge = f'<span class="badge-software">💻 {j_cat}</span>'
            else:
                cat_badge = f'<span class="badge-general">⚙️ {j_cat}</span>'

            # Platform Source Badges
            if j_src == "OCC":
                src_badge = '<span class="badge-source-occ">🌐 OCC Mundial</span>'
            elif j_src == "LinkedIn":
                src_badge = '<span class="badge-source-linkedin">💼 LinkedIn</span>'
            elif j_src == "CompuTrabajo":
                src_badge = '<span class="badge-source-computrabajo">🟧 CompuTrabajo</span>'
            elif j_src == "Glassdoor":
                src_badge = '<span class="badge-source-glassdoor">🟢 Glassdoor</span>'
            elif j_src == "Jobrapido":
                src_badge = '<span class="badge-source-jobrapido">🌐 Jobrapido</span>'
            elif j_src == "JobLeads":
                src_badge = '<span class="badge-source-jobleads">🎯 JobLeads</span>'
            else:
                src_badge = '<span class="badge-source-fb">📱 Red Social (Facebook)</span>'
            
            # Modality Badge
            mod_badge = f'<span class="badge-modality">🏢 {j_mod}</span>'

            # Phone Badge
            if j_phone:
                phone_badge = f'<span class="badge-phone">📞 {j_phone}</span>'
            else:
                phone_badge = '<span style="color:#94A3B8; font-size:0.8rem;">📵 Sin teléfono directo</span>'

            # WhatsApp URL representation
            if not j_wa and j_phone:
                j_wa = notifier.generate_whatsapp_link(j_phone, j_title, j_comp, category=j_cat)

            wa_badge_html = f'<a href="{j_wa}" target="_blank" class="badge-whatsapp">💬 wa.me</a>' if j_wa else ''

            # Status Badge representation
            status_colors = {
                "Pendiente": "🟡 Pendiente",
                "Postulado": "🟢 Postulado",
                "Entrevista": "🟣 En Entrevista",
                "Descartado": "⚪ Descartado"
            }
            status_label = status_colors.get(j_status, j_status)

            card_html = textwrap.dedent(f"""
<div class="job-card">
<div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
<div>
<h3 style="margin: 0; color: #0F172A; font-size: 1.25rem;">{j_title}</h3>
<p style="margin: 3px 0 0 0; color: #475569; font-weight: 500;">🏢 {j_comp} &nbsp;•&nbsp; 📍 {j_loc}</p>
</div>
<div style="text-align: right;">
{cat_badge} &nbsp; {src_badge}
</div>
</div>
<div style="margin-top: 10px; display: flex; gap: 12px; align-items: center; flex-wrap: wrap;">
<span class="badge-salary">💰 {j_sal}</span>
{mod_badge}
{phone_badge}
{wa_badge_html}
<span style="font-size: 0.88rem; color: #64748B; margin-left: auto;"><b>Estado:</b> {status_label}</span>
</div>
</div>
""").strip()

            with st.container():
                st.markdown(card_html, unsafe_allow_html=True)

                # Action row for the job card: WhatsApp, Ver Vacante, Postularme, Entrevista, Descartar
                act_col1, act_col2, act_col3, act_col4, act_col5 = st.columns([2.2, 1.4, 1.4, 1.4, 1.2])
                
                with act_col1:
                    if j_phone:
                        wa_direct = notifier.generate_whatsapp_link(j_phone, j_title, j_comp, category=j_cat)
                        st.link_button(f"💬 WhatsApp ({j_phone})", wa_direct, use_container_width=True, type="primary")
                    elif j_wa:
                        st.link_button("💬 Abrir WhatsApp", j_wa, use_container_width=True, type="primary")
                    else:
                        st.button("📵 Sin Teléfono", disabled=True, key=f"nophone_{j_id}", use_container_width=True)

                with act_col2:
                    if j_url and j_url.startswith("http"):
                        st.link_button("🌐 Ver Vacante", j_url, use_container_width=True)
                    else:
                        st.button("🌐 Enlace N/D", disabled=True, key=f"nourl_{j_id}", use_container_width=True)

                with act_col3:
                    if j_status == "Postulado":
                        if st.button("✅ Postulado", key=f"app_{j_id}", use_container_width=True, type="primary", help="Registrado como Postulado. Haz clic para desmarcar."):
                            db.update_job_status(j_id, "Pendiente")
                            st.toast(f"Vacante #{j_id} desmarcada (Pendiente).", icon="↩️")
                            st.rerun()
                    else:
                        if st.button("⬜ Postularme", key=f"app_{j_id}", use_container_width=True, help="Haz clic para registrar tu postulación en la base de datos."):
                            db.update_job_status(j_id, "Postulado")
                            st.toast(f"¡Postulación registrada en base de datos para #{j_id}!", icon="✅")
                            st.rerun()

                with act_col4:
                    if j_status == "Entrevista":
                        if st.button("🟣 En Entrevista", key=f"ent_{j_id}", use_container_width=True, type="primary", help="Registrado como Entrevista. Haz clic para desmarcar."):
                            db.update_job_status(j_id, "Pendiente")
                            st.toast(f"Vacante #{j_id} desmarcada (Pendiente).", icon="↩️")
                            st.rerun()
                    else:
                        if st.button("🎯 Entrevista", key=f"ent_{j_id}", use_container_width=True, help="Haz clic para registrar que conseguiste entrevista en la base de datos."):
                            db.update_job_status(j_id, "Entrevista")
                            st.toast(f"¡Entrevista registrada en base de datos para #{j_id}!", icon="🎯")
                            st.rerun()

                with act_col5:
                    if st.button("🗑️ Descartar", key=f"del_{j_id}", use_container_width=True, help="Eliminar vacante"):
                        db.delete_job(j_id)
                        st.rerun()

                # Description Expander
                with st.expander(f"📋 Ver Ficha Completa: Modalidad, Teléfono, WhatsApp y Descripción (#{j_id})"):
                    det_c1, det_c2, det_c3 = st.columns(3)
                    with det_c1:
                        st.write(f"🏢 **Modalidad:** `{j_mod}`")
                        st.write(f"📍 **Ubicación:** `{j_loc}`")
                        st.write(f"🌐 **Plataforma:** `{j_src}`")
                    with det_c2:
                        st.write(f"📞 **Teléfono:** `{j_phone or 'No especificado'}`")
                        st.write(f"💰 **Sueldo Ofertado:** `{j_sal}`")
                    with det_c3:
                        if j_wa:
                            st.markdown(f"🔗 **WhatsApp URL:** [Abrir Chat]({j_wa})")
                            st.code(j_wa, language="text")
                        else:
                            st.write("🔗 **WhatsApp URL:** `No disponible`")

                    st.divider()
                    st.markdown("#### 📄 Descripción de la Posición")
                    st.write(j_desc if j_desc else "Sin descripción detallada.")
                    
                    st.divider()
                    new_notes = st.text_input("Notas personales sobre esta vacante:", value=j_notes, key=f"notes_{j_id}")
                    if st.button("💾 Guardar Nota", key=f"savenote_{j_id}"):
                        db.update_job_notes(j_id, new_notes)
                        st.success("Nota actualizada correctamente.")

                st.markdown("<hr style='margin: 12px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 3: SCRAPING & EXTRACCIÓN (7 PLATAFORMAS)
# -------------------------------------------------------------
with tab3:
    st.subheader("🔍 Centro de Scraping y Extracción Inteligente")

    # Global Scan Banner
    if st.button("⚡ ESCANEAR TODAS LAS PLATAFORMAS (LinkedIn, OCC, CompuTrabajo, Glassdoor, Jobrapido, JobLeads, FB)", type="primary", use_container_width=True):
        with st.spinner("Rastreando vacantes simultáneamente en todos los portales de México..."):
            total_s = 0
            for sc_name, sc_cls in [
                ("LinkedIn", LinkedInScraper),
                ("OCC", OCCBot),
                ("CompuTrabajo", CompuTrabajoScraper),
                ("Glassdoor", GlassdoorScraper),
                ("Jobrapido", JobrapidoScraper),
                ("JobLeads", JobLeadsScraper),
                ("Facebook", FacebookScraper)
            ]:
                try:
                    s = sc_cls()
                    if hasattr(s, "run_search_and_save"):
                        r = s.run_search_and_save()
                        total_s += r.get("total_new", 0)
                    elif hasattr(s, "run_scan_and_save"):
                        r = s.run_scan_and_save()
                        total_s += r.get("new_saved", 0)
                except Exception:
                    pass
            st.success(f"¡Escaneo global completado! Se encontraron e insertaron {total_s} nuevas vacantes.")
            st.rerun()

    st.divider()

    # ROW 1: OCC, LinkedIn, CompuTrabajo, Glassdoor
    sc_c1, sc_c2, sc_c3, sc_c4 = st.columns(4)

    with sc_c1:
        st.markdown("### 🌐 OCC Mundial")
        occ_target = st.selectbox("Especialidad OCC:", ["Todos", "Ingeniero de RF / Optimización", "Ingeniero Eléctrico", "Ingeniero de Sistemas / Software"], key="occ_s")
        if st.button("🚀 Escanear OCC", use_container_width=True):
            with st.spinner("Conectando con OCC..."):
                r = OCCBot().run_search_and_save(categories=None if occ_target == "Todos" else [occ_target])
                st.success(f"OCC: {r['total_new']} nuevas.")
                st.rerun()

    with sc_c2:
        st.markdown("### 💼 LinkedIn Jobs")
        lk_target = st.selectbox("Especialidad LinkedIn:", ["Todos", "Ingeniero de RF / Optimización", "Ingeniero Eléctrico", "Ingeniero de Sistemas / Software"], key="lk_s")
        if st.button("💼 Escanear LinkedIn", use_container_width=True):
            with st.spinner("Consultando LinkedIn..."):
                r = LinkedInScraper().run_search_and_save(categories=None if lk_target == "Todos" else [lk_target])
                st.success(f"LinkedIn: {r['total_new']} nuevas.")
                st.rerun()

    with sc_c3:
        st.markdown("### 🟧 CompuTrabajo")
        ct_target = st.selectbox("Especialidad CompuTrabajo:", ["Todos", "Ingeniero de RF / Optimización", "Ingeniero Eléctrico", "Ingeniero de Sistemas / Software"], key="ct_s")
        if st.button("🟧 Escanear CompuTrabajo", use_container_width=True):
            with st.spinner("Consultando CompuTrabajo..."):
                r = CompuTrabajoScraper().run_search_and_save(categories=None if ct_target == "Todos" else [ct_target])
                st.success(f"CompuTrabajo: {r['total_new']} nuevas.")
                st.rerun()

    with sc_c4:
        st.markdown("### 🟢 Glassdoor")
        gd_target = st.selectbox("Especialidad Glassdoor:", ["Todos", "Ingeniero de RF / Optimización", "Ingeniero Eléctrico", "Ingeniero de Sistemas / Software"], key="gd_s")
        if st.button("🟢 Escanear Glassdoor", use_container_width=True):
            with st.spinner("Consultando Glassdoor..."):
                r = GlassdoorScraper().run_search_and_save(categories=None if gd_target == "Todos" else [gd_target])
                st.success(f"Glassdoor: {r['total_new']} nuevas.")
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ROW 2: Jobrapido, JobLeads, Facebook
    sc_c5, sc_c6, sc_c7 = st.columns(3)

    with sc_c5:
        st.markdown("### 🌐 Jobrapido")
        jr_target = st.selectbox("Especialidad Jobrapido:", ["Todos", "Ingeniero de RF / Optimización", "Ingeniero Eléctrico", "Ingeniero de Sistemas / Software"], key="jr_s")
        if st.button("🌐 Escanear Jobrapido", use_container_width=True):
            with st.spinner("Consultando Jobrapido..."):
                r = JobrapidoScraper().run_search_and_save(categories=None if jr_target == "Todos" else [jr_target])
                st.success(f"Jobrapido: {r['total_new']} nuevas.")
                st.rerun()

    with sc_c6:
        st.markdown("### 🎯 JobLeads")
        jl_target = st.selectbox("Especialidad JobLeads:", ["Todos", "Ingeniero de RF / Optimización", "Ingeniero Eléctrico", "Ingeniero de Sistemas / Software"], key="jl_s")
        if st.button("🎯 Escanear JobLeads", use_container_width=True):
            with st.spinner("Consultando JobLeads..."):
                r = JobLeadsScraper().run_search_and_save(categories=None if jl_target == "Todos" else [jl_target])
                st.success(f"JobLeads: {r['total_new']} nuevas.")
                st.rerun()

    with sc_c7:
        st.markdown("### 📱 Redes Sociales")
        st.write("Escanea publicaciones en grupos de empleo de ingeniería en Facebook.")
        if st.button("📱 Escanear Facebook", use_container_width=True):
            with st.spinner("Escaneando Facebook..."):
                r = FacebookScraper().run_scan_and_save()
                st.success(f"Facebook: {r['new_saved']} nuevas.")
                st.rerun()

    st.divider()
    st.markdown("### 📝 Extractor Inteligente de Publicaciones (Pegar Texto)")
    st.write("Pega el texto de cualquier publicación para extraer automáticamente todos sus campos:")
    
    sample_paste = st.text_area(
        "Texto de la publicación:",
        height=130,
        placeholder="Ejemplo:\nBuscamos Ingeniero de RF 5G para Huawei en CDMX (Híbrido). Sueldo $35,000 libres. Mandar CV al WhatsApp 55 1234 5678 o https://wa.me/525512345678"
    )

    if st.button("⚡ Extraer y Guardar Publicación", use_container_width=True):
        if not sample_paste.strip():
            st.warning("Por favor pega el texto de una publicación.")
        else:
            parsed = extractor.parse_job_post(sample_paste, source="Facebook")
            job_id, is_new = db.add_job(parsed)
            if is_new:
                st.success(f"¡Vacante extraída y guardada con éxito! (ID #{job_id})")
            else:
                st.info(f"Vacante actualizada con los nuevos datos (ID #{job_id}).")
            
            st.markdown("#### 🎯 Datos Extraídos:")
            ex_c1, ex_c2, ex_c3 = st.columns(3)
            with ex_c1:
                st.write(f"📌 **Puesto:** {parsed.get('title')}")
                st.write(f"🏢 **Modalidad:** `{parsed.get('modality')}`")
            with ex_c2:
                st.write(f"📞 **Teléfono:** `{parsed.get('phone') or 'N/D'}`")
                st.write(f"💰 **Sueldo:** `{parsed.get('salary_raw') or 'N/D'}`")
            with ex_c3:
                st.write(f"💬 **WhatsApp URL:**")
                if parsed.get('whatsapp_url'):
                    st.markdown(f"[{parsed.get('whatsapp_url')}]({parsed.get('whatsapp_url')})")
                else:
                    st.write("`N/D`")
            st.rerun()

# -------------------------------------------------------------
# TAB 4: CV & PERFIL
# -------------------------------------------------------------
with tab4:
    st.subheader("📄 Gestión de Curriculum Vitae (CV) y Perfil")
    
    cv_col1, cv_col2 = st.columns([1.5, 1])

    with cv_col1:
        st.markdown("#### 👤 Perfil Profesional del Postulante")
        cand_name = st.text_input("Nombre Completo:", value="Ingeniero Candidato")
        cand_phone = st.text_input("Teléfono de Contacto (WhatsApp):", value=getattr(settings, "USER_WHATSAPP_PHONE", os.getenv("USER_WHATSAPP_PHONE", "+5255XXXXXXXX")))
        cand_email = st.text_input("Correo Electrónico:", value=getattr(settings, "OCC_EMAIL", os.getenv("OCC_EMAIL", "correo@ejemplo.com")))
        
        st.markdown("#### 📌 Especialidades Objetivo")
        target_roles = getattr(settings, "TARGET_ROLES", ["Ingeniero de RF", "Ingeniero Eléctrico", "Ingeniero de Sistemas"])
        for r in target_roles:
            st.write(f"- 🔹 **{r}**")

        st.markdown("#### 💬 Mensaje de Presentación Predeterminado para WhatsApp")
        sample_msg = notifier.generate_whatsapp_message(
            job_title="Ingeniero de Optimización RF / Telecomunicaciones",
            company="Empresa Contratante",
            candidate_name=cand_name,
            category="Ingeniero de RF / Optimización"
        )
        st.text_area("Plantilla de mensaje:", value=sample_msg, height=200)

    with cv_col2:
        st.markdown("#### 📎 Archivo de Currículum (PDF)")
        cv_path_val = getattr(settings, "CV_PATH", str(settings.CV_DIR / "mi_cv.pdf"))
        cv_target_path = Path(cv_path_val)
        
        if cv_target_path.exists():
            size_kb = cv_target_path.stat().st_size / 1024
            st.success(f"✅ CV cargado: `{cv_target_path.name}` ({size_kb:.1f} KB)")
        else:
            st.warning("⚠️ No se ha detectado archivo de CV en la ruta predeterminada.")

        uploaded_cv = st.file_uploader("Subir o actualizar CV (PDF)", type=["pdf", "docx"])
        if uploaded_cv is not None:
            save_path = settings.CV_DIR / uploaded_cv.name
            with open(save_path, "wb") as f:
                f.write(uploaded_cv.getbuffer())
            settings.update_env_variable("CV_PATH", str(save_path))
            st.success(f"¡CV guardado exitosamente en: `{save_path}`!")
            st.rerun()

# -------------------------------------------------------------
# TAB 5: CONFIGURACIÓN & EXPORTACIÓN
# -------------------------------------------------------------
with tab5:
    st.subheader("⚙️ Configuración del Sistema y Exportación de Datos")

    exp_col1, exp_col2 = st.columns(2)

    with exp_col1:
        st.markdown("### 📥 Exportar Base de Datos")
        st.write("Descarga el listado completo de vacantes de **OCC, LinkedIn, CompuTrabajo, Glassdoor, Jobrapido, JobLeads y Facebook** (incluyendo **Modalidad**, **Teléfono**, **WhatsApp URL** y **Fecha de Postulación**).")

        excel_path = db.export_to_excel()
        with open(excel_path, "rb") as f:
            st.download_button(
                label="📊 Descargar Reporte en Excel (.xlsx)",
                data=f,
                file_name=f"vacantes_ingenieria_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )

        csv_path = db.export_to_csv()
        with open(csv_path, "rb") as f:
            st.download_button(
                label="📄 Descargar Reporte en CSV",
                data=f,
                file_name=f"vacantes_ingenieria_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )

    with exp_col2:
        st.markdown("### 🔐 Credenciales y Variables de Entorno (.env)")
        st.write(f"Archivo de configuración: `{settings.ENV_PATH}`")
        
        with st.expander("Ver / Editar Variables de Entorno"):
            occ_mail = st.text_input("OCC Email:", value=getattr(settings, "OCC_EMAIL", os.getenv("OCC_EMAIL", "")))
            lk_mail = st.text_input("LinkedIn Email:", value=getattr(settings, "LINKEDIN_EMAIL", os.getenv("LINKEDIN_EMAIL", "")))
            ct_mail = st.text_input("CompuTrabajo Email:", value=getattr(settings, "COMPUTRABAJO_EMAIL", os.getenv("COMPUTRABAJO_EMAIL", "")))
            gd_mail = st.text_input("Glassdoor Email:", value=getattr(settings, "GLASSDOOR_EMAIL", os.getenv("GLASSDOOR_EMAIL", "")))
            jr_mail = st.text_input("Jobrapido Email:", value=getattr(settings, "JOBRAPIDO_EMAIL", os.getenv("JOBRAPIDO_EMAIL", "")))
            jl_mail = st.text_input("JobLeads Email:", value=getattr(settings, "JOBLEADS_EMAIL", os.getenv("JOBLEADS_EMAIL", "")))
            fb_mail = st.text_input("Facebook Email:", value=getattr(settings, "FB_EMAIL", os.getenv("FB_EMAIL", "")))
            wa_ph = st.text_input("WhatsApp Personal:", value=getattr(settings, "USER_WHATSAPP_PHONE", os.getenv("USER_WHATSAPP_PHONE", "")))
            
            if st.button("Guardar Cambios en .env"):
                settings.update_env_variable("OCC_EMAIL", occ_mail)
                settings.update_env_variable("LINKEDIN_EMAIL", lk_mail)
                settings.update_env_variable("COMPUTRABAJO_EMAIL", ct_mail)
                settings.update_env_variable("GLASSDOOR_EMAIL", gd_mail)
                settings.update_env_variable("JOBRAPIDO_EMAIL", jr_mail)
                settings.update_env_variable("JOBLEADS_EMAIL", jl_mail)
                settings.update_env_variable("FB_EMAIL", fb_mail)
                settings.update_env_variable("USER_WHATSAPP_PHONE", wa_ph)
                st.success("Variables de entorno actualizadas con éxito.")

    st.divider()
    st.markdown("### 🏷️ Palabras Clave y Filtros (`config/keywords.json`)")
    kw_data = settings.get_keywords()
    with st.expander("Ver JSON de Configuración"):
        st.json(kw_data)