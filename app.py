"""
app.py — Punto de entrada del Dashboard
────────────────────────────────────────
Autores : Camila Acosta & Cristian Robledo  |  Talento Tech  |  Mayo 2026
"""

import streamlit as st

# ── set_page_config SIEMPRE primero ──────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Coevolución Capital Humano & Energía ⚡",
    page_icon="⚡",
    initial_sidebar_state="collapsed",
)

# ── CSS global ────────────────────────────────────────────────────────────────
from utils.ui import CSS
st.markdown(CSS, unsafe_allow_html=True)

# ── Queries (backend) ─────────────────────────────────────────────────────────
from queries.analytics import (
    get_coevolucion_nacional,
    get_distribucion_regional,
    get_mapa_colombia,
    get_top_areas_conocimiento,
    get_modelo_estadistico,
)

# ── Componentes (frontend) ────────────────────────────────────────────────────
from components.hero import render_hero
from components.tab_coevolucion import render_tab_coevolucion
from components.tab_regional import render_tab_regional
from components.tab_modelo import render_tab_modelo


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


_loader = st.empty()
_loader.markdown("""
<div style="position:fixed;inset:0;z-index:9999;background:#020817;
display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1.2rem">
  <div style="width:56px;height:56px;border-radius:50%;
  border:4px solid #1E293B;border-top-color:#22D3EE;
  animation:spin 0.9s linear infinite"></div>
  <div style="font-size:0.95rem;font-weight:600;color:#64748B;letter-spacing:0.05em">
    Conectando con Supabase…</div>
  <style>@keyframes spin{to{transform:rotate(360deg)}}</style>
</div>
""", unsafe_allow_html=True)

try:
    df_coev, df_s1, df_s2, df_mapa, df_top, modelo = _cargar_todo()
    st.toast("Datos cargados ✓", icon="⚡")
except Exception as exc:
    _loader.empty()
    st.error(f"**No se pudo conectar con Supabase.**\n\n`{exc}`")
    st.stop()

_loader.empty()


# ─────────────────────────────────────────────────────────────────────────────
# MÉTRICAS GLOBALES
# ─────────────────────────────────────────────────────────────────────────────
if len(df_coev) >= 2:
    s1 = df_coev.iloc[-2]
    s2 = df_coev.iloc[-1]
elif len(df_coev) == 1:
    s1 = df_coev.iloc[0]
    s2 = s1
else:
    s1, s2 = None, None

s1_label = f"S{int(s1['semester'])}·{int(s1['year'])}" if s1 is not None else "—"
s2_label = f"S{int(s2['semester'])}·{int(s2['year'])}" if s2 is not None else "—"


def _get_pct(df, region_substr: str) -> float:
    mask = df["macro_region"].str.contains(region_substr, na=False)
    return float(df.loc[mask, "porcentaje_participacion_talento"].iloc[0]) if mask.any() else 0.0


pct_andina = _get_pct(df_s1, "Andina")
pct_caribe  = _get_pct(df_s1, "Caribe")


# ─────────────────────────────────────────────────────────────────────────────
# RENDER
# ─────────────────────────────────────────────────────────────────────────────
render_hero(df_mapa, s1, s2, modelo, pct_andina, pct_caribe, s1_label, s2_label)

tab1, tab2, tab3 = st.tabs([
    "📊  Coevolución Nacional",
    "🗺️  Brechas Regionales",
    "🧮  Modelo Estadístico",
])

with tab1:
    render_tab_coevolucion(df_coev, modelo)

with tab2:
    render_tab_regional(df_s1, df_s2, df_mapa, pct_andina, pct_caribe)

with tab3:
    render_tab_modelo(modelo, df_top)


# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    '<div style="margin-top:2rem;background:#0F172A;border:1px solid #1E293B;'
    'border-radius:14px;padding:1.1rem 2rem;text-align:center;font-size:0.78rem;color:#334155">'
    '⚡ <b style="color:#475569">Coevolución STEM–Energía · Colombia 2022-2024</b>'
    ' &nbsp;|&nbsp; 👩‍💻 <b style="color:#475569">Camila Acosta &amp; Cristian Robledo</b>'
    ' &nbsp;|&nbsp; 🏫 <b style="color:#475569">Talento Tech</b>'
    ' &nbsp;|&nbsp; SNIES · XM · DANE–GEIH · Banco Mundial · Jun 2026'
    '</div>',
    unsafe_allow_html=True,
)
