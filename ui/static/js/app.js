/**
 * AutoJob Hunter - Vanilla JavaScript Client
 * Handles Dashboard metrics, Chart.js, Job filtering, WhatsApp Simulator, Scrapers & Settings.
 */

// Global Chart instances
let dailyChartInstance = null;
let sourceChartInstance = null;
let categoryChartInstance = null;
let modalityChartInstance = null;

// DOM Ready
document.addEventListener("DOMContentLoaded", () => {
    initApp();
});

function initApp() {
    loadStats();
    loadJobs();
    loadProfile();
    loadSettings();
    setupEventListeners();
}

function showSpinner(text = "Procesando...") {
    const overlay = document.getElementById("spinner-overlay");
    const label = document.getElementById("spinner-text");
    if (label) label.textContent = text;
    if (overlay) overlay.classList.add("show");
}

function hideSpinner() {
    const overlay = document.getElementById("spinner-overlay");
    if (overlay) overlay.classList.remove("show");
}

function showToast(message, type = "success") {
    const toastEl = document.getElementById("liveToast");
    const bodyEl = document.getElementById("toastBody");
    if (!toastEl || !bodyEl) return;

    bodyEl.textContent = message;
    toastEl.className = `toast align-items-center text-white border-0 bg-${type === 'error' ? 'danger' : type === 'info' ? 'info' : 'success'}`;
    const toast = new bootstrap.Toast(toastEl, { delay: 3500 });
    toast.show();
}

// -------------------------------------------------------------
// STATS & CHARTS
// -------------------------------------------------------------
async function loadStats() {
    try {
        const res = await fetch("/api/stats");
        const data = await res.json();
        if (!data.success) throw new Error(data.error || "Error al cargar estadísticas");

        const appStats = data.applications;
        const genStats = data.general;

        // Update KPIs
        const elApplied = document.getElementById("kpi-applied");
        const elToday = document.getElementById("kpi-today");
        const elWeek = document.getElementById("kpi-week");
        const elMonth = document.getElementById("kpi-month");
        const elInterview = document.getElementById("kpi-interview");
        const elConversion = document.getElementById("kpi-conversion");

        if (elApplied) elApplied.textContent = appStats.applied_count;
        if (elToday) elToday.textContent = appStats.today_count;
        if (elWeek) elWeek.textContent = appStats.week_count;
        if (elMonth) elMonth.textContent = appStats.month_count;
        if (elInterview) elInterview.textContent = appStats.interview_count;
        if (elConversion) elConversion.textContent = `Éxito: ${appStats.conversion_rate}%`;

        // Update Sidebar KPIs
        const sideApplied = document.getElementById("side-kpi-applied");
        const sideToday = document.getElementById("side-kpi-today");
        const sideInterview = document.getElementById("side-kpi-interview");
        const sidePending = document.getElementById("side-kpi-pending");
        const sideTotal = document.getElementById("side-kpi-total");

        if (sideApplied) sideApplied.textContent = appStats.applied_count;
        if (sideToday) sideToday.textContent = appStats.today_count;
        if (sideInterview) sideInterview.textContent = appStats.interview_count;
        if (sidePending) sidePending.textContent = genStats.pending_count || 0;
        if (sideTotal) sideTotal.textContent = genStats.total_jobs || 215;

        // Update Quick Filter Pill Counts in Tab 2
        const qcAll = document.getElementById("quick-count-all");
        const qcApp = document.getElementById("quick-count-applied");
        const qcToday = document.getElementById("quick-count-today");
        const qcInt = document.getElementById("quick-count-interview");
        const qcPen = document.getElementById("quick-count-pending");

        if (qcAll) qcAll.textContent = genStats.total_jobs || 215;
        if (qcApp) qcApp.textContent = appStats.applied_count;
        if (qcToday) qcToday.textContent = appStats.today_count;
        if (qcInt) qcInt.textContent = appStats.interview_count;
        if (qcPen) qcPen.textContent = genStats.pending_count || 0;

        // Update Tracked Applications Table Counts in Tab 1
        const tcAll = document.getElementById("tracked-count-all");
        const tcApp = document.getElementById("tracked-count-applied");
        const tcToday = document.getElementById("tracked-count-today");
        const tcInt = document.getElementById("tracked-count-interview");

        if (tcAll) tcAll.textContent = appStats.total_active_applied;
        if (tcApp) tcApp.textContent = appStats.applied_count;
        if (tcToday) tcToday.textContent = appStats.today_count;
        if (tcInt) tcInt.textContent = appStats.interview_count;

        // Render Platform Ranking
        const bySource = genStats.by_source || {};
        const totalRealJobs = genStats.total_jobs || 215;
        renderPlatformRanking(bySource, totalRealJobs);

        // Render Charts
        renderDailyChart(appStats.daily_applications || {});
        renderSourceChart(bySource);
        renderCategoryChart(genStats.by_category || appStats.applied_by_category || {});
        renderModalityChart(genStats.by_modality || appStats.applied_by_modality || {});

        // Render Tracked Applications Table
        renderTrackedTable('refresh');

    } catch (err) {
        console.error("Error loading stats:", err);
    }
}

const PLATFORM_META = {
    "OCC": { name: "OCC Mundial", color: "#2563EB", icon: "🌐", badge: "badge-source-occ" },
    "LinkedIn": { name: "LinkedIn", color: "#0A66C2", icon: "💼", badge: "badge-source-linkedin" },
    "Facebook": { name: "Facebook", color: "#1877F2", icon: "📱", badge: "badge-source-fb" },
    "CompuTrabajo": { name: "CompuTrabajo", color: "#EA580C", icon: "🟧", badge: "badge-source-computrabajo" },
    "Jobrapido": { name: "Jobrapido", color: "#0284C7", icon: "🧭", badge: "badge-source-jobrapido" },
    "Glassdoor": { name: "Glassdoor", color: "#059669", icon: "🟢", badge: "badge-source-glassdoor" },
    "JobLeads": { name: "JobLeads", color: "#7C3AED", icon: "🎯", badge: "badge-source-jobleads" },
    "Jobsora": { name: "Jobsora", color: "#DC2626", icon: "🔴", badge: "badge-source-jobsora" }
};

function renderPlatformRanking(bySource, totalRealJobs) {
    const total = totalRealJobs || 215;
    const rankTotalEl = document.getElementById("rank-total-count");
    if (rankTotalEl) rankTotalEl.textContent = total;
    const sideTotalSources = document.getElementById("side-total-sources");
    if (sideTotalSources) sideTotalSources.textContent = total;

    // Sort platforms descending by quantity to see which gives the highest
    const sorted = Object.keys(bySource).sort((a, b) => bySource[b] - bySource[a]);

    // 1. Render Progress Bars in Tab 1
    const barsContainer = document.getElementById("platformRankingBars");
    if (barsContainer) {
        barsContainer.innerHTML = sorted.map((src, index) => {
            const count = bySource[src];
            const pct = total > 0 ? ((count / total) * 100).toFixed(1) : "0.0";
            const meta = PLATFORM_META[src] || { name: src, color: "#475569", icon: "💼", badge: "badge-general" };
            const isTop = index === 0;
            const rankBadge = index === 0 ? "🥇" : index === 1 ? "🥈" : index === 2 ? "🥉" : `#${index + 1}`;

            return `
                <div class="platform-rank-item">
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="d-flex align-items-center gap-2">
                            <span class="fw-bold fs-6">${rankBadge}</span>
                            <span class="badge ${meta.badge}">${meta.icon} ${meta.name}</span>
                            ${isTop ? '<span class="badge bg-success-subtle text-success border border-success-subtle small ms-1"><i class="bi bi-star-fill me-1"></i>Mayor fuente de vacantes</span>' : ''}
                        </div>
                        <div class="text-end">
                            <strong class="fs-6 text-dark">${count}</strong>
                            <span class="text-muted small ms-1">(${pct}%)</span>
                        </div>
                    </div>
                    <div class="platform-rank-bar-bg">
                        <div class="platform-rank-bar-fill" style="width: ${pct}%; background-color: ${meta.color};"></div>
                    </div>
                </div>
            `;
        }).join("");
    }

    // 2. Render Table in Tab 1
    const tableBody = document.getElementById("platformRankingTableBody");
    if (tableBody) {
        tableBody.innerHTML = sorted.map((src, index) => {
            const count = bySource[src];
            const pct = total > 0 ? ((count / total) * 100).toFixed(1) : "0.0";
            const meta = PLATFORM_META[src] || { name: src, color: "#475569", icon: "💼", badge: "badge-general" };
            const rankLabel = index === 0 ? '<span class="badge bg-warning text-dark">1º</span>' :
                              index === 1 ? '<span class="badge bg-secondary text-white">2º</span>' :
                              index === 2 ? '<span class="badge bg-danger-subtle text-danger">3º</span>' :
                              `<span class="text-muted small">${index + 1}º</span>`;

            return `
                <tr>
                    <td class="ps-3 fw-bold">${rankLabel}</td>
                    <td>
                        <span class="badge ${meta.badge}">${meta.icon} ${meta.name}</span>
                    </td>
                    <td class="text-center fw-bold text-dark">${count}</td>
                    <td class="text-end pe-3">
                        <span class="badge bg-light text-dark border">${pct}%</span>
                    </td>
                </tr>
            `;
        }).join("");
    }

    // 3. Render Left Sidebar Platform Breakdown
    const sidebarContainer = document.getElementById("side-platform-breakdown");
    if (sidebarContainer) {
        sidebarContainer.innerHTML = sorted.map((src, index) => {
            const count = bySource[src];
            const meta = PLATFORM_META[src] || { name: src, color: "#475569", icon: "💼", badge: "badge-general" };
            return `
                <li class="list-group-item d-flex justify-content-between align-items-center px-0 py-1 border-0">
                    <span class="d-flex align-items-center gap-1 text-truncate" style="max-width: 140px;" title="${meta.name}">
                        <span class="small">${meta.icon}</span>
                        <span class="text-truncate">${meta.name}</span>
                    </span>
                    <span class="badge ${index === 0 ? 'bg-primary' : 'bg-secondary'} rounded-pill">${count}</span>
                </li>
            `;
        }).join("");
    }
}

function renderDailyChart(dailyData) {
    const ctx = document.getElementById("dailyChart");
    if (!ctx) return;

    const labels = Object.keys(dailyData).sort();
    const values = labels.map(k => dailyData[k]);

    if (dailyChartInstance) dailyChartInstance.destroy();

    dailyChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels.length ? labels : ['Sin datos'],
            datasets: [{
                label: 'Gestiones Diarias',
                data: values.length ? values : [0],
                backgroundColor: '#2563EB',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, ticks: { precision: 0 } }
            }
        }
    });

    // Populate daily summary table
    const tableBody = document.getElementById("dailyTableBody");
    if (tableBody) {
        if (!labels.length) {
            tableBody.innerHTML = `<tr><td colspan="2" class="text-center text-muted">Sin actividad registrada</td></tr>`;
        } else {
            tableBody.innerHTML = labels.map(date => `
                <tr>
                    <td><strong>${date}</strong></td>
                    <td class="text-end"><span class="badge bg-primary">${dailyData[date]}</span></td>
                </tr>
            `).join("");
        }
    }
}

function renderSourceChart(srcData) {
    const ctx = document.getElementById("sourceChart");
    if (!ctx) return;

    // Sort descending by count
    const labels = Object.keys(srcData).sort((a, b) => srcData[b] - srcData[a]);
    const values = labels.map(k => srcData[k]);
    const bgColors = labels.map(k => (PLATFORM_META[k] ? PLATFORM_META[k].color : "#0284C7"));

    if (sourceChartInstance) sourceChartInstance.destroy();

    sourceChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels.length ? labels : ['Sin datos'],
            datasets: [{
                label: 'Oportunidades Reales',
                data: values.length ? values : [0],
                backgroundColor: bgColors,
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
        }
    });
}

function renderCategoryChart(catData) {
    const ctx = document.getElementById("categoryChart");
    if (!ctx) return;

    const labels = Object.keys(catData);
    const values = labels.map(k => catData[k]);

    if (categoryChartInstance) categoryChartInstance.destroy();

    categoryChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels.length ? labels : ['Sin datos'],
            datasets: [{
                data: values.length ? values : [0],
                backgroundColor: '#10B981',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
        }
    });
}

function renderModalityChart(modData) {
    const ctx = document.getElementById("modalityChart");
    if (!ctx) return;

    const labels = Object.keys(modData);
    const values = labels.map(k => modData[k]);

    if (modalityChartInstance) modalityChartInstance.destroy();

    modalityChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels.length ? labels : ['Sin datos'],
            datasets: [{
                data: values.length ? values : [0],
                backgroundColor: '#F59E0B',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
        }
    });
}

let trackedApplicationsCache = [];

async function renderTrackedTable(filter = 'all') {
    const tbody = document.getElementById("trackedTableBody");
    if (!tbody) return;

    try {
        if (!trackedApplicationsCache.length || filter === 'refresh') {
            const [resApp, resInt] = await Promise.all([
                fetch("/api/jobs?status=Postulado"),
                fetch("/api/jobs?status=Entrevista")
            ]);
            const dataApp = await resApp.json();
            const dataInt = await resInt.json();
            trackedApplicationsCache = [...(dataApp.jobs || []), ...(dataInt.jobs || [])];
        }

        const todayStr = new Date().toISOString().substring(0, 10);
        let filtered = trackedApplicationsCache;

        if (filter === 'Postulado') {
            filtered = trackedApplicationsCache.filter(j => j.status === 'Postulado');
        } else if (filter === 'Entrevista') {
            filtered = trackedApplicationsCache.filter(j => j.status === 'Entrevista');
        } else if (filter === 'hoy') {
            filtered = trackedApplicationsCache.filter(j => {
                const appDay = j.applied_at ? j.applied_at.substring(0, 10) : '';
                const updDay = j.updated_at ? j.updated_at.substring(0, 10) : '';
                return appDay === todayStr || updDay === todayStr;
            });
        }

        if (!filtered.length) {
            const label = filter === 'Postulado' ? 'postuladas' : filter === 'Entrevista' ? 'en cotización' : filter === 'hoy' ? 'gestionadas hoy' : 'en seguimiento';
            tbody.innerHTML = `<tr><td colspan="7" class="text-center py-4 text-muted">No hay oportunidades ${label} todavía.</td></tr>`;
            return;
        }

        tbody.innerHTML = filtered.map(j => `
            <tr>
                <td><small class="text-muted">${j.applied_at ? j.applied_at.substring(0, 16) : 'N/D'}</small></td>
                <td><strong>${escapeHtml(j.title)}</strong></td>
                <td>${escapeHtml(j.company)}</td>
                <td><span class="badge bg-light text-dark border">${escapeHtml(j.source || 'OCC')}</span></td>
                <td>${j.phone ? `<a href="tel:${j.phone}" class="text-decoration-none">📞 ${escapeHtml(j.phone)}</a>` : '<span class="text-muted">N/D</span>'}</td>
                <td>
                    <span class="badge ${j.status === 'Entrevista' ? 'bg-info text-dark' : 'bg-primary'}">
                        ${escapeHtml(j.status === 'Entrevista' ? '🟣 En Cotización' : '🎯 Postulado')}
                    </span>
                </td>
                <td>${j.whatsapp_url ? `<a href="${j.whatsapp_url}" target="_blank" class="btn btn-sm btn-outline-success"><i class="bi bi-whatsapp"></i> Chat</a>` : '-'}</td>
            </tr>
        `).join("");
    } catch (e) {
        console.error("Error loading tracked jobs:", e);
    }
}

function filterTrackedTable(filter, btn) {
    if (btn) {
        document.querySelectorAll("#trackedFilterBtns .btn").forEach(b => {
            b.classList.remove("active", "btn-primary", "btn-success", "btn-info");
            if (b.id === 'btn-tracked-today') b.classList.add("btn-outline-success");
            else if (b.id === 'btn-tracked-interview') b.classList.add("btn-outline-info");
            else b.classList.add("btn-outline-primary");
        });
        btn.classList.add("active");
        if (btn.id === 'btn-tracked-today') {
            btn.classList.remove("btn-outline-success");
            btn.classList.add("btn-success");
        } else if (btn.id === 'btn-tracked-interview') {
            btn.classList.remove("btn-outline-info");
            btn.classList.add("btn-info");
        } else {
            btn.classList.remove("btn-outline-primary");
            btn.classList.add("btn-primary");
        }
    }
    renderTrackedTable(filter);
}

// -------------------------------------------------------------
// FILTERING SHORTCUTS & INTERACTION
// -------------------------------------------------------------
function filterByStatusQuick(status) {
    // 1. Switch active pill tab to Tab 2 (Bolsa de Vacantes)
    const tabBtn = document.getElementById("tab-jobs-btn");
    if (tabBtn) {
        const tab = bootstrap.Tab.getInstance(tabBtn) || new bootstrap.Tab(tabBtn);
        tab.show();
    }

    // 2. Select quick filter and reload jobs
    selectQuickFilter(status);

    // 3. Smooth scroll down to the filtered results
    setTimeout(() => {
        const target = document.getElementById("jobFilterForm") || document.getElementById("jobsContainer");
        if (target) {
            target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    }, 150);

    // 4. Synchronize tracked table in Tab 1 if applicable
    if (status === 'Postulado' || status === 'hoy' || status === 'Entrevista') {
        filterTrackedTable(status);
    }
}

function selectQuickFilter(status) {
    // 1. Sync dropdown
    const statusDropdown = document.getElementById("filterStatus");
    if (statusDropdown) {
        statusDropdown.value = status;
    }

    // 2. Update pill buttons active classes and styles
    document.querySelectorAll(".btn-quick-filter").forEach(btn => {
        const btnStatus = btn.getAttribute("data-status");
        if (btnStatus === status) {
            btn.classList.add("active");
            btn.classList.remove("btn-outline-dark", "btn-outline-primary", "btn-outline-success", "btn-outline-info", "btn-outline-secondary");
            if (status === 'Todos') btn.classList.add("btn-dark");
            else if (status === 'Postulado') btn.classList.add("btn-primary");
            else if (status === 'hoy') btn.classList.add("btn-success");
            else if (status === 'Entrevista') btn.classList.add("btn-info");
            else if (status === 'Pendiente') btn.classList.add("btn-secondary");
        } else {
            btn.classList.remove("active", "btn-dark", "btn-primary", "btn-success", "btn-info", "btn-secondary");
            if (btnStatus === 'Todos') btn.classList.add("btn-outline-dark");
            else if (btnStatus === 'Postulado') btn.classList.add("btn-outline-primary");
            else if (btnStatus === 'hoy') btn.classList.add("btn-outline-success");
            else if (btnStatus === 'Entrevista') btn.classList.add("btn-outline-info");
            else if (btnStatus === 'Pendiente') btn.classList.add("btn-outline-secondary");
        }
    });

    // 3. Load jobs with new filter
    loadJobs();
}

function onStatusDropdownChange(status) {
    selectQuickFilter(status);
}


// -------------------------------------------------------------
// JOBS & QUOTATIONS EXPLORER
// -------------------------------------------------------------
async function loadJobs() {
    const container = document.getElementById("jobsContainer");
    const countEl = document.getElementById("resultsCount");
    if (!container) return;

    container.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2 text-muted">Cargando oportunidades laborales y cotizaciones...</p>
        </div>
    `;

    const searchQuery = document.getElementById("filterSearch")?.value || "";
    const location = document.getElementById("filterCity")?.value || "";
    const category = document.getElementById("filterCategory")?.value || "Todas";
    const source = document.getElementById("filterSource")?.value || "Todas";
    const status = document.getElementById("filterStatus")?.value || "Todos";
    const modality = document.getElementById("filterModality")?.value || "Todas";
    const hasPhoneOnly = document.getElementById("filterPhoneOnly")?.checked || false;

    const params = new URLSearchParams();
    if (searchQuery.trim()) params.append("search_query", searchQuery.trim());
    if (location.trim()) params.append("location", location.trim());
    if (category !== "Todas") params.append("category", category);
    if (source !== "Todas") params.append("source", source);
    if (modality !== "Todas") params.append("modality", modality);
    if (hasPhoneOnly) params.append("has_phone_only", "true");

    if (status === "hoy" || status === "Gestionadas Hoy") {
        params.append("managed_today", "true");
    } else if (status !== "Todos") {
        params.append("status", status);
    }

    try {
        const res = await fetch(`/api/jobs?${params.toString()}`);
        const data = await res.json();
        if (!data.success) throw new Error(data.error || "Error al cargar vacantes");

        const jobs = data.jobs || [];
        if (countEl) countEl.textContent = jobs.length;

        // Label for active filter badge
        const activeFilterLabel = status === 'Postulado' ? '🎯 Oportunidades Postuladas' :
                                  status === 'hoy' ? '📅 Gestionadas Hoy' :
                                  status === 'Entrevista' ? '🟣 En Cotización / Entrevista' :
                                  status === 'Pendiente' ? '🟢 Oportunidades Pendientes' :
                                  status === 'Descartado' ? '⚪ Oportunidades Descartadas' : '';

        let filterBanner = "";
        if (activeFilterLabel) {
            filterBanner = `
                <div class="alert alert-primary py-2 px-3 mb-3 d-flex justify-content-between align-items-center rounded-3 border-0 bg-primary-subtle text-primary shadow-sm">
                    <div>
                        <i class="bi bi-funnel-fill me-1"></i> Filtro activo: <strong>${activeFilterLabel}</strong> &nbsp;•&nbsp; <span>${jobs.length} encontradas</span>
                    </div>
                    <button type="button" class="btn btn-sm btn-outline-primary py-0 px-2" onclick="selectQuickFilter('Todos')">
                        <i class="bi bi-x-circle me-1"></i> Mostrar todas
                    </button>
                </div>
            `;
        }

        if (jobs.length === 0) {
            container.innerHTML = filterBanner + `
                <div class="alert alert-info py-4 text-center">
                    <i class="bi bi-info-circle fs-3 d-block mb-2"></i>
                    No se encontraron oportunidades con los criterios de búsqueda seleccionados.
                </div>
            `;
            return;
        }

        container.innerHTML = filterBanner + jobs.map(j => renderJobCard(j)).join("");

    } catch (err) {
        console.error("Error loading jobs:", err);
        container.innerHTML = `
            <div class="alert alert-danger py-4 text-center">
                Error al conectar con la base de datos: ${err.message}
            </div>
        `;
    }
}

function renderJobCard(job) {
    const isQuoteLead = (job.title + " " + (job.description || "")).toLowerCase().includes("cotiza") ||
                        (job.title + " " + (job.description || "")).toLowerCase().includes("instala") ||
                        (job.title + " " + (job.description || "")).toLowerCase().includes("presupuesto");

    // Category Badge
    let catBadge = `<span class="badge badge-general">💼 ${escapeHtml(job.category)}</span>`;
    if (job.category.includes("Medio Oficial")) {
        catBadge = `<span class="badge badge-medio-oficial">🔧 ${escapeHtml(job.category)}</span>`;
    } else if (job.category.includes("Oficial")) {
        catBadge = `<span class="badge badge-oficial">👷 ${escapeHtml(job.category)}</span>`;
    } else if (job.category.includes("RF")) {
        catBadge = `<span class="badge badge-rf">📡 ${escapeHtml(job.category)}</span>`;
    } else if (job.category.includes("Eléctric")) {
        catBadge = `<span class="badge badge-electric">⚡ ${escapeHtml(job.category)}</span>`;
    } else if (job.category.includes("Sistemas") || job.category.includes("Software")) {
        catBadge = `<span class="badge badge-software">💻 ${escapeHtml(job.category)}</span>`;
    } else if (job.category.includes("Performance")) {
        catBadge = `<span class="badge badge-performance">📈 ${escapeHtml(job.category)}</span>`;
    } else if (job.category.includes("NOC")) {
        catBadge = `<span class="badge badge-noc">🖥️ ${escapeHtml(job.category)}</span>`;
    } else if (job.category.includes("Web")) {
        catBadge = `<span class="badge badge-web">🌐 ${escapeHtml(job.category)}</span>`;
    } else if (job.category.includes("Backend")) {
        catBadge = `<span class="badge badge-backend">⚙️ ${escapeHtml(job.category)}</span>`;
    } else if (job.category.includes("Frontend")) {
        catBadge = `<span class="badge badge-frontend">🎨 ${escapeHtml(job.category)}</span>`;
    }

    // Source Badge
    let srcClass = "badge-source-fb";
    const src = job.source || "OCC";
    if (src === "OCC") srcClass = "badge-source-occ";
    else if (src === "LinkedIn") srcClass = "badge-source-linkedin";
    else if (src === "CompuTrabajo") srcClass = "badge-source-computrabajo";
    else if (src === "Glassdoor") srcClass = "badge-source-glassdoor";
    else if (src === "Jobrapido") srcClass = "badge-source-jobrapido";
    else if (src === "JobLeads") srcClass = "badge-source-jobleads";
    else if (src === "Jobsora") srcClass = "badge-source-jobsora";
    const srcBadge = `<span class="badge ${srcClass}">🌐 ${escapeHtml(src)}</span>`;

    // Status Badge
    let statusBadge = `<span class="badge bg-warning text-dark">🟡 Pendiente</span>`;
    if (job.status === "Postulado") {
        statusBadge = `<span class="badge bg-success">🟢 Postulado / En Contacto</span>`;
    } else if (job.status === "Entrevista") {
        statusBadge = `<span class="badge bg-info text-dark">🟣 Cotización / Entrevista</span>`;
    } else if (job.status === "Descartado") {
        statusBadge = `<span class="badge bg-secondary">⚪ Descartado</span>`;
    }

    const waLabel = isQuoteLead ? "💬 Cotizar wa.me" : "💬 wa.me";
    const waLinkHtml = job.whatsapp_url
        ? `<a href="${job.whatsapp_url}" target="_blank" class="badge-whatsapp"><i class="bi bi-whatsapp"></i> ${waLabel}</a>`
        : "";

    const phoneHtml = job.phone
        ? `<span class="badge badge-phone"><i class="bi bi-telephone-fill me-1"></i>${escapeHtml(job.phone)}</span>`
        : `<span class="text-muted small">📵 Sin teléfono</span>`;

    return `
        <div class="job-item-card" id="job-card-${job.id}">
            <div class="d-flex justify-content-between align-items-start mb-2">
                <div>
                    <h4 class="job-title">${escapeHtml(job.title)}</h4>
                    <div class="job-company">
                        🏢 ${escapeHtml(job.company)} &nbsp;•&nbsp; 📍 ${escapeHtml(job.location || 'México')} &nbsp;
                        <span class="contact-tag">👤 Contacto: ${escapeHtml(job.company)}</span>
                    </div>
                </div>
                <div class="text-end">
                    ${catBadge} ${srcBadge}
                </div>
            </div>

            <div class="d-flex gap-2 align-items-center flex-wrap my-3">
                <span class="badge badge-salary">💰 ${escapeHtml(job.salary_raw || 'No especificado')}</span>
                <span class="badge badge-modality">🏢 ${escapeHtml(job.modality || 'No especificado')}</span>
                ${phoneHtml}
                ${waLinkHtml}
                <span class="ms-auto">${statusBadge}</span>
            </div>

            <!-- Quick Action Buttons Row -->
            <div class="row g-2 align-items-center pt-2 border-top">
                <div class="col-md-3">
                    ${job.whatsapp_url ? `
                        <a href="${job.whatsapp_url}" target="_blank" class="btn btn-success btn-sm w-100 fw-bold">
                            <i class="bi bi-whatsapp"></i> ${isQuoteLead ? 'Cotizar WhatsApp' : 'WhatsApp'}
                        </a>
                    ` : `
                        <button class="btn btn-outline-secondary btn-sm w-100" disabled>📵 Sin Teléfono</button>
                    `}
                </div>
                <div class="col-md-2">
                    ${job.phone ? `
                        <a href="tel:${job.phone}" class="btn btn-outline-primary btn-sm w-100">
                            <i class="bi bi-telephone"></i> Llamar
                        </a>
                    ` : (job.url && job.url.startsWith("http") ? `
                        <a href="${job.url}" target="_blank" class="btn btn-outline-primary btn-sm w-100">
                            <i class="bi bi-box-arrow-up-right"></i> Ver Enlace
                        </a>
                    ` : `
                        <button class="btn btn-outline-secondary btn-sm w-100" disabled>Sin Enlace</button>
                    `)}
                </div>
                <div class="col-md-3">
                    <button class="btn btn-sm w-100 ${job.status === 'Postulado' ? 'btn-primary' : 'btn-outline-primary'}"
                            onclick="toggleJobStatus(${job.id}, '${job.status === 'Postulado' ? 'Pendiente' : 'Postulado'}')">
                        ${job.status === 'Postulado' ? '✅ En Contacto' : '⬜ Postular / Contactar'}
                    </button>
                </div>
                <div class="col-md-3">
                    <button class="btn btn-sm w-100 ${job.status === 'Entrevista' ? 'btn-info text-dark fw-bold' : 'btn-outline-info text-dark'}"
                            onclick="toggleJobStatus(${job.id}, '${job.status === 'Entrevista' ? 'Pendiente' : 'Entrevista'}')">
                        ${job.status === 'Entrevista' ? '🟣 En Cotización' : '🎯 Cotizar / Entrevista'}
                    </button>
                </div>
                <div class="col-md-1">
                    <button class="btn btn-outline-danger btn-sm w-100" title="Descartar" onclick="deleteJob(${job.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>

            <!-- Accordion Details -->
            <div class="accordion mt-3" id="accordionJob-${job.id}">
                <div class="accordion-item border-0">
                    <h2 class="accordion-header">
                        <button class="accordion-button collapsed py-2 px-3 bg-light rounded text-secondary" type="button" data-bs-toggle="collapse" data-bs-target="#collapseJob-${job.id}">
                            <i class="bi bi-file-text me-2"></i> Ficha Técnica, Contacto y Alcance del Trabajo (#${job.id})
                        </button>
                    </h2>
                    <div id="collapseJob-${job.id}" class="accordion-collapse collapse" data-bs-parent="#accordionJob-${job.id}">
                        <div class="accordion-body bg-light rounded mt-2">
                            <div class="row g-3 mb-3">
                                <div class="col-md-4">
                                    <small class="text-muted d-block">Cliente / Contacto</small>
                                    <code>${escapeHtml(job.company)}</code>
                                    <small class="text-muted d-block mt-2">Ubicación</small>
                                    <strong>${escapeHtml(job.location || 'México')}</strong>
                                </div>
                                <div class="col-md-4">
                                    <small class="text-muted d-block">Teléfono de Contacto</small>
                                    <strong>${escapeHtml(job.phone || 'No especificado')}</strong>
                                    <small class="text-muted d-block mt-2">Plataforma Origen</small>
                                    <strong>${escapeHtml(job.source || 'OCC')}</strong>
                                </div>
                                <div class="col-md-4">
                                    <small class="text-muted d-block">WhatsApp Link</small>
                                    ${job.whatsapp_url ? `<a href="${job.whatsapp_url}" target="_blank" class="small text-break">${job.whatsapp_url}</a>` : '<code>No disponible</code>'}
                                </div>
                            </div>

                            <hr class="my-2">
                            <h6>📄 Detalle del Requerimiento / Alcance de Instalación:</h6>
                            <p class="small text-secondary" style="white-space: pre-wrap;">${escapeHtml(job.description || 'Sin descripción detallada.')}</p>

                            <hr class="my-2">
                            <div class="row g-2 align-items-center">
                                <div class="col-md-9">
                                    <input type="text" id="notes-input-${job.id}" class="form-control form-control-sm"
                                           placeholder="Escribe notas de seguimiento o cotización..." value="${escapeHtml(job.notes || '')}">
                                </div>
                                <div class="col-md-3">
                                    <button class="btn btn-sm btn-secondary w-100" onclick="saveJobNotes(${job.id})">
                                        <i class="bi bi-floppy"></i> Guardar Nota
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

async function toggleJobStatus(jobId, newStatus) {
    try {
        const res = await fetch(`/api/jobs/${jobId}/status`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ status: newStatus })
        });
        const data = await res.json();
        if (data.success) {
            showToast(`Oportunidad #${jobId} actualizada a '${newStatus}'`);
            loadJobs();
            loadStats();
        } else {
            showToast(data.error || "Error al actualizar estado", "error");
        }
    } catch (e) {
        showToast("Error de conexión al servidor", "error");
    }
}

async function saveJobNotes(jobId) {
    const input = document.getElementById(`notes-input-${jobId}`);
    if (!input) return;
    const notes = input.value;

    try {
        const res = await fetch(`/api/jobs/${jobId}/notes`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ notes })
        });
        const data = await res.json();
        if (data.success) {
            showToast(`Nota guardada para la oportunidad #${jobId}`);
        } else {
            showToast("Error al guardar nota", "error");
        }
    } catch (e) {
        showToast("Error al conectar con el servidor", "error");
    }
}

async function deleteJob(jobId) {
    if (!confirm("¿Deseas descartar y eliminar esta oportunidad?")) return;
    try {
        const res = await fetch(`/api/jobs/${jobId}`, { method: "DELETE" });
        const data = await res.json();
        if (data.success) {
            showToast(`Oportunidad #${jobId} eliminada`);
            const card = document.getElementById(`job-card-${jobId}`);
            if (card) card.remove();
            loadStats();
        } else {
            showToast("Error al eliminar", "error");
        }
    } catch (e) {
        showToast("Error al conectar con el servidor", "error");
    }
}


// -------------------------------------------------------------
// WHATSAPP BOT SIMULATOR
// -------------------------------------------------------------
async function sendWhatsAppCommand(cmd) {
    const input = document.getElementById("waCmdInput");
    const activeCmd = cmd || (input ? input.value.trim() : "");
    if (!activeCmd) return;

    if (input && cmd) input.value = cmd;

    const previewContainer = document.getElementById("waBubbleContainer");
    if (previewContainer) {
        previewContainer.innerHTML = `<div class="wa-bubble text-muted"><div class="spinner-border spinner-border-sm me-2"></div>Procesando en el Bot...</div>`;
    }

    try {
        const res = await fetch("/api/whatsapp/simulate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: activeCmd })
        });
        const data = await res.json();
        if (data.success && previewContainer) {
            previewContainer.innerHTML = `<div class="wa-bubble">${escapeHtml(data.reply)}</div>`;
        } else if (previewContainer) {
            previewContainer.innerHTML = `<div class="wa-bubble text-danger">Error: ${escapeHtml(data.error)}</div>`;
        }
    } catch (e) {
        if (previewContainer) {
            previewContainer.innerHTML = `<div class="wa-bubble text-danger">Error de comunicación con el motor de WhatsApp</div>`;
        }
    }
}


// -------------------------------------------------------------
// SCRAPERS & EXTRACTION
// -------------------------------------------------------------
async function runScraper(name, categorySelectorId = null) {
    let category = "Todos";
    if (categorySelectorId) {
        const el = document.getElementById(categorySelectorId);
        if (el) category = el.value;
    }

    const platformNames = {
        all: "TODAS las plataformas",
        fb: "Facebook (Cotizaciones)",
        linkedin: "LinkedIn",
        occ: "OCC Mundial",
        computrabajo: "CompuTrabajo",
        glassdoor: "Glassdoor",
        jobrapido: "Jobrapido",
        jobleads: "JobLeads",
        jobsora: "Jobsora"
    };

    const label = platformNames[name] || name;
    showSpinner(`Escaneando ${label}... Esto puede tardar unos segundos.`);

    try {
        const res = await fetch("/api/scrapers/run", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ scraper: name, category })
        });
        const data = await res.json();
        hideSpinner();

        if (data.success) {
            const count = data.total_new !== undefined ? data.total_new : (data.details?.total_new || 0);
            showToast(`¡Escaneo de ${label} terminado! ${count} nuevas oportunidades registradas.`);
            loadJobs();
            loadStats();
        } else {
            showToast(`Error en escaneo: ${data.error}`, "error");
        }
    } catch (e) {
        hideSpinner();
        showToast(`Error al ejecutar scraper: ${e.message}`, "error");
    }
}

async function extractPastedJob() {
    const textarea = document.getElementById("pasteJobText");
    const text = textarea ? textarea.value.trim() : "";
    if (!text) {
        showToast("Por favor pega el texto de una publicación primero", "error");
        return;
    }

    showSpinner("Extrayendo entidades (puesto, cliente, teléfono, salario)...");

    try {
        const res = await fetch("/api/extract", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, source: "Facebook" })
        });
        const data = await res.json();
        hideSpinner();

        if (data.success) {
            showToast(`¡Oportunidad extraída y guardada con éxito! (ID #${data.job_id})`);
            const resCard = document.getElementById("extractResultCard");
            const resBody = document.getElementById("extractResultBody");
            if (resCard && resBody) {
                resCard.classList.remove("d-none");
                const p = data.parsed;
                resBody.innerHTML = `
                    <div class="row g-3">
                        <div class="col-md-4">📌 <strong>Requerimiento:</strong> ${escapeHtml(p.title || '')}</div>
                        <div class="col-md-4">🏢 <strong>Contacto/Cliente:</strong> <code>${escapeHtml(p.company || '')}</code></div>
                        <div class="col-md-4">📞 <strong>Teléfono:</strong> <code>${escapeHtml(p.phone || 'N/D')}</code></div>
                        <div class="col-md-4">💰 <strong>Presupuesto:</strong> <code>${escapeHtml(p.salary_raw || 'N/D')}</code></div>
                        <div class="col-md-8">💬 <strong>WhatsApp:</strong> ${p.whatsapp_url ? `<a href="${p.whatsapp_url}" target="_blank">${p.whatsapp_url}</a>` : '<code>N/D</code>'}</div>
                    </div>
                `;
            }
            if (textarea) textarea.value = "";
            loadJobs();
            loadStats();
        } else {
            showToast(data.error || "Error al extraer datos", "error");
        }
    } catch (e) {
        hideSpinner();
        showToast("Error de conexión al servidor", "error");
    }
}


// -------------------------------------------------------------
// PROFILE & TEMPLATES
// -------------------------------------------------------------
async function loadProfile() {
    try {
        const res = await fetch("/api/profile");
        const data = await res.json();
        if (!data.success) return;

        const p = data.profile;
        const cv = data.cv;
        const t = data.templates;

        if (document.getElementById("profName")) document.getElementById("profName").value = p.name || "";
        if (document.getElementById("profPhone")) document.getElementById("profPhone").value = p.phone || "";
        if (document.getElementById("profEmail")) document.getElementById("profEmail").value = p.email || "";

        if (document.getElementById("templateApp")) document.getElementById("templateApp").value = t.application || "";
        if (document.getElementById("templateQuote")) document.getElementById("templateQuote").value = t.quotation || "";

        const cvStatusEl = document.getElementById("cvStatusContainer");
        if (cvStatusEl) {
            if (cv.exists) {
                cvStatusEl.innerHTML = `
                    <div class="alert alert-success d-flex justify-content-between align-items-center py-2 mb-3">
                        <div>
                            <i class="bi bi-file-earmark-pdf-fill fs-4 me-2 text-danger"></i>
                            <strong>${escapeHtml(cv.filename)}</strong> (${cv.size_kb} KB)
                        </div>
                        <a href="/api/cv/download" class="btn btn-sm btn-outline-success">Descargar</a>
                    </div>
                `;
            } else {
                cvStatusEl.innerHTML = `
                    <div class="alert alert-warning py-2 mb-3">
                        <i class="bi bi-exclamation-triangle me-2"></i> No se ha detectado archivo de CV en la ruta predeterminada.
                    </div>
                `;
            }
        }
    } catch (e) {
        console.error("Error loading profile:", e);
    }
}

async function saveProfile() {
    const name = document.getElementById("profName")?.value || "";
    const phone = document.getElementById("profPhone")?.value || "";
    const email = document.getElementById("profEmail")?.value || "";

    try {
        const res = await fetch("/api/profile", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, phone, email })
        });
        const data = await res.json();
        if (data.success) {
            showToast("Perfil y datos de contacto guardados.");
            loadProfile();
        } else {
            showToast(data.error || "Error al guardar perfil", "error");
        }
    } catch (e) {
        showToast("Error al conectar con el servidor", "error");
    }
}

async function uploadCvFile() {
    const fileInput = document.getElementById("cvFileInput");
    if (!fileInput || !fileInput.files.length) {
        showToast("Por favor selecciona un archivo PDF o DOCX", "error");
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    showSpinner("Subiendo archivo de CV...");
    try {
        const res = await fetch("/api/cv/upload", {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        hideSpinner();

        if (data.success) {
            showToast(`¡CV '${data.filename}' cargado correctamente! (${data.size_kb} KB)`);
            loadProfile();
        } else {
            showToast(data.error || "Error al subir archivo", "error");
        }
    } catch (e) {
        hideSpinner();
        showToast("Error al conectar con el servidor", "error");
    }
}

function copyToClipboard(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;
    navigator.clipboard.writeText(el.value).then(() => {
        showToast("¡Texto copiado al portapapeles! Listo para enviar por WhatsApp.");
    }).catch(() => {
        showToast("No se pudo copiar automáticamente", "error");
    });
}


// -------------------------------------------------------------
// SETTINGS & EXPORTS
// -------------------------------------------------------------
async function loadSettings() {
    try {
        const res = await fetch("/api/settings");
        const data = await res.json();
        if (!data.success) return;

        const s = data.settings;
        if (document.getElementById("setWaProvider")) document.getElementById("setWaProvider").value = s.whatsapp_provider || "greenapi";
        if (document.getElementById("setWaPhone")) document.getElementById("setWaPhone").value = s.user_whatsapp_phone || "";
        if (document.getElementById("setGreenId")) document.getElementById("setGreenId").value = s.greenapi_instance_id || "";
        if (document.getElementById("setMetaPid")) document.getElementById("setMetaPid").value = s.meta_phone_number_id || "";

        const kwJsonEl = document.getElementById("keywordsJsonView");
        if (kwJsonEl) {
            kwJsonEl.textContent = JSON.stringify(data.keywords || {}, null, 2);
        }
    } catch (e) {
        console.error("Error loading settings:", e);
    }
}

async function saveSettings() {
    const provider = document.getElementById("setWaProvider")?.value || "greenapi";
    const phone = document.getElementById("setWaPhone")?.value || "";
    const greenId = document.getElementById("setGreenId")?.value || "";
    const greenToken = document.getElementById("setGreenToken")?.value || "";
    const metaPid = document.getElementById("setMetaPid")?.value || "";
    const metaToken = document.getElementById("setMetaToken")?.value || "";

    const payload = {
        whatsapp_provider: provider,
        user_whatsapp_phone: phone,
        greenapi_instance_id: greenId,
        meta_phone_number_id: metaPid
    };
    if (greenToken.trim()) payload.greenapi_api_token = greenToken.trim();
    if (metaToken.trim()) payload.meta_access_token = metaToken.trim();

    try {
        const res = await fetch("/api/settings", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            showToast("Configuraciones de WhatsApp Bot y .env guardadas.");
        } else {
            showToast(data.error || "Error al guardar", "error");
        }
    } catch (e) {
        showToast("Error de conexión al servidor", "error");
    }
}


// -------------------------------------------------------------
// EVENT LISTENERS & HELPERS
// -------------------------------------------------------------
function setupEventListeners() {
    // Filter form
    const filterForm = document.getElementById("jobFilterForm");
    if (filterForm) {
        filterForm.addEventListener("submit", (e) => {
            e.preventDefault();
            loadJobs();
        });
    }

    const resetFilterBtn = document.getElementById("btnResetFilters");
    if (resetFilterBtn) {
        resetFilterBtn.addEventListener("click", () => {
            if (document.getElementById("filterSearch")) document.getElementById("filterSearch").value = "";
            if (document.getElementById("filterCity")) document.getElementById("filterCity").value = "";
            if (document.getElementById("filterCategory")) document.getElementById("filterCategory").value = "Todas";
            if (document.getElementById("filterSource")) document.getElementById("filterSource").value = "Todas";
            if (document.getElementById("filterModality")) document.getElementById("filterModality").value = "Todas";
            if (document.getElementById("filterPhoneOnly")) document.getElementById("filterPhoneOnly").checked = false;
            selectQuickFilter('Todos');
        });
    }

    // WhatsApp command form
    const waForm = document.getElementById("waCommandForm");
    if (waForm) {
        waForm.addEventListener("submit", (e) => {
            e.preventDefault();
            sendWhatsAppCommand();
        });
    }
}

function escapeHtml(str) {
    if (!str) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
