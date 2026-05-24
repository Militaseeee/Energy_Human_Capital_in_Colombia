"""
app.py — Dashboard Oscuro · Coevolución STEM ⚡ Colombia 2023
─────────────────────────────────────────────────────────────────────────────
Autores : Camila Acosta & Cristian Robledo  |  Talento Tech  |  Mayo 2026
─────────────────────────────────────────────────────────────────────────────
"""

import streamlit as st

# ── set_page_config SIEMPRE primero ──────────────────────────────────────────
st.set_page_config(
    page_title="Coevolución STEM ⚡ Colombia",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Importaciones internas ───────────────────────────────────────────────────
from queries.analytics import (
    get_coevolucion_nacional,
    get_distribucion_regional,
    get_mapa_colombia,
    get_top_areas_conocimiento,
    get_modelo_estadistico,
)
from utils.charts import (
    C,
    REGION_COLORS,
    chart_coevolucion,
    chart_distribucion_regional,
    chart_mapa_hero,
    chart_mapa_colombia,
    chart_top_areas,
    chart_regresion,
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS GLOBAL — tema oscuro + tipografía
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"], [class*="st-"], button, input, select, textarea {
    font-family: 'Plus Jakarta Sans', 'Segoe UI', system-ui, sans-serif !important;
}

/* Fondo general */
[data-testid="stAppViewContainer"] { background: #020817 !important; }
[data-testid="stHeader"]           { background: transparent !important; }
[data-testid="stSidebar"]          { background: #0F172A !important; }
.main .block-container {
    padding-top: 1rem;
    padding-bottom: 2.5rem;
    max-width: 1300px;
}

/* Pestañas */
.stTabs [data-baseweb="tab-list"] {
    background: #0F172A;
    border-radius: 14px;
    padding: 5px;
    gap: 4px;
    border: 1px solid #1E293B;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    padding: 0.5rem 1.3rem !important;
    color: #94A3B8 !important;
    background: transparent !important;
    transition: all 0.25s ease !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #0EA5E9, #22D3EE) !important;
    color: #020817 !important;
    font-weight: 700 !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding-top: 1.8rem;
}

/* Expanders */
[data-testid="stExpander"] {
    background: #0F172A !important;
    border: 1px solid #1E293B !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    color: #94A3B8 !important;
    font-size: 0.85rem !important;
}

/* DataFrames */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* Radio y selectbox */
[data-testid="stRadio"] label, [data-testid="stSelectbox"] label {
    color: #94A3B8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

/* Spinner */
[data-testid="stSpinner"] { color: #22D3EE !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0F172A; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }

/* Ocultar elementos de UI innecesarios */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIONES HELPER — HTML sin indentación profunda (evita bloque de código)
# ─────────────────────────────────────────────────────────────────────────────

def _badge_kpi(icon: str, value: str, label: str, color: str) -> str:
    """Tarjeta KPI compacta para el hero section. HTML en una sola línea."""
    return (
        f'<div style="background:#0F172A;border-radius:12px;padding:1rem 1.2rem;'
        f'border-left:3px solid {color};margin-bottom:0.75rem">'
        f'<div style="font-size:1.5rem;font-weight:900;color:{color};line-height:1">{value}</div>'
        f'<div style="font-size:0.72rem;color:#64748B;text-transform:uppercase;'
        f'letter-spacing:0.07em;margin-top:0.25rem">{icon} {label}</div>'
        f'</div>'
    )


def _card_metrica(icon: str, value: str, label: str, sublabel: str, color: str) -> str:
    """Tarjeta métrica Tab 1. HTML en una sola línea."""
    return (
        f'<div style="background:#0F172A;border-radius:16px;padding:1.4rem 1rem;'
        f'border-top:4px solid {color};box-shadow:0 4px 20px rgba(0,0,0,0.4);text-align:center">'
        f'<div style="font-size:2rem;margin-bottom:0.35rem">{icon}</div>'
        f'<div style="font-size:1.8rem;font-weight:800;color:{color};line-height:1.1">{value}</div>'
        f'<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:0.07em;color:#F1F5F9;margin-top:0.5rem">{label}</div>'
        f'<div style="font-size:0.7rem;color:#64748B;margin-top:0.15rem">{sublabel}</div>'
        f'</div>'
    )


def _kpi_card(icon: str, label: str, value: str, sublabel: str, color: str) -> str:
    """Tarjeta KPI Tab 3. HTML de una línea para evitar bloque Markdown."""
    return (
        f'<div style="background:#0F172A;border-radius:14px;padding:1.5rem 1rem;'
        f'border-top:4px solid {color};box-shadow:0 4px 20px rgba(0,0,0,0.4);text-align:center">'
        f'<div style="font-size:1.8rem">{icon}</div>'
        f'<div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:0.09em;color:#64748B;margin-top:0.4rem">{label}</div>'
        f'<div style="font-size:1.9rem;font-weight:900;color:{color};'
        f'line-height:1.1;margin-top:0.25rem">{value}</div>'
        f'<div style="font-size:0.68rem;color:#475569;margin-top:0.25rem">{sublabel}</div>'
        f'</div>'
    )


def _alert(titulo: str, cuerpo: str) -> str:
    return (
        '<div style="background:#1a0a0a;border:1px solid #7F1D1D;border-left:5px solid #F87171;'
        'border-radius:14px;padding:1.2rem 1.5rem;margin:0.8rem 0">'
        f'<div style="font-weight:700;color:#FCA5A5;font-size:0.93rem;margin-bottom:0.4rem">🚨 {titulo}</div>'
        f'<div style="color:#FCA5A5;font-size:0.85rem;line-height:1.65;opacity:0.85">{cuerpo}</div>'
        '</div>'
    )


def _insight(titulo: str, cuerpo: str) -> str:
    return (
        '<div style="background:#051a0f;border:1px solid #166534;border-left:5px solid #4ADE80;'
        'border-radius:14px;padding:1.2rem 1.5rem;margin:0.8rem 0">'
        f'<div style="font-weight:700;color:#86EFAC;font-size:0.93rem;margin-bottom:0.4rem">💡 {titulo}</div>'
        f'<div style="color:#86EFAC;font-size:0.85rem;line-height:1.65;opacity:0.85">{cuerpo}</div>'
        '</div>'
    )


def _divider() -> None:
    st.markdown(
        '<hr style="border:none;border-top:1px solid #1E293B;margin:1.2rem 0">',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# CARGA DE DATOS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=600, show_spinner=False)
def _cargar_todo():
    return (
        get_coevolucion_nacional(),
        get_distribucion_regional(1),
        get_distribucion_regional(2),
        get_mapa_colombia(),
        get_top_areas_conocimiento(),
        get_modelo_estadistico(),
    )


with st.spinner("Conectando con Supabase…"):
    try:
        df_coev, df_s1, df_s2, df_mapa, df_top, modelo = _cargar_todo()
        st.toast("Datos listos ✓", icon="⚡")
    except Exception as exc:
        st.error(
            f"**No se pudo conectar con Supabase.**\n\n"
            f"Verifica `.streamlit/secrets.toml`\n\n`{exc}`"
        )
        st.stop()


# ─────────────────────────────────────────────────────────────────────────────
# ██████████████  HERO SECTION  ██████████████
# Título grande + mapa de Colombia lado a lado
# ─────────────────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:
    # ── Marca / etiqueta superior ─────────────────────────────────────────
    st.markdown(
        '<div style="display:inline-block;background:#0F172A;border:1px solid #1E293B;'
        'border-radius:20px;padding:0.35rem 1rem;font-size:0.72rem;font-weight:700;'
        'text-transform:uppercase;letter-spacing:0.12em;color:#22D3EE;margin-bottom:1rem">'
        '🇨🇴 Colombia &nbsp;·&nbsp; Minería de Datos &nbsp;·&nbsp; 2023'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Título principal grande ───────────────────────────────────────────
    st.markdown(
        '<h1 style="font-size:2.6rem;font-weight:900;line-height:1.15;color:#F1F5F9;margin:0 0 0.8rem 0">'
        '⚡ Coevolución del<br>'
        '<span style="color:#22D3EE">Capital Humano STEM</span><br>'
        'y el Sector Energético'
        '</h1>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p style="color:#64748B;font-size:0.9rem;line-height:1.6;margin-bottom:1.8rem">'
        'Análisis multifuente de la sincronía entre la formación universitaria STEM '
        'y la absorción laboral en el sector eléctrico colombiano.<br>'
        '<span style="color:#475569;font-size:0.8rem">'
        'SNIES &nbsp;·&nbsp; XM S.A. E.S.P. &nbsp;·&nbsp; DANE–GEIH &nbsp;·&nbsp; Banco Mundial'
        '</span></p>',
        unsafe_allow_html=True,
    )

    # ── 4 KPI badges — extraídos del semestre 1 ───────────────────────────
    if not df_coev.empty:
        f = df_coev.iloc[0]
        ka, kb = st.columns(2)
        with ka:
            st.markdown(_badge_kpi("🎓", f"{int(f['total_talento_stem']):,}", "Talento STEM", C["blue"]), unsafe_allow_html=True)
            st.markdown(_badge_kpi("⚡", f"{float(f['empleo_energia_miles']):.1f} K", "Empleo Energía", C["gold"]), unsafe_allow_html=True)
        with kb:
            st.markdown(_badge_kpi("🌿", f"{float(f['porcentaje_energia_limpia']):.1f}%", "Energía Limpia", C["green"]), unsafe_allow_html=True)
            st.markdown(_badge_kpi("🔗", "r = 1.0000", "Correlación Pearson", C["teal"]), unsafe_allow_html=True)

    # ── Créditos ──────────────────────────────────────────────────────────
    st.markdown(
        '<div style="margin-top:1.4rem;padding-top:1.2rem;border-top:1px solid #1E293B">'
        '<span style="color:#475569;font-size:0.78rem">'
        '👩‍💻 <b style="color:#94A3B8">Camila Acosta &amp; Cristian Robledo</b>'
        ' &nbsp;·&nbsp; 🏫 <b style="color:#94A3B8">Talento Tech</b>'
        ' &nbsp;·&nbsp; Mayo 2026'
        '</span></div>',
        unsafe_allow_html=True,
    )

with col_right:
    # ── Colombia map como hero visual ─────────────────────────────────────
    fig_hero = chart_mapa_hero(df_mapa)
    if fig_hero is not None:
        st.plotly_chart(fig_hero, use_container_width=True)
    else:
        st.markdown(
            '<div style="background:#0F172A;border:1px dashed #334155;border-radius:16px;'
            'padding:3rem;text-align:center;color:#475569">'
            '🗺️ Mapa no disponible sin conexión a internet</div>',
            unsafe_allow_html=True,
        )

# Separador visual entre hero y tabs
st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
st.markdown(
    '<div style="height:3px;background:linear-gradient(to right,#1E293B,#22D3EE,#60A5FA,#1E293B);'
    'border-radius:2px;margin-bottom:1.5rem"></div>',
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# PESTAÑAS DE ANÁLISIS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "📊  Coevolución Nacional",
    "🗺️  Brechas Regionales",
    "🧮  Modelo Estadístico",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — BALANCE DE COEVOLUCIÓN NACIONAL
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown(
        '<h3 style="font-size:1.1rem;font-weight:700;color:#F1F5F9;margin-bottom:0.2rem">'
        '📊 Indicadores por Semestre — Colombia 2023</h3>'
        '<p style="font-size:0.82rem;color:#64748B;margin-top:0">'
        'SNIES · XM S.A. E.S.P. · DANE–GEIH — cruzados por periodo académico.</p>',
        unsafe_allow_html=True,
    )

    sem = st.radio("Periodo:", [1, 2], format_func=lambda x: f"Semestre {x} · 2023",
                   horizontal=True, key="t1_sem")

    idx  = min(sem - 1, len(df_coev) - 1)
    fila = df_coev.iloc[idx] if not df_coev.empty else None

    _divider()

    # ── 4 métricas ────────────────────────────────────────────────────────
    if fila is not None:
        mc1, mc2, mc3, mc4 = st.columns(4, gap="medium")
        for col, ico, val, lbl, sub, color in [
            (mc1, "🌿", f"{float(fila['porcentaje_energia_limpia']):.1f}%",
             "Energía Limpia",      "Generación renovable",        C["green"]),
            (mc2, "🎓", f"{int(fila['total_talento_stem']):,}",
             "Talento STEM",        "Matrículas universitarias",   C["blue"]),
            (mc3, "⚡", f"{float(fila['empleo_energia_miles']):.1f} K",
             "Empleo en Energía",   "Miles de trabajadores",       C["gold"]),
            (mc4, "📉", f"{float(fila['tasa_desempleo_pais']):.1f}%",
             "Tasa de Desempleo",   "Total nacional · DANE",       C["red"]),
        ]:
            with col:
                st.markdown(_card_metrica(ico, val, lbl, sub, color), unsafe_allow_html=True)
    else:
        st.warning("Sin datos para el semestre seleccionado.")

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

    # ── Gráfico de coevolución ─────────────────────────────────────────────
    if not df_coev.empty:
        st.plotly_chart(chart_coevolucion(df_coev), use_container_width=True)

    # ── Insight ───────────────────────────────────────────────────────────
    st.markdown(_insight(
        "¿Qué nos dice el gráfico?",
        "La línea azul (talento STEM) y la línea ámbar (empleo energético) crecen "
        "en perfecta sincronía durante ambos semestres. El modelo OLS cuantifica "
        "esta coevolución con <b>r = 1.0000</b> y <b>R² = 1.0000</b> — ver pestaña Modelo.",
    ), unsafe_allow_html=True)

    # ── Tabla ─────────────────────────────────────────────────────────────
    with st.expander("🔍 Tabla de datos completa (2023)"):
        st.dataframe(
            df_coev.rename(columns={
                "year": "Año", "semester": "Semestre",
                "porcentaje_energia_limpia": "% Energía Limpia",
                "total_talento_stem": "Talento STEM",
                "empleo_energia_miles": "Empleo Energía (K)",
                "tasa_desempleo_pais": "Tasa Desempleo %",
            }),
            use_container_width=True, hide_index=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — DISTRIBUCIÓN Y BRECHAS REGIONALES
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown(
        '<h3 style="font-size:1.1rem;font-weight:700;color:#F1F5F9;margin-bottom:0.2rem">'
        '🗺️ Radiografía Geográfica del Talento STEM — 2023</h3>'
        '<p style="font-size:0.82rem;color:#64748B;margin-top:0">'
        '¿Dónde se forma el capital humano? ¿Coincide con las zonas de mayor potencial energético?</p>',
        unsafe_allow_html=True,
    )

    # ── Alerta ────────────────────────────────────────────────────────────
    st.markdown(_alert(
        "Brecha Territorial Crítica Detectada",
        "La <b>Región Andina concentra el 68.54%</b> del talento STEM nacional, mientras "
        "la <b>Región Caribe apenas alcanza el 16.47%</b>. Los parques eólicos de La Guajira "
        "y las granjas solares de Cesar se construyen donde <i>menos</i> talento técnico existe.",
    ), unsafe_allow_html=True)

    # ── Selector ──────────────────────────────────────────────────────────
    sem_reg = st.selectbox("📅 Semestre:", [1, 2],
                           format_func=lambda x: f"2023 — Semestre {x}", key="t2_sem")
    df_reg  = df_s1 if sem_reg == 1 else df_s2

    _divider()

    # ── Mapa coroplético de Colombia ──────────────────────────────────────
    fig_mapa_tab2 = chart_mapa_colombia(df_mapa, height=580, show_title=True)
    if fig_mapa_tab2 is not None:
        st.plotly_chart(fig_mapa_tab2, use_container_width=True)
    else:
        st.info("⚠️ Sin conexión — mostrando distribución alternativa.")

    _divider()

    # ── Segunda fila: dona + detalle ──────────────────────────────────────
    col_dona, col_det = st.columns([5, 4], gap="large")

    with col_dona:
        st.markdown(
            '<p style="font-size:0.83rem;font-weight:600;color:#94A3B8;margin-bottom:0.3rem">'
            'Participación % por Macro-Región</p>',
            unsafe_allow_html=True,
        )
        if not df_reg.empty:
            st.plotly_chart(chart_distribucion_regional(df_reg), use_container_width=True)

    with col_det:
        st.markdown(
            '<p style="font-size:0.83rem;font-weight:600;color:#94A3B8;margin-bottom:0.6rem">'
            '🔎 Detalle por Región</p>',
            unsafe_allow_html=True,
        )
        if not df_reg.empty:
            reg_sel = st.selectbox(
                "Región:", df_reg["macro_region"].dropna().unique().tolist(), key="t2_reg"
            )
            fila_r  = df_reg[df_reg["macro_region"] == reg_sel].iloc[0]
            color_r = REGION_COLORS.get(reg_sel, C["teal"])

            st.markdown(
                f'<div style="background:#0F172A;border-radius:14px;padding:1.4rem;'
                f'border-left:5px solid {color_r};box-shadow:0 4px 20px rgba(0,0,0,0.4);margin-top:0.5rem">'
                f'<div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;'
                f'letter-spacing:0.09em;color:#475569">Macro-Región</div>'
                f'<div style="font-size:1.1rem;font-weight:800;color:{color_r};margin:0.2rem 0 1rem 0">'
                f'{reg_sel}</div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem">'
                f'<div style="background:#1E293B;border-radius:10px;padding:0.8rem;text-align:center">'
                f'<div style="font-size:1.5rem;font-weight:800;color:#F1F5F9">'
                f'{int(fila_r["cantidad_departamentos"])}</div>'
                f'<div style="font-size:0.68rem;color:#64748B;text-transform:uppercase;font-weight:600">'
                f'Departamentos</div></div>'
                f'<div style="background:#1E293B;border-radius:10px;padding:0.8rem;text-align:center">'
                f'<div style="font-size:1.5rem;font-weight:800;color:{color_r}">'
                f'{float(fila_r["porcentaje_participacion_talento"]):.1f}%</div>'
                f'<div style="font-size:0.68rem;color:#64748B;text-transform:uppercase;font-weight:600">'
                f'Participación</div></div></div>'
                f'<div style="margin-top:0.9rem;font-size:0.85rem;color:#94A3B8;font-weight:600">'
                f'🎓 {int(fila_r["estudiantes_matriculados"]):,} estudiantes STEM</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Contexto por región
            contextos = {
                "Andina":    ("insight", "Epicentro del talento.",
                              "Alta densidad de IES y programas STEM. Requiere estrategias de movilidad hacia las zonas de demanda energética."),
                "Caribe":    ("alert",   "Brecha estructural urgente.",
                              "Alta demanda eólica y solar, pero baja oferta local de ingenieros. Prioridad de política pública en formación técnica."),
                "Pacífica":  ("insight", "Potencial hídrico elevado.",
                              "Déficit de ingeniería eléctrica y ambiental para aprovechar los recursos del litoral pacífico."),
                "Orinoquía": ("insight", "Llanura en expansión.",
                              "Región en crecimiento energético con baja densidad de formación STEM. Oportunidad de extensión universitaria."),
                "Amazonía":  ("insight", "Datos en consolidación.",
                              "Proyección de política pública en etapa temprana. Énfasis en sostenibilidad y energía renovable aislada."),
                "Insular":   ("insight", "Archipiélago estratégico.",
                              "Alta dependencia de generación diésel; potencial solar y eólico sin explotar. Ideal para proyectos piloto."),
            }
            st.markdown('<div style="height:0.6rem"></div>', unsafe_allow_html=True)
            for key, (tipo, titulo, cuerpo) in contextos.items():
                if key in reg_sel:
                    fn = _insight if tipo == "insight" else _alert
                    st.markdown(fn(titulo, cuerpo), unsafe_allow_html=True)
                    break

    with st.expander("📊 Tabla regional completa"):
        st.dataframe(
            df_reg.rename(columns={
                "macro_region": "Macro-Región",
                "cantidad_departamentos": "Departamentos",
                "estudiantes_matriculados": "Estudiantes STEM",
                "porcentaje_participacion_talento": "Participación %",
            }),
            use_container_width=True, hide_index=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — MODELO MATEMÁTICO Y COMPETENCIAS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown(
        '<h3 style="font-size:1.1rem;font-weight:700;color:#F1F5F9;margin-bottom:0.2rem">'
        '🧮 Modelo Estadístico Relacional — Pearson + OLS</h3>'
        '<p style="font-size:0.82rem;color:#64748B;margin-top:0">'
        'Resultados de la Fase de Modelado: cruce STEM × Empleo Energético · 2023.</p>',
        unsafe_allow_html=True,
    )

    _divider()

    # ── 4 KPI cards del modelo — usando st.columns para evitar el bug ──────
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    for col, ico, lbl, val, sub, color in [
        (k1, "🔗", "r — Pearson",    f"{modelo['r']:.4f}",         "Coevolución perfecta",        C["teal"]),
        (k2, "📈", "R² — OLS",       f"{modelo['r2']:.4f}",        "Ajuste del modelo",            C["green"]),
        (k3, "📐", "m — Pendiente",  f"{modelo['slope']:.6f}",     "↑10K est. → +10.41K emp.",    C["gold"]),
        (k4, "📍", "b — Intercepto", f"{modelo['intercept']:.2f}", "Base del modelo",              C["purple"]),
    ]:
        with col:
            st.markdown(_kpi_card(ico, lbl, val, sub, color), unsafe_allow_html=True)

    _divider()

    # ── Ecuación + Interpretación ─────────────────────────────────────────
    col_eq, col_int = st.columns([1, 1], gap="large")

    with col_eq:
        st.markdown(
            '<div style="background:#0F172A;border:1px solid #1E293B;border-radius:16px;'
            'padding:1.8rem;text-align:center">'
            '<div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:0.12em;color:#22D3EE;margin-bottom:0.8rem">📐 Ecuación OLS</div>',
            unsafe_allow_html=True,
        )
        st.latex(rf"Y = {modelo['slope']:.6f} \cdot X + ({modelo['intercept']:.2f})")
        st.markdown(
            '<div style="font-size:0.78rem;color:#475569;margin-top:0.6rem;line-height:1.5">'
            '<b style="color:#64748B">X</b> = Estudiantes STEM matriculados<br>'
            '<b style="color:#64748B">Y</b> = Empleo Sector Energía (miles)'
            '</div></div>',
            unsafe_allow_html=True,
        )

    with col_int:
        inc_10k = modelo["slope"] * 10_000
        st.markdown(_insight(
            "Interpretación Ejecutiva",
            f"Por cada incremento de <b>10,000 estudiantes</b> en programas STEM, "
            f"el ecosistema colombiano absorbe <b>{inc_10k:.2f} mil empleos formales</b> "
            f"en el sector de electricidad, gas y agua.",
        ), unsafe_allow_html=True)

        st.markdown(_alert(
            "Nota de Evaluación Científica",
            "R² = 1.0000 es esperado con dos puntos de muestra (S1 y S2 del 2023). "
            "El modelo es un <b>descriptor exacto</b> del año. Para tendencia predictiva "
            "se recomienda incorporar la serie 2018–2023.",
        ), unsafe_allow_html=True)

    _divider()

    # ── Gráficos: OLS + Top 10 ─────────────────────────────────────────────
    col_ols, col_top = st.columns([1, 1], gap="large")

    with col_ols:
        st.markdown('<p style="font-size:0.85rem;font-weight:600;color:#94A3B8;margin-bottom:0.3rem">📉 Recta de Regresión OLS</p>', unsafe_allow_html=True)
        df_mod = modelo["df"]
        if not df_mod.empty:
            st.plotly_chart(chart_regresion(df_mod, modelo["slope"], modelo["intercept"]),
                            use_container_width=True)

    with col_top:
        st.markdown('<p style="font-size:0.85rem;font-weight:600;color:#94A3B8;margin-bottom:0.3rem">🏆 Top 10 Áreas de Conocimiento STEM</p>', unsafe_allow_html=True)
        if not df_top.empty:
            st.plotly_chart(chart_top_areas(df_top), use_container_width=True)

    # ── Tablas ────────────────────────────────────────────────────────────
    ta, tb = st.columns(2)
    with ta:
        with st.expander("🔍 Datos fuente del modelo"):
            if not df_mod.empty:
                st.dataframe(df_mod.rename(columns={
                    "semester": "Semestre", "talento_stem": "Estudiantes STEM",
                    "empleo_energia": "Empleo Energía (K)",
                }), use_container_width=True, hide_index=True)
    with tb:
        with st.expander("🔍 Tabla Top 10 Áreas"):
            if not df_top.empty:
                st.dataframe(df_top.rename(columns={
                    "area_conocimiento": "Área de Conocimiento",
                    "total_estudiantes": "Total Estudiantes",
                    "ranking_nacional": "Ranking",
                }), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="margin-top:2.5rem;background:#0F172A;border:1px solid #1E293B;'
    'border-radius:14px;padding:1.1rem 2rem;text-align:center;'
    'font-size:0.78rem;color:#475569">'
    '⚡ <b style="color:#64748B">Coevolución STEM–Energía · Colombia 2023</b>'
    ' &nbsp;|&nbsp; 👩‍💻 <b style="color:#64748B">Camila Acosta &amp; Cristian Robledo</b>'
    ' &nbsp;|&nbsp; 🏫 <b style="color:#64748B">Talento Tech</b>'
    ' &nbsp;|&nbsp; Datos: SNIES · XM · DANE–GEIH · Banco Mundial · Mayo 2026'
    '</div>',
    unsafe_allow_html=True,
)
