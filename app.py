"""
app.py — Dashboard Ejecutivo · Coevolución STEM ⚡ Colombia 2023
─────────────────────────────────────────────────────────────────────────────
Autores : Camila Acosta & Cristian Robledo  |  Talento Tech  |  Mayo 2026
─────────────────────────────────────────────────────────────────────────────
Estructura visual:
  1. Banner + título
  2. 4 métricas ejecutivas (st.metric con deltas reales S1→S2)
  3. Hero: mapa de Colombia (izq) + descripción del proyecto (der)
  4. Pestañas: Coevolución · Brechas Regionales · Modelo Estadístico
─────────────────────────────────────────────────────────────────────────────
"""

import streamlit as st

# ── set_page_config SIEMPRE primero ──────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Coevolución Capital Humano & Energía ⚡",
    page_icon="⚡",
    initial_sidebar_state="collapsed",
)

# ── Importaciones internas ───────────────────────────────────────────────────
from queries.analytics import (
    get_coevolucion_nacional,
    get_distribucion_regional,
    get_mapa_colombia,
    get_top_areas_conocimiento,
    get_modelo_estadistico,
    get_resource_types_diagnostico,
)
from utils.charts import (
    C, REGION_COLORS,
    chart_coevolucion,
    chart_distribucion_regional,
    chart_mapa_hero,
    chart_mapa_colombia,
    chart_top_areas,
    chart_regresion,
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

html, body, h1, h2, h3, h4, h5, h6,
p, button, input, select, textarea,
.stApp, .main,
[data-testid="stMarkdownContainer"] *,
[data-testid="stText"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"] *,
[data-testid="stMetricDelta"] * {
    font-family: 'Plus Jakarta Sans', 'Segoe UI', system-ui, sans-serif !important;
}

/* ── Fondos ── */
[data-testid="stAppViewContainer"] { background: #020817 !important; }
[data-testid="stHeader"]           { background: transparent !important; }
.main .block-container { padding-top: 0.8rem; padding-bottom: 2.5rem; max-width: 1300px; }

/* ── st.metric — tarjetas compactas para grid 2×2 ── */
div[data-testid="metric-container"] {
    background: #0F172A;
    border-radius: 13px;
    padding: 0.85rem 0.75rem !important;
    border: 1px solid #1E293B;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
    text-align: center;
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
}
div[data-testid="metric-container"]:hover {
    border-color: #334155;
    box-shadow: 0 6px 28px rgba(0,0,0,0.5);
}
div[data-testid="stMetricValue"] > div {
    font-size: 1.5rem !important;
    font-weight: 900 !important;
    color: #F1F5F9 !important;
    letter-spacing: -0.02em;
}
div[data-testid="stMetricLabel"] > div {
    font-size: 0.66rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #64748B !important;
}
div[data-testid="stMetricDelta"] > div {
    font-size: 0.71rem !important;
    font-weight: 600 !important;
}

/* ── Pestañas ── */
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

/* ── Expanders ── */
[data-testid="stExpander"] {
    background: #0F172A !important;
    border: 1px solid #1E293B !important;
    border-radius: 12px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0F172A; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }

/* ── Ocultar UI de Streamlit ── */
#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HTML HELPERS — una sola línea por función (evita el bug de 4 espacios markdown)
# ─────────────────────────────────────────────────────────────────────────────
def _divider(color: str = "#1E293B") -> None:
    st.markdown(f'<hr style="border:none;border-top:1px solid {color};margin:1rem 0">', unsafe_allow_html=True)

def _gradient_divider() -> None:
    st.markdown('<div style="height:3px;background:linear-gradient(to right,#1E293B,#22D3EE,#60A5FA,#1E293B);border-radius:2px;margin:1.2rem 0"></div>', unsafe_allow_html=True)

def _alert(titulo: str, cuerpo: str) -> str:
    return (
        '<div style="background:#1a0a0a;border:1px solid #7F1D1D;border-left:5px solid #F87171;'
        'border-radius:14px;padding:1.2rem 1.5rem;margin:0.8rem 0">'
        f'<div style="font-weight:700;color:#FCA5A5;font-size:0.93rem;margin-bottom:0.35rem">🚨 {titulo}</div>'
        f'<div style="color:#FCA5A5;font-size:0.85rem;line-height:1.65;opacity:0.85">{cuerpo}</div>'
        '</div>'
    )

def _insight(titulo: str, cuerpo: str) -> str:
    return (
        '<div style="background:#051a0f;border:1px solid #166534;border-left:5px solid #4ADE80;'
        'border-radius:14px;padding:1.2rem 1.5rem;margin:0.8rem 0">'
        f'<div style="font-weight:700;color:#86EFAC;font-size:0.93rem;margin-bottom:0.35rem">💡 {titulo}</div>'
        f'<div style="color:#86EFAC;font-size:0.85rem;line-height:1.65;opacity:0.85">{cuerpo}</div>'
        '</div>'
    )

def _card_metrica(icon: str, value: str, label: str, sublabel: str, color: str) -> str:
    return (
        f'<div style="background:#0F172A;border-radius:16px;padding:1.4rem 1rem;'
        f'border-top:4px solid {color};box-shadow:0 4px 20px rgba(0,0,0,0.4);text-align:center">'
        f'<div style="font-size:2rem;margin-bottom:0.3rem">{icon}</div>'
        f'<div style="font-size:1.8rem;font-weight:800;color:{color};line-height:1.1">{value}</div>'
        f'<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:0.07em;color:#F1F5F9;margin-top:0.5rem">{label}</div>'
        f'<div style="font-size:0.7rem;color:#64748B;margin-top:0.12rem">{sublabel}</div>'
        f'</div>'
    )

def _kpi_card(icon: str, label: str, value: str, sublabel: str, color: str) -> str:
    return (
        f'<div style="background:#0F172A;border-radius:14px;padding:1.5rem 1rem;'
        f'border-top:4px solid {color};box-shadow:0 4px 20px rgba(0,0,0,0.4);text-align:center">'
        f'<div style="font-size:1.8rem">{icon}</div>'
        f'<div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:0.09em;color:#64748B;margin-top:0.4rem">{label}</div>'
        f'<div style="font-size:1.9rem;font-weight:900;color:{color};line-height:1.1;margin-top:0.2rem">{value}</div>'
        f'<div style="font-size:0.68rem;color:#475569;margin-top:0.22rem">{sublabel}</div>'
        f'</div>'
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
        st.toast("Datos cargados ✓", icon="⚡")
    except Exception as exc:
        st.error(f"**No se pudo conectar con Supabase.**\n\n`{exc}`")
        st.stop()

# Extraer filas por semestre
s1 = df_coev.iloc[0] if len(df_coev) > 0 else None
s2 = df_coev.iloc[1] if len(df_coev) > 1 else s1


# ═════════════════════════════════════════════════════════════════════════════
# HERO — Título + Leyenda (izq) · KPIs + Mapa + Alerta (der)
# ═════════════════════════════════════════════════════════════════════════════
col_left, col_right = st.columns([1, 1.5], gap="large")

with col_left:
    # ── Eyebrow + título con gradiente y halo difuminado ─────────────────────
    st.markdown(
        '<div style="background:radial-gradient(ellipse at 10% 50%,'
        'rgba(34,211,238,0.12) 0%,transparent 65%);'
        'padding:0.5rem 0 1rem 0">'
        '<div style="font-size:0.62rem;font-weight:700;text-transform:uppercase;'
        'letter-spacing:0.2em;color:#334155;margin-bottom:0.75rem">'
        '🇨🇴 &nbsp;Minería de Datos &nbsp;·&nbsp; Colombia 2023</div>'
        '<h1 style="font-size:2.75rem;font-weight:900;line-height:1.1;'
        'letter-spacing:-0.03em;margin:0 0 0.75rem 0;'
        'background:linear-gradient(140deg,#FFFFFF 0%,#E2E8F0 22%,'
        '#22D3EE 62%,#60A5FA 100%);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'background-clip:text">'
        'Coevolución del Capital Humano STEM y el Sector Energético</h1>'
        '<p style="color:#64748B;font-size:0.83rem;line-height:1.65;'
        'margin:0 0 0.3rem">'
        'Sincronía entre la formación universitaria STEM y la absorción '
        'laboral en el sector eléctrico colombiano.</p>'
        '<span style="font-size:0.67rem;color:#334155">'
        'SNIES &nbsp;·&nbsp; XM S.A. E.S.P. &nbsp;·&nbsp; '
        'DANE–GEIH &nbsp;·&nbsp; Banco Mundial</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Separador fino ────────────────────────────────────────────────────────
    st.markdown(
        '<div style="height:1px;background:linear-gradient(to right,'
        '#1E293B,#22D3EE44,#1E293B);margin:0.1rem 0 0.75rem"></div>',
        unsafe_allow_html=True,
    )

    # ── Leyenda de macro-regiones (lista vertical con glow) ──────────────────
    regiones_hero = [
        (REGION_COLORS["Región Andina"],    "Región Andina",    "68.54% del talento STEM"),
        (REGION_COLORS["Región Caribe"],    "Región Caribe",    "16.47% — brecha crítica"),
        (REGION_COLORS["Región Pacífica"],  "Región Pacífica",  "Potencial hídrico"),
        (REGION_COLORS["Región Orinoquía"], "Región Orinoquía", "Llanura en crecimiento"),
        (REGION_COLORS["Región Amazonía"],  "Región Amazonía",  "En consolidación"),
        (REGION_COLORS["Región Insular"],   "Región Insular",   "Potencial solar/eólico"),
    ]
    for clr, nombre, desc in regiones_hero:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:0.55rem;margin-bottom:0.42rem">'
            f'<div style="width:9px;height:9px;border-radius:50%;background:{clr};'
            f'box-shadow:0 0 8px {clr}88;flex-shrink:0"></div>'
            f'<span style="font-size:0.8rem;font-weight:700;color:#CBD5E1">{nombre}</span>'
            f'<span style="font-size:0.72rem;color:#475569"> — {desc}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

with col_right:
    # ── KPIs en una sola fila (4 columnas) ───────────────────────────────────
    kr1, kr2, kr3, kr4 = st.columns(4, gap="small")
    with kr1:
        val_stem = int(s1["total_talento_stem"]) if s1 is not None else 0
        delta_stem = (int(s2["total_talento_stem"]) - int(s1["total_talento_stem"])
                      if s2 is not None and s1 is not None else None)
        st.metric("🎓 Talento STEM", f"{val_stem:,}",
                  f"{delta_stem:+,} Sem. 2" if delta_stem is not None else "2023")
    with kr2:
        val_emp = float(s1["empleo_energia_miles"]) if s1 is not None else 0
        delta_emp = (float(s2["empleo_energia_miles"]) - float(s1["empleo_energia_miles"])
                     if s2 is not None and s1 is not None else None)
        st.metric("⚡ Empleo Energía", f"{val_emp:.1f} K",
                  f"{delta_emp:+.2f} K Sem. 2" if delta_emp is not None else "Miles")
    with kr3:
        val_enl = float(s1["porcentaje_energia_limpia"]) if s1 is not None else 0
        delta_enl = (float(s2["porcentaje_energia_limpia"]) - float(s1["porcentaje_energia_limpia"])
                     if s2 is not None and s1 is not None else None)
        st.metric("🌿 Energía Limpia", f"{val_enl:.2f}%",
                  f"{delta_enl:+.2f}% Sem. 2" if delta_enl is not None else "2023")
    with kr4:
        st.metric("🔗 Correlación r", f"{modelo['r']:.4f}",
                  "Sincronía Perfecta", delta_color="normal")

    # ── Mapa coroplético interactivo ──────────────────────────────────────────
    st.markdown('<div style="margin-top:0.35rem"></div>', unsafe_allow_html=True)
    fig_hero = chart_mapa_colombia(df_mapa, height=450, show_title=False)
    if fig_hero is not None:
        st.plotly_chart(fig_hero, use_container_width=True)
    else:
        st.markdown(
            '<div style="background:#0F172A;border:1px dashed #334155;'
            'border-radius:16px;padding:3rem;text-align:center;color:#475569">'
            '🗺️ Mapa no disponible sin conexión a internet</div>',
            unsafe_allow_html=True,
        )

    # ── Alerta debajo del mapa ────────────────────────────────────────────────
    st.markdown(
        '<div style="background:#1a0a0a;border-width:1px 1px 1px 4px;'
        'border-style:solid;border-color:#7F1D1D #7F1D1D #7F1D1D #F87171;'
        'border-radius:10px;padding:0.6rem 1rem;margin-top:0.1rem">'
        '<span style="font-weight:700;color:#FCA5A5;font-size:0.82rem">'
        '🚨 Brecha Territorial — </span>'
        '<span style="color:#FCA5A5;font-size:0.79rem">'
        'La <b>Región Andina</b> concentra el <b>68.54%</b> del talento '
        'mientras parques eólicos y solares se construyen en el '
        '<b>Caribe (16.47%)</b>.</span></div>',
        unsafe_allow_html=True,
    )

_gradient_divider()


# ═════════════════════════════════════════════════════════════════════════════
# ④ PESTAÑAS DE ANÁLISIS
# ═════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs([
    "📊  Coevolución Nacional",
    "🗺️  Brechas Regionales",
    "🧮  Modelo Estadístico",
])


# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 — COEVOLUCIÓN NACIONAL
# ──────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown(
        '<h3 style="font-size:1.1rem;font-weight:700;color:#F1F5F9;margin-bottom:0.15rem">'
        '📊 Balance de Coevolución — Colombia 2023</h3>'
        '<p style="font-size:0.82rem;color:#64748B;margin-top:0">'
        'Indicadores cruzados SNIES · XM · DANE por semestre académico.</p>',
        unsafe_allow_html=True,
    )

    sem = st.radio("Periodo:", [1, 2], format_func=lambda x: f"Semestre {x} · 2023",
                   horizontal=True, key="t1_sem")
    fila = df_coev.iloc[min(sem - 1, len(df_coev) - 1)] if not df_coev.empty else None

    _divider()

    if fila is not None:
        mc1, mc2, mc3, mc4 = st.columns(4, gap="medium")
        for col, ico, val, lbl, sub, color in [
            (mc1, "🌿", f"{float(fila['porcentaje_energia_limpia']):.2f}%",
             "Energía Limpia",    "Generación renovable",       C["green"]),
            (mc2, "🎓", f"{int(fila['total_talento_stem']):,}",
             "Talento STEM",      "Matrículas universitarias",  C["blue"]),
            (mc3, "⚡", f"{float(fila['empleo_energia_miles']):.2f} K",
             "Empleo en Energía", "Miles de trabajadores",      C["gold"]),
            (mc4, "📉", f"{float(fila['tasa_desempleo_pais']):.2f}%",
             "Tasa de Desempleo", "Total nacional · DANE",      C["red"]),
        ]:
            with col:
                st.markdown(_card_metrica(ico, val, lbl, sub, color), unsafe_allow_html=True)

    st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)

    if not df_coev.empty:
        st.plotly_chart(chart_coevolucion(df_coev), use_container_width=True)

    st.markdown(_insight(
        "¿Qué nos dice el gráfico?",
        "La línea azul (talento STEM) y la línea ámbar (empleo energético) crecen en "
        "perfecta sincronía. El modelo OLS cuantifica esta coevolución con "
        "<b>r = 1.0000</b> y <b>R² = 1.0000</b> — ver pestaña Modelo.",
    ), unsafe_allow_html=True)

    with st.expander("🔍 Ver tabla de datos completa"):
        st.dataframe(df_coev.rename(columns={
            "year": "Año", "semester": "Semestre",
            "porcentaje_energia_limpia": "% Energía Limpia",
            "total_talento_stem": "Talento STEM",
            "empleo_energia_miles": "Empleo Energía (K)",
            "tasa_desempleo_pais": "Tasa Desempleo %",
        }), use_container_width=True, hide_index=True)

    # ── Diagnóstico de tipos de energía ──────────────────────────────────────
    with st.expander("🔧 Diagnóstico: tipos de energía en la BD (abre si Energía Limpia = 0%)"):
        st.markdown(
            '<p style="font-size:0.8rem;color:#94A3B8;margin-bottom:0.5rem">'
            'Esta tabla muestra los valores exactos de <code>resource_type</code> '
            'que cargó el ETL de XM en Supabase. Si el porcentaje de energía limpia '
            'es 0%, verifica que los tipos renovables aparezcan aquí y ajusta el filtro.</p>',
            unsafe_allow_html=True,
        )
        try:
            df_diag = get_resource_types_diagnostico()
            if not df_diag.empty:
                st.dataframe(
                    df_diag.rename(columns={
                        "resource_type": "Tipo de Recurso (resource_type)",
                        "registros":     "Registros en BD",
                        "gwh_total":     "Generación Total (GWh)",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )
                # Alerta si no hay tipos limpios reconocidos
                tipos = df_diag["resource_type"].str.upper().tolist()
                limpios = [t for t in tipos if any(
                    k in t for k in ["HIDRAUL","SOLAR","EOLIC","MENORES","BIOMASA","BAGAZO","GEOTERM","RENOVABLE"]
                )]
                if limpios:
                    st.success(f"✅ Tipos renovables detectados: **{', '.join(limpios)}**")
                else:
                    st.warning(
                        "⚠️ **Ningún tipo coincide con los patrones renovables actuales.** "
                        "Copia el nombre exacto de la columna de arriba y actualiza el CASE WHEN "
                        "en `queries/analytics.py` → `get_coevolucion_nacional()`."
                    )
            else:
                st.info("La tabla fact_energy está vacía.")
        except Exception as e:
            st.error(f"Error al consultar tipos: {e}")


# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 — BRECHAS REGIONALES
# ──────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown(
        '<h3 style="font-size:1.1rem;font-weight:700;color:#F1F5F9;margin-bottom:0.15rem">'
        '🗺️ Radiografía Geográfica del Talento STEM — 2023</h3>'
        '<p style="font-size:0.82rem;color:#64748B;margin-top:0">'
        '¿Dónde se forma el capital humano? ¿Coincide con las zonas de mayor potencial energético?</p>',
        unsafe_allow_html=True,
    )

    st.markdown(_alert(
        "Brecha Territorial Crítica",
        "La <b>Región Andina concentra el 68.54%</b> del talento STEM, mientras la "
        "<b>Región Caribe apenas alcanza el 16.47%</b>. Los parques eólicos de La Guajira "
        "y las granjas solares de Cesar se construyen donde menos ingenieros se forman.",
    ), unsafe_allow_html=True)

    sem_reg = st.selectbox("📅 Semestre:", [1, 2],
                           format_func=lambda x: f"2023 — Semestre {x}", key="t2_sem")
    df_reg = df_s1 if sem_reg == 1 else df_s2

    _divider()

    fig_mapa_t2 = chart_mapa_colombia(df_mapa, height=580, show_title=True)
    if fig_mapa_t2 is not None:
        st.plotly_chart(fig_mapa_t2, use_container_width=True)
    else:
        st.info("⚠️ Sin conexión — mostrando distribución alternativa.")

    _divider()

    col_dona, col_det = st.columns([5, 4], gap="large")

    with col_dona:
        st.markdown('<p style="font-size:0.83rem;font-weight:600;color:#94A3B8;margin-bottom:0.3rem">Participación % por Macro-Región</p>', unsafe_allow_html=True)
        if not df_reg.empty:
            st.plotly_chart(chart_distribucion_regional(df_reg), use_container_width=True)

    with col_det:
        st.markdown('<p style="font-size:0.83rem;font-weight:600;color:#94A3B8;margin-bottom:0.5rem">🔎 Detalle por Región</p>', unsafe_allow_html=True)
        if not df_reg.empty:
            reg_sel = st.selectbox("Región:", df_reg["macro_region"].dropna().unique().tolist(), key="t2_reg")
            fila_r  = df_reg[df_reg["macro_region"] == reg_sel].iloc[0]
            color_r = REGION_COLORS.get(reg_sel, C["teal"])

            st.markdown(
                f'<div style="background:#0F172A;border-radius:14px;padding:1.4rem;'
                f'border-left:5px solid {color_r};box-shadow:0 4px 20px rgba(0,0,0,0.4);margin-top:0.5rem">'
                f'<div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#475569">Macro-Región</div>'
                f'<div style="font-size:1.1rem;font-weight:800;color:{color_r};margin:0.2rem 0 1rem 0">{reg_sel}</div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.8rem">'
                f'<div style="background:#1E293B;border-radius:10px;padding:0.8rem;text-align:center">'
                f'<div style="font-size:1.5rem;font-weight:800;color:#F1F5F9">{int(fila_r["cantidad_departamentos"])}</div>'
                f'<div style="font-size:0.68rem;color:#64748B;text-transform:uppercase;font-weight:600">Departamentos</div></div>'
                f'<div style="background:#1E293B;border-radius:10px;padding:0.8rem;text-align:center">'
                f'<div style="font-size:1.5rem;font-weight:800;color:{color_r}">{float(fila_r["porcentaje_participacion_talento"]):.1f}%</div>'
                f'<div style="font-size:0.68rem;color:#64748B;text-transform:uppercase;font-weight:600">Participación</div></div></div>'
                f'<div style="margin-top:0.9rem;font-size:0.85rem;color:#94A3B8;font-weight:600">'
                f'🎓 {int(fila_r["estudiantes_matriculados"]):,} estudiantes STEM</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            contextos = {
                "Andina":    ("insight", "Epicentro del talento.", "Alta densidad de IES. Requiere estrategias de movilidad hacia regiones con demanda energética real."),
                "Caribe":    ("alert",   "Brecha estructural urgente.", "Alta demanda eólica y solar, pero baja oferta local de ingenieros. Prioridad de política pública."),
                "Pacífica":  ("insight", "Potencial hídrico elevado.", "Déficit de ingeniería eléctrica para aprovechar los recursos del litoral."),
                "Orinoquía": ("insight", "Llanura en expansión.", "Región en crecimiento energético con baja densidad de formación STEM."),
                "Amazonía":  ("insight", "En consolidación.", "Énfasis en sostenibilidad y energía renovable aislada."),
                "Insular":   ("insight", "Archipiélago estratégico.", "Alta dependencia diésel; potencial solar y eólico sin explotar."),
            }
            st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
            for key, (tipo, titulo, cuerpo) in contextos.items():
                if key in reg_sel:
                    fn = _insight if tipo == "insight" else _alert
                    st.markdown(fn(titulo, cuerpo), unsafe_allow_html=True)
                    break

    with st.expander("📊 Tabla regional completa"):
        st.dataframe(df_reg.rename(columns={
            "macro_region": "Macro-Región",
            "cantidad_departamentos": "Departamentos",
            "estudiantes_matriculados": "Estudiantes STEM",
            "porcentaje_participacion_talento": "Participación %",
        }), use_container_width=True, hide_index=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 3 — MODELO ESTADÍSTICO
# ──────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown(
        '<h3 style="font-size:1.1rem;font-weight:700;color:#F1F5F9;margin-bottom:0.15rem">'
        '🧮 Modelo Estadístico Relacional — Pearson + OLS</h3>'
        '<p style="font-size:0.82rem;color:#64748B;margin-top:0">'
        'Resultados de la Fase de Modelado: cruce STEM × Empleo Energético · 2023.</p>',
        unsafe_allow_html=True,
    )

    _divider()

    # 4 KPI cards usando st.columns (sin flex, sin bug)
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    for col, ico, lbl, val, sub, color in [
        (k1, "🔗", "r — Pearson",    f"{modelo['r']:.4f}",         "Coevolución perfecta",     C["teal"]),
        (k2, "📈", "R² — OLS",       f"{modelo['r2']:.4f}",        "Ajuste del modelo",         C["green"]),
        (k3, "📐", "m — Pendiente",  f"{modelo['slope']:.6f}",     "↑10K est. → +10.41K emp.", C["gold"]),
        (k4, "📍", "b — Intercepto", f"{modelo['intercept']:.2f}", "Base del modelo",           C["purple"]),
    ]:
        with col:
            st.markdown(_kpi_card(ico, lbl, val, sub, color), unsafe_allow_html=True)

    _divider()

    col_eq, col_int = st.columns([1, 1], gap="large")

    with col_eq:
        st.markdown(
            '<div style="background:#0F172A;border:1px solid #1E293B;border-radius:16px;padding:1.8rem;text-align:center">'
            '<div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:0.12em;color:#22D3EE;margin-bottom:0.8rem">📐 Ecuación del Modelo OLS</div>',
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
            f"en electricidad, gas y agua.",
        ), unsafe_allow_html=True)
        st.markdown(_alert(
            "Nota de Evaluación Científica",
            "R² = 1.0000 es esperado con dos puntos de muestra. El modelo es un "
            "<b>descriptor exacto del 2023</b>. Para tendencia predictiva se recomienda "
            "incorporar la serie histórica 2018–2023.",
        ), unsafe_allow_html=True)

    _divider()

    col_ols, col_top = st.columns([1, 1], gap="large")

    with col_ols:
        st.markdown('<p style="font-size:0.85rem;font-weight:600;color:#94A3B8;margin-bottom:0.2rem">📉 Recta de Regresión OLS</p>', unsafe_allow_html=True)
        df_mod = modelo["df"]
        if not df_mod.empty:
            st.plotly_chart(chart_regresion(df_mod, modelo["slope"], modelo["intercept"]), use_container_width=True)

    with col_top:
        st.markdown('<p style="font-size:0.85rem;font-weight:600;color:#94A3B8;margin-bottom:0.2rem">🏆 Top 10 Áreas de Conocimiento STEM</p>', unsafe_allow_html=True)
        if not df_top.empty:
            st.plotly_chart(chart_top_areas(df_top), use_container_width=True)

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


# ═════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(
    '<div style="margin-top:2rem;background:#0F172A;border:1px solid #1E293B;'
    'border-radius:14px;padding:1.1rem 2rem;text-align:center;font-size:0.78rem;color:#334155">'
    '⚡ <b style="color:#475569">Coevolución STEM–Energía · Colombia 2023</b>'
    ' &nbsp;|&nbsp; 👩‍💻 <b style="color:#475569">Camila Acosta &amp; Cristian Robledo</b>'
    ' &nbsp;|&nbsp; 🏫 <b style="color:#475569">Talento Tech</b>'
    ' &nbsp;|&nbsp; SNIES · XM · DANE–GEIH · Banco Mundial · Mayo 2026'
    '</div>',
    unsafe_allow_html=True,
)
