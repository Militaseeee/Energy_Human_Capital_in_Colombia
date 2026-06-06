"""
utils/ui.py
───────────
CSS global y helpers HTML para el dashboard oscuro.
"""

import streamlit as st

# ─────────────────────────────────────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────────────────────────────────────
CSS = """
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
[data-testid="stMainBlockContainer"] { padding-bottom: 6rem !important; }

/* ── st.metric ── */
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

/* ── Espaciado entre bloques verticales ── */
[data-testid="stVerticalBlock"] { gap: 0.5rem !important; }

/* ── Animaciones ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes shimmer {
    0%   { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
[data-testid="stPlotlyChart"],
[data-testid="stMetric"],
[data-testid="stMarkdownContainer"] > div {
    animation: fadeUp 0.45s ease both;
}

/* ── Ocultar UI de Streamlit ── */
#MainMenu, footer,
[data-testid="stToolbar"],
[data-testid="stToolbarActions"],
[data-testid="stToolbarActionButton"],
[data-testid="stDecoration"],
[data-testid="stHeader"] { display: none !important; }

/* ─────────────────────────────────────────────────────────────────────────
   RESPONSIVE — MÓVIL  (≤ 768 px)
   ───────────────────────────────────────────────────────────────────────── */
@media (max-width: 768px) {

    /* Sin scroll horizontal */
    body, .stApp { overflow-x: hidden !important; }

    /* Padding lateral — varios selectores para cubrir versiones de Streamlit */
    [data-testid="stMainBlockContainer"],
    .main .block-container,
    section.main > div:first-child {
        padding: 0.5rem 0.75rem 4rem !important;
        max-width: 100% !important;
    }

    /* ── Ocultar elementos verbosos del hero en móvil ── */
    .hero-desktop-extra { display: none !important; }

    /* ── Apilar TODAS las columnas en vertical ── */
    [data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 0.4rem !important;
        row-gap: 0.4rem !important;
    }
    [data-testid="stColumn"] {
        min-width: 100% !important;
        flex: 1 1 100% !important;
    }

    /* ── Excepción: fila de 4 KPIs → cuadrícula 2×2 ── */
    [data-testid="stHorizontalBlock"]:has(
        > [data-testid="stColumn"]:nth-child(4)
    ) > [data-testid="stColumn"] {
        min-width: calc(50% - 0.35rem) !important;
        flex: 1 1 calc(50% - 0.35rem) !important;
    }

    /* ── Título hero más compacto ── */
    h1 {
        font-size: 1.6rem !important;
        line-height: 1.2 !important;
        margin-bottom: 0.5rem !important;
    }

    /* ── Métricas compactas ── */
    div[data-testid="stMetricValue"] > div { font-size: 1rem !important; }
    div[data-testid="stMetricLabel"] > div { font-size: 0.56rem !important; }
    div[data-testid="stMetricDelta"] > div { font-size: 0.56rem !important; }
    div[data-testid="metric-container"]    { padding: 0.55rem 0.35rem !important; }

    /* ── Tabs: scroll horizontal, sin salto de línea ── */
    .stTabs [data-baseweb="tab-list"] {
        overflow-x: auto !important;
        flex-wrap: nowrap !important;
        -webkit-overflow-scrolling: touch !important;
        scrollbar-width: none !important;
    }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar { display: none !important; }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.68rem !important;
        padding: 0.38rem 0.65rem !important;
        white-space: nowrap !important;
    }

    /* ── Gráficos ── */
    [data-testid="stPlotlyChart"] { min-height: unset !important; }

    /* ── Gaps verticales ── */
    [data-testid="stVerticalBlock"] { gap: 0.35rem !important; }

    /* ── Cards custom HTML: evitar desbordamiento ── */
    [data-testid="stMarkdownContainer"] div[style] {
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
}

/* ─────────────────────────────────────────────────────────────────────────
   RESPONSIVE — TABLET  (769 px – 1024 px)
   ───────────────────────────────────────────────────────────────────────── */
@media (min-width: 769px) and (max-width: 1024px) {

    [data-testid="stMainBlockContainer"] {
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }

    /* Fila de 4 KPIs → 2×2 también en tablet */
    [data-testid="stHorizontalBlock"]:has(
        > [data-testid="stColumn"]:nth-child(4)
    ) > [data-testid="stColumn"] {
        min-width: calc(50% - 0.5rem) !important;
        flex: 1 1 calc(50% - 0.5rem) !important;
    }

    [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }

    h1 { font-size: 2.1rem !important; }
}
</style>
"""


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS HTML
# ─────────────────────────────────────────────────────────────────────────────

def divider(color: str = "#1E293B") -> None:
    st.markdown(
        f'<hr style="border:none;border-top:1px solid {color};margin:1rem 0">',
        unsafe_allow_html=True,
    )


def gradient_divider() -> None:
    st.markdown(
        '<div style="height:3px;background:linear-gradient(to right,'
        '#1E293B,#22D3EE,#60A5FA,#1E293B);border-radius:2px;margin:1.2rem 0"></div>',
        unsafe_allow_html=True,
    )


def alert(titulo: str, cuerpo: str) -> str:
    return (
        '<div style="background:#1a0a0a;border:1px solid #7F1D1D;border-left:5px solid #F87171;'
        'border-radius:14px;padding:1.2rem 1.5rem;margin:0.8rem 0">'
        f'<div style="font-weight:700;color:#FCA5A5;font-size:0.93rem;margin-bottom:0.35rem">🚨 {titulo}</div>'
        f'<div style="color:#FCA5A5;font-size:0.85rem;line-height:1.65;opacity:0.85">{cuerpo}</div>'
        '</div>'
    )


def insight(titulo: str, cuerpo: str) -> str:
    return (
        '<div style="background:#051a0f;border:1px solid #166534;border-left:5px solid #4ADE80;'
        'border-radius:14px;padding:1.2rem 1.5rem;margin:0.8rem 0">'
        f'<div style="font-weight:700;color:#86EFAC;font-size:0.93rem;margin-bottom:0.35rem">💡 {titulo}</div>'
        f'<div style="color:#86EFAC;font-size:0.85rem;line-height:1.65;opacity:0.85">{cuerpo}</div>'
        '</div>'
    )


def card_metrica(icon: str, value: str, label: str, sublabel: str, color: str, explain: str = "") -> str:
    _det = (
        f'<details style="margin-top:0.65rem;border-top:1px solid #1E293B;padding-top:0.45rem">'
        f'<summary style="cursor:pointer;font-size:0.65rem;color:#475569;font-weight:600;'
        f'outline:none;display:flex;align-items:center;justify-content:center;gap:0.3rem">'
        f'<span class="card-arrow">▶</span> ¿Qué es esto?</summary>'
        f'<p style="font-size:0.7rem;color:#64748B;line-height:1.55;margin:0.45rem 0 0;text-align:left">'
        f'{explain}</p></details>'
    ) if explain else ""
    return (
        f'<div style="background:#0F172A;border-radius:16px;padding:1.4rem 1rem;'
        f'border-top:4px solid {color};box-shadow:0 4px 20px rgba(0,0,0,0.4);text-align:center">'
        f'<div style="font-size:2rem;margin-bottom:0.3rem">{icon}</div>'
        f'<div style="font-size:1.8rem;font-weight:800;color:{color};line-height:1.1">{value}</div>'
        f'<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:0.07em;color:#F1F5F9;margin-top:0.5rem">{label}</div>'
        f'<div style="font-size:0.7rem;color:#64748B;margin-top:0.12rem">{sublabel}</div>'
        f'{_det}</div>'
    )


def skeleton(height: int = 400) -> str:
    return (
        f'<div style="background:#0F172A;border-radius:16px;height:{height}px;'
        f'position:relative;overflow:hidden;border:1px solid #1E293B">'
        f'<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center">'
        f'<div style="font-size:1.8rem;opacity:0.25">⚡</div>'
        f'<div style="font-size:0.68rem;font-weight:700;letter-spacing:0.14em;color:#334155;margin-top:0.4rem">CARGANDO</div>'
        f'</div>'
        f'<div style="position:absolute;inset:0;background:linear-gradient(90deg,'
        f'transparent 0%,rgba(34,211,238,0.06) 50%,transparent 100%);'
        f'animation:shimmer 1.6s ease-in-out infinite"></div>'
        f'</div>'
    )


def kpi_card(icon: str, label: str, value: str, sublabel: str, color: str) -> str:
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
