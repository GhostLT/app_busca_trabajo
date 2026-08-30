import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import json
from datetime import datetime

import config.settings as settings
import core.database as db
import core.data_extractor as extractor
import core.notifier_whatsapp as notifier
from core.occ_bot import OCCBot
from core.facebook_scraper import FacebookScraper

# Page Configuration
st.set_page_config(
    page_title="AutoJob Hunter & Tracker | Ingeniería",
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
    .metric-box {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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
    }
    .badge-electric {
        background-color: #FEF3C7;
        color: #B45309;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .badge-software {
        background-color: #D1FAE5;
        color: #047857;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .badge-general {
        background-color: #F1F5F9;
        color: #475569;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem;
    }
    .badge-source-occ {
        background-color: #EEF2FF;
        color: #4338CA;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
    }
    .badge-source-fb {
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 3px 8px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.75rem;
    }
    .badge-salary {
        background-color: #ECFDF5;
        color: #065F46;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.88rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize DB
db.init_db()

# Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3850/3850285.png", width=64)
    st.title("AutoJob Hunter")
    st.caption("OCC Mundial & Redes Sociales")
    st.divider()

    st.subheader("⚡ Acciones Rápidas")
    
    if st.button("🚀 Escanear OCC Mundial", use_container_width=True, type="primary"):
        with st.spinner("Buscando vacantes en OCC Mundial..."):
            bot = OCCBot()
            res = bot.run_search_and_save()
            st.success(f"¡Búsqueda lista! {res['total_found']} encontradas ({res['total_new']} nuevas)")
            st.rerun()

    if st.button("📱 Escanear Redes (Facebook)", use_container_width=True):
        with st.spinner("Escaneando publicaciones en grupos..."):
            fb = FacebookScraper()
            res = fb.run_scan_and_save()
            st.success(f"¡Listo! {res['total_found']} publicaciones ({res['new_saved']} nuevas)")
            st.rerun()

    if st.button("🧪 Cargar Vacantes Demo", use_container_width=True):
        added = db.seed_sample_jobs()
        st.info(f"Se verificaron y cargaron {added} vacantes de demostración.")
        st.rerun()

    st.divider()
    stats = db.get_stats()
    st.subheader("📊 Resumen")
    st.write(f"📁 **Total Vacantes:** {stats['total_jobs']}")
    st.write(f"✅ **Postuladas:** {stats['applied_count']}")
    st.write(f"⏳ **Pendientes:** {stats['pending_count']}")
    st.write(f"💬 **Con WhatsApp:** {stats['with_phone_count']}")

# Main Header
st.markdown('<div class="main-header">🚀 AutoJob Hunter & Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Plataforma integral de búsqueda, extracción y postulación automática para Ingenieros de <b>RF / Telecomunicaciones</b>, <b>Eléctricos</b> y <b>Sistemas / Software</b></div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "💼 Bolsa de Vacantes",
    "🔍 Scraping & Extracción",
    "📄 Mi CV & Perfil",
    "⚙️ Configuración & Exportación"
])

# -------------------------------------------------------------
# TAB 1: DASHBOARD
# -------------------------------------------------------------
with tab1:
    stats = db.get_stats()
    
    # Top KPI Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Vacantes", stats["total_jobs"])
    with col2:
        st.metric("Postuladas", stats["applied_count"], delta=f"{stats['applied_count']}/{stats['total_jobs']}" if stats['total_jobs'] else "0")
    with col3:
        st.metric("Pendientes", stats["pending_count"])
    with col4:
        st.metric("En Entrevista", stats["interview_count"])
    with col5:
        avg_s = f"${stats['avg_salary']:,.0f} MXN" if stats['avg_salary'] > 0 else "N/D"
        st.metric("Sueldo Promedio", avg_s)

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row
    ch_col1, ch_col2, ch_col3 = st.columns(3)
    
    with ch_col1:
        st.subheader("📡 Por Especialidad")
        if stats["by_category"]:
            df_cat = pd.DataFrame(list(stats["by_category"].items()), columns=["Especialidad", "Vacantes"])
            st.bar_chart(df_cat.set_index("Especialidad"), color="#1E88E5")
        else:
            st.info("Sin datos de especialidades.")

    with ch_col2:
        st.subheader("🏢 Por Modalidad")
        if stats["by_modality"]:
            df_mod = pd.DataFrame(list(stats["by_modality"].items()), columns=["Modalidad", "Vacantes"])
            st.bar_chart(df_mod.set_index("Modalidad"), color="#10B981")
        else:
            st.info("Sin datos de modalidad.")

    with ch_col3:
        st.subheader("🌐 Por Fuente")
        if stats["by_source"]:
            df_src = pd.DataFrame(list(stats["by_source"].items()), columns=["Fuente", "Vacantes"])
            st.bar_chart(df_src.set_index("Fuente"), color="#F59E0B")
        else:
            st.info("Sin datos de fuente.")

    st.divider()
    st.subheader("🕒 Vacantes Recientes")
    recent_jobs = db.get_jobs(order_by="created_at DESC")[:5]
    if recent_jobs:
        df_rec = pd.DataFrame(recent_jobs)[["title", "company", "category", "salary_raw", "source", "status", "created_at"]]
        df_rec.columns = ["Puesto", "Empresa", "Especialidad", "Sueldo", "Fuente", "Estado", "Fecha"]
        st.dataframe(df_rec, use_container_width=True)
    else:
        st.info("No hay vacantes registradas aún.")

# -------------------------------------------------------------
# TAB 2: EXPLORADOR DE VACANTES
# -------------------------------------------------------------
with tab2:
    # Filter Toolbar
    f_col1, f_col2, f_col3, f_col4, f_col5 = st.columns([2, 1.5, 1.5, 1.5, 1.5])
    
    with f_col1:
        search_query = st.text_input("🔍 Buscar puesto, empresa, tecnología o ciudad...", placeholder="Ej: Python, RF, Subestaciones, CDMX...")
    
    with f_col2:
        cat_filter = st.selectbox("Especialidad:", [
            "Todos",
            "Ingeniero de RF / Optimización",
            "Ingeniero Eléctrico",
            "Ingeniero de Sistemas / Software"
        ])
    
    with f_col3:
        status_filter = st.selectbox("Estado:", ["Todos", "Pendiente", "Postulado", "Entrevista", "Descartado"])
        
    with f_col4:
        source_filter = st.selectbox("Fuente:", ["Todos", "OCC", "Facebook"])

    with f_col5:
        phone_only = st.checkbox("Solo con WhatsApp 📱", value=False)

    # Fetch Filtered Jobs
    jobs = db.get_jobs(
        category=cat_filter,
        source=source_filter,
        status=status_filter,
        search_query=search_query,
        has_phone_only=phone_only,
        order_by="id DESC"
    )

    st.caption(f"Mostrando **{len(jobs)}** vacantes encontradas:")

    if not jobs:
        st.info("No se encontraron vacantes con los filtros seleccionados.")
    else:
        for job in jobs:
            j_id = job["id"]
            j_title = job["title"]
            j_comp = job["company"]
            j_cat = job["category"]
            j_loc = job["location"] or "México"
            j_mod = job["modality"] or "No especificado"
            j_sal = job["salary_raw"] or "No especificado"
            j_phone = job["phone"]
            j_wa = job["whatsapp_url"]
            j_desc = job["description"] or ""
            j_url = job["url"]
            j_status = job["status"]
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

            # Source Badge
            src_badge = f'<span class="badge-source-occ">🌐 OCC Mundial</span>' if job["source"] == "OCC" else f'<span class="badge-source-fb">📱 Facebook</span>'
            
            # Status Badge
            status_colors = {
                "Pendiente": "🟡 Pendiente",
                "Postulado": "🟢 Postulado",
                "Entrevista": "🟣 En Entrevista",
                "Descartado": "⚪ Descartado"
            }
            status_label = status_colors.get(j_status, j_status)

            with st.container():
                st.markdown(f"""
                <div class="job-card">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <div>
                            <h3 style="margin: 0; color: #0F172A; font-size: 1.25rem;">{j_title}</h3>
                            <p style="margin: 3px 0 0 0; color: #475569; font-weight: 500;">🏢 {j_comp} &nbsp;•&nbsp; 📍 {j_loc} ({j_mod})</p>
                        </div>
                        <div style="text-align: right;">
                            {cat_badge} &nbsp; {src_badge}
                        </div>
                    </div>
                    <div style="margin-top: 10px; display: flex; gap: 15px; align-items: center;">
                        <span class="badge-salary">💰 {j_sal}</span>
                        <span style="font-size: 0.9rem; color: #64748B;"><b>Estado:</b> {status_label}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Action row for the job card
                act_col1, act_col2, act_col3, act_col4, act_col5 = st.columns([2, 1.5, 1.5, 1.5, 1.5])
                
                with act_col1:
                    if j_phone:
                        wa_direct = notifier.generate_whatsapp_link(j_phone, j_title, j_comp, category=j_cat)
                        st.link_button(f"💬 WhatsApp ({j_phone})", wa_direct, use_container_width=True, type="primary")
                    else:
                        st.button(f"📵 Sin Teléfono", disabled=True, key=f"nophone_{j_id}", use_container_width=True)

                with act_col2:
                    if j_url and j_url.startswith("http"):
                        st.link_button("🌐 Ver Vacante", j_url, use_container_width=True)
                    else:
                        st.button("🌐 Enlace N/D", disabled=True, key=f"nourl_{j_id}", use_container_width=True)

                with act_col3:
                    if j_status != "Postulado":
                        if st.button("✅ Postulado", key=f"app_{j_id}", use_container_width=True):
                            db.update_job_status(j_id, "Postulado")
                            st.rerun()
                    else:
                        if st.button("↩️ Pendiente", key=f"pend_{j_id}", use_container_width=True):
                            db.update_job_status(j_id, "Pendiente")
                            st.rerun()

                with act_col4:
                    if j_status != "Entrevista":
                        if st.button("🎯 Entrevista", key=f"ent_{j_id}", use_container_width=True):
                            db.update_job_status(j_id, "Entrevista")
                            st.rerun()

                with act_col5:
                    if st.button("🗑️ Descartar", key=f"del_{j_id}", use_container_width=True):
                        db.delete_job(j_id)
                        st.rerun()

                # Description Expander
                with st.expander(f"📋 Ver Descripción Completa y Notas (#{j_id})"):
                    st.write(j_desc if j_desc else "Sin descripción detallada.")
                    new_notes = st.text_input("Notas personales:", value=j_notes, key=f"notes_{j_id}")
                    if st.button("Guardar Nota", key=f"savenote_{j_id}"):
                        db.update_job_notes(j_id, new_notes)
                        st.success("Nota actualizada.")

                st.markdown("<hr style='margin: 12px 0; border: none; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)

# -------------------------------------------------------------
# TAB 3: SCRAPING & EXTRACCIÓN
# -------------------------------------------------------------
with tab3:
    st.subheader("🔍 Centro de Scraping y Extracción Inteligente")

    sc_col1, sc_col2 = st.columns(2)

    # OCC Scraper Box
    with sc_col1:
        st.markdown("### 🌐 OCC Mundial Bot")
        st.info("Realiza búsquedas automáticas en OCC Mundial según las palabras clave de ingeniería y extrae salario, ubicación y datos de la empresa.")
        
        occ_target = st.selectbox("Especialidad a buscar:", [
            "Todos",
            "Ingeniero de RF / Optimización",
            "Ingeniero Eléctrico",
            "Ingeniero de Sistemas / Software"
        ], key="occ_target_select")

        if st.button("🚀 Ejecutar Scraping en OCC", type="primary", use_container_width=True):
            with st.spinner("Conectando con OCC Mundial y analizando ofertas..."):
                bot = OCCBot()
                categories = None if occ_target == "Todos" else [occ_target]
                res = bot.run_search_and_save(categories=categories)
                st.success(f"✅ ¡Búsqueda completada! Se encontraron {res['total_found']} vacantes y se guardaron {res['total_new']} nuevas.")
                st.rerun()

    # Facebook Post Parser Box
    with sc_col2:
        st.markdown("### 📱 Extractor de Publicaciones de Redes Sociales")
        st.info("Pega el texto de cualquier publicación de Facebook, grupo de WhatsApp o LinkedIn. El sistema extraerá automáticamente el Puesto, Teléfono/WhatsApp, Sueldo y Ubicación.")
        
        sample_paste = st.text_area(
            "Pega aquí el texto de la vacante:",
            height=160,
            placeholder="Ejemplo:\nBuscamos Ingeniero de RF 5G para Huawei en CDMX. Sueldo $35,000 libres. Mandar CV al WhatsApp 55 1234 5678."
        )

        if st.button("⚡ Extraer y Guardar Vacante", use_container_width=True):
            if not sample_paste.strip():
                st.warning("Por favor pega el texto de una publicación.")
            else:
                parsed = extractor.parse_job_post(sample_paste, source="Facebook")
                job_id, is_new = db.add_job(parsed)
                if is_new:
                    st.success(f"¡Vacante extraída y guardada con éxito! (ID #{job_id})")
                else:
                    st.info(f"Vacante actualizada con los nuevos datos (ID #{job_id}).")
                
                # Preview extracted data
                with st.expander("👀 Ver Datos Extraídos"):
                    st.json(parsed)
                st.rerun()

    st.divider()
    st.markdown("### 📡 Escáner de Grupos de Empleo en Redes Sociales")
    st.write("Escanea automáticamente grupos especializados de telecomunicaciones, electricidad y desarrollo de software en México.")
    
    if st.button("🔄 Escanear Todos los Grupos de Empleo", use_container_width=True):
        with st.spinner("Escaneando feeds de grupos de empleo..."):
            fb = FacebookScraper()
            res = fb.run_scan_and_save()
            st.success(f"Escaneo finalizado: {res['total_found']} ofertas revisadas ({res['new_saved']} nuevas añadidas a la base de datos).")
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
        cand_phone = st.text_input("Teléfono de Contacto (WhatsApp):", value=settings.USER_WHATSAPP_PHONE or "+5255XXXXXXXX")
        cand_email = st.text_input("Correo Electrónico:", value=settings.OCC_EMAIL or "correo@ejemplo.com")
        
        st.markdown("#### 📌 Especialidades Objetivo")
        for r in settings.TARGET_ROLES:
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
        cv_target_path = Path(settings.CV_PATH)
        
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
        st.write("Descarga el listado completo de vacantes y postulaciones registradas.")

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
        
        with st.expander("Ver / Editar Variables"):
            occ_mail = st.text_input("OCC Email:", value=settings.OCC_EMAIL)
            fb_mail = st.text_input("Facebook Email:", value=settings.FB_EMAIL)
            wa_ph = st.text_input("WhatsApp Personal:", value=settings.USER_WHATSAPP_PHONE)
            
            if st.button("Guardar Cambios en .env"):
                settings.update_env_variable("OCC_EMAIL", occ_mail)
                settings.update_env_variable("FB_EMAIL", fb_mail)
                settings.update_env_variable("USER_WHATSAPP_PHONE", wa_ph)
                st.success("Variables de entorno actualizadas.")

    st.divider()
    st.markdown("### 🏷️ Palabras Clave y Filtros (`config/keywords.json`)")
    kw_data = settings.get_keywords()
    with st.expander("Ver JSON de Configuración"):
        st.json(kw_data)