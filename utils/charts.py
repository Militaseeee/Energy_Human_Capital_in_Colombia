"""
utils/charts.py
────────────────
Constructores de gráficos Plotly optimizados para tema oscuro.
"""

import unicodedata
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

# ── Paleta oscura — brillante sobre fondo #020817 ─────────────────────────────
REGION_COLORS: dict[str, str] = {
    "Región Andina":    "#60A5FA",   # Blue 400    — núcleo STEM
    "Región Caribe":    "#FBBF24",   # Amber 400   — alerta brecha
    "Región Pacífica":  "#4ADE80",   # Green 400   — litoral
    "Región Orinoquía": "#C084FC",   # Purple 400  — llanura
    "Región Amazonía":  "#22D3EE",   # Cyan 400    — selva
    "Región Insular":   "#F472B6",   # Pink 400    — archipiélago
}

# Colores de acento general
C = {
    "teal":   "#22D3EE",
    "blue":   "#60A5FA",
    "green":  "#4ADE80",
    "gold":   "#FBBF24",
    "purple": "#C084FC",
    "red":    "#F87171",
    "text":   "#F1F5F9",
    "muted":  "#94A3B8",
    "surface":"#0F172A",
    "card":   "#1E293B",
    "border": "#334155",
}

# Layout base oscuro — SIN 'legend' para evitar keyword-conflict cuando
# cada función pasa su propio legend=dict(...)
_DARK = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(15,23,42,0.4)",
    font=dict(color=C["text"], family="Plus Jakarta Sans, Segoe UI, sans-serif"),
)


def _leg(**extra) -> dict:
    """Devuelve un dict de leyenda con estilos oscuros base + sobrescrituras."""
    base = dict(
        bgcolor="#1E293B",
        bordercolor="#334155",
        borderwidth=1,
        font=dict(color=C["text"]),
    )
    base.update(extra)
    return base


# ── Utilidad: normalizar nombres para match GeoJSON ───────────────────────────
def _norm(name: str) -> str:
    nfkd = unicodedata.normalize("NFKD", str(name).upper().strip())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


# ── GeoJSON Colombia ──────────────────────────────────────────────────────────
@st.cache_data(ttl=86_400, show_spinner="🗺️ Descargando mapa de Colombia…")
def _fetch_colombia_geojson() -> dict | None:
    try:
        import requests
        url = (
            "https://gist.githubusercontent.com/john-guerra/"
            "43c7656821069d00dcbc/raw/"
            "3aadedf47badbdac823b00dbe259f6bc6d9e1899/colombia.geo.json"
        )
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        geojson = resp.json()
        for feat in geojson["features"]:
            raw = feat["properties"].get("NOMBRE_DPT", "")
            feat["properties"]["dept_norm"] = _norm(raw)
        return geojson
    except Exception:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# HERO — Mapa coroplético oscuro (usado en página principal)
# ─────────────────────────────────────────────────────────────────────────────
def chart_mapa_hero(df_mapa: pd.DataFrame) -> go.Figure | None:
    """Versión compacta del mapa para el hero section."""
    return chart_mapa_colombia(df_mapa, height=520, show_title=False)


# ─────────────────────────────────────────────────────────────────────────────
# MAPA COROPLÉTICO — Tab 2
# ─────────────────────────────────────────────────────────────────────────────
def chart_mapa_colombia(
    df_mapa: pd.DataFrame,
    height: int = 580,
    show_title: bool = True,
) -> go.Figure | None:
    geojson = _fetch_colombia_geojson()
    if geojson is None:
        return None

    df = df_mapa.copy()
    df["dept_norm"] = df["departamento"].apply(_norm)

    fig = px.choropleth(
        df,
        geojson=geojson,
        locations="dept_norm",
        featureidkey="properties.dept_norm",
        color="macro_region",
        color_discrete_map=REGION_COLORS,
        hover_name="departamento",
        hover_data={"macro_region": True, "total_stem": ":,", "dept_norm": False},
        labels={"macro_region": "Macro-Región", "total_stem": "Estudiantes STEM"},
        category_orders={"macro_region": list(REGION_COLORS.keys())},
    )

    fig.update_geos(fitbounds="locations", visible=False, bgcolor="rgba(0,0,0,0)")
    fig.update_traces(
        marker_line_color="#020817",
        marker_line_width=0.9,
    )

    title_cfg = (
        dict(
            text="<b>🗺️ Distribución del Capital Humano STEM — Colombia (2022-2024)</b>",
            x=0.5, xanchor="center",
            font=dict(size=15, color=C["text"]),
        )
        if show_title
        else dict(text="")
    )

    fig.update_layout(
        **_DARK,
        title=title_cfg,
        legend=_leg(
            title="<b>Macro-Región</b>",
            font=dict(color=C["text"], size=11),
            orientation="v",
            x=1.01, y=0.5,
        ),
        height=height,
        margin=dict(t=50 if show_title else 10, b=10, l=0, r=0),
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICO 1 — Doble eje Y (Tab 1)
# ─────────────────────────────────────────────────────────────────────────────
def chart_coevolucion(df: pd.DataFrame) -> go.Figure:
    periodos = [f"Sem. {int(row['semester'])} · {int(row['year'])}" for _, row in df.iterrows()]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=periodos, y=df["total_talento_stem"],
            name="🎓 Talento STEM",
            mode="lines+markers+text",
            text=[f"<b>{int(v):,}</b>" for v in df["total_talento_stem"]],
            textposition="top center",
            textfont=dict(size=13, color=C["blue"]),
            line=dict(color=C["blue"], width=4),
            marker=dict(size=14, color=C["blue"], line=dict(color="#020817", width=2)),
            fill="tozeroy",
            fillcolor="rgba(96,165,250,0.08)",
        ),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(
            x=periodos, y=df["empleo_energia_miles"],
            name="⚡ Empleo Energía (K)",
            mode="lines+markers+text",
            text=[f"<b>{float(v):.2f} K</b>" for v in df["empleo_energia_miles"]],
            textposition="bottom center",
            textfont=dict(size=13, color=C["gold"]),
            line=dict(color=C["gold"], width=4, dash="dash"),
            marker=dict(size=14, symbol="diamond", color=C["gold"],
                        line=dict(color="#020817", width=2)),
        ),
        secondary_y=True,
    )

    fig.update_layout(
        **_DARK,
        title=dict(
            text="<b>Coevolución (2022-2024) — Formación STEM ↔ Empleo Energético</b>",
            x=0.5, xanchor="center",
            font=dict(size=16, color=C["text"]),
        ),
        xaxis_title="Periodo Académico",
        legend=_leg(orientation="h", y=-0.22, x=0.5, xanchor="center",
                    bgcolor="rgba(0,0,0,0)", font=dict(size=12, color=C["text"])),
        height=460,
        margin=dict(t=70, b=90),
        xaxis=dict(showgrid=False, color=C["muted"]),
    )
    fig.update_yaxes(
        title_text="<b>Estudiantes STEM</b>",
        title_font=dict(color=C["blue"]),
        tickfont=dict(color=C["blue"]),
        showgrid=True, gridcolor="#1E293B",
        secondary_y=False,
    )
    fig.update_yaxes(
        title_text="<b>Ocupados Energía</b> (K)",
        title_font=dict(color=C["gold"]),
        tickfont=dict(color=C["gold"]),
        showgrid=False,
        secondary_y=True,
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICO 2B — Dona fallback (Tab 2)
# ─────────────────────────────────────────────────────────────────────────────
def chart_distribucion_regional(df: pd.DataFrame, selected: str = "") -> go.Figure:
    pulls = [0.06 if selected and selected in str(r) else 0.0 for r in df["macro_region"]]

    fig = px.pie(
        df,
        values="estudiantes_matriculados",
        names="macro_region",
        color="macro_region",
        color_discrete_map=REGION_COLORS,
        hole=0.44,
    )
    fig.update_traces(
        pull=pulls,
        textinfo="percent+label",
        textfont=dict(size=12, color=C["text"]),
        marker=dict(line=dict(color="#020817", width=2)),
        hovertemplate="<b>%{label}</b><br>Estudiantes: <b>%{value:,.0f}</b><br>%{percent}",
    )
    fig.update_layout(
        **_DARK,
        title=dict(
            text="<b>Participación % por Macro-Región</b>",
            x=0.5, xanchor="center", font=dict(size=13),
        ),
        height=400,
        legend=_leg(orientation="v", x=1.0, y=0.5,
                    font=dict(size=11, color=C["text"])),
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICO 3A — Barras horizontales Top 10 (Tab 3)
# ─────────────────────────────────────────────────────────────────────────────
def chart_top_areas(df: pd.DataFrame) -> go.Figure:
    df_s = df.sort_values("total_estudiantes", ascending=True)

    # Escala Blugrn funciona bien en oscuro; se ve vibrante
    fig = px.bar(
        df_s,
        x="total_estudiantes", y="area_conocimiento",
        orientation="h",
        color="total_estudiantes",
        color_continuous_scale="Blugrn",
        text="total_estudiantes",
        labels={"total_estudiantes": "Estudiantes", "area_conocimiento": ""},
    )
    fig.update_traces(
        texttemplate="<b>%{text:,.0f}</b>",
        textposition="outside",
        textfont=dict(size=11, color=C["text"]),
        marker=dict(line=dict(color="rgba(0,0,0,0)")),
    )
    fig.update_layout(
        **_DARK,
        title=dict(
            text="<b>🏆 Top 10 Áreas STEM · Colombia (2022-2024)</b>",
            x=0.5, xanchor="center", font=dict(size=14, color=C["text"]),
        ),
        xaxis_title="Total Estudiantes",
        coloraxis_showscale=False,
        height=520,
        margin=dict(l=270, r=90, t=60, b=40),
        xaxis=dict(showgrid=True, gridcolor="#1E293B", color=C["muted"]),
        yaxis=dict(tickfont=dict(size=11, color=C["text"])),
    )
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# GRÁFICO 3B — Scatter + Recta OLS (Tab 3)
# ─────────────────────────────────────────────────────────────────────────────
def chart_regresion(df: pd.DataFrame, slope: float, intercept: float) -> go.Figure:
    X      = df["talento_stem"].values.astype(float)
    Y_real = df["empleo_energia"].values.astype(float)
    periodos = [f"Semestre {int(s)}" for s in df["semester"]]

    x_line = np.linspace(X.min() * 0.96, X.max() * 1.04, 200)
    y_line = slope * x_line + intercept

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_line, y=y_line, mode="lines",
        name=f"Ŷ = {slope:.4f}·X + ({intercept:.2f})",
        line=dict(color=C["gold"], width=3, dash="dot"),
        fill="tozeroy", fillcolor="rgba(251,191,36,0.05)",
    ))

    fig.add_trace(go.Scatter(
        x=X, y=Y_real, mode="markers+text",
        name="Datos reales (2022-2024)",
        text=periodos, textposition="top center",
        textfont=dict(size=12, color=C["teal"]),
        marker=dict(size=18, color=C["blue"], line=dict(color="#020817", width=3)),
    ))

    fig.update_layout(
        **_DARK,
        title=dict(
            text="<b>📉 Recta OLS: STEM → Empleo Energético</b>",
            x=0.5, xanchor="center", font=dict(size=14),
        ),
        xaxis_title="Estudiantes STEM Matriculados",
        yaxis_title="Empleo Sector Energía (K)",
        legend=_leg(orientation="h", y=-0.22, x=0.5, xanchor="center"),
        height=420,
        xaxis=dict(showgrid=True, gridcolor="#1E293B", color=C["muted"]),
        yaxis=dict(showgrid=True, gridcolor="#1E293B", color=C["muted"]),
    )
    return fig
