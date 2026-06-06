"""
components/tab_modelo.py
─────────────────────────
Tab 3 — Modelo Estadístico (Pearson + OLS).
"""

import textwrap

import streamlit as st

from utils.ui import divider, insight, alert, kpi_card, skeleton
from utils.charts import C, chart_regresion, chart_top_areas


def render_tab_modelo(modelo: dict, df_top) -> None:
    st.markdown(
        '<h3 style="font-size:1.1rem;font-weight:700;color:#F1F5F9;margin-bottom:0.15rem">'
        '🧮 Modelo Estadístico Relacional — Pearson + OLS</h3>'
        '<p style="font-size:0.82rem;color:#64748B;margin-top:0">'
        'Resultados de la Fase de Modelado: cruce STEM × Empleo Energético · 2022-2024.</p>',
        unsafe_allow_html=True,
    )

    divider()

    k1, k2, k3, k4 = st.columns(4, gap="medium")
    for col, ico, lbl, val, sub, color in [
        (k1, "🔗", "r — Pearson",    f"{modelo['r']:.4f}",         "Coevolución perfecta",     C["teal"]),
        (k2, "📈", "R² — OLS",       f"{modelo['r2']:.4f}",        "Ajuste del modelo",         C["green"]),
        (k3, "📐", "m — Pendiente",  f"{modelo['slope']:.6f}",     "↑10K est. → +10.41K emp.", C["gold"]),
        (k4, "📍", "b — Intercepto", f"{modelo['intercept']:.2f}", "Base del modelo",           C["purple"]),
    ]:
        with col:
            st.markdown(kpi_card(ico, lbl, val, sub, color), unsafe_allow_html=True)

    divider()

    col_eq, col_int = st.columns([1, 1], gap="large")

    with col_eq:
        st.markdown(
            textwrap.dedent("""
            <div style="background: #0F172A;
                        border-radius: 16px;
                        border-left: 5px solid #22D3EE;
                        padding: 2rem;
                        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
                        position: relative;
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        border-top: 1px solid #1E293B;
                        border-right: 1px solid #1E293B;
                        border-bottom: 1px solid #1E293B;
                        margin: 0.8rem 0px;">
            <div style="position: absolute; top: 0; left: 0;
                        background: #22D3EE; color: #020817;
                        padding: 0.4rem 1.2rem;
                        border-radius: 14px 0 14px 0;
                        font-weight: 900; font-size: 0.72rem;
                        letter-spacing: 0.1em; text-transform: uppercase;">
                📐 Estructura Matemática
            </div>
            <div style="margin-top: 1rem; padding: 1.5rem;
                        background: #020817;
                        border: 1px dashed #334155;
                        border-radius: 12px;
                        text-align: center;">
                <span style="font-size: 1.8rem; font-weight: 900; color: #F1F5F9; letter-spacing: 0.02em;">
                Y = <span style="color: #EAB308;">{slope}</span> &middot; X + <span style="color: #A78BFA;">({intercept})</span>
                </span>
            </div>
            <div style="display: flex; justify-content: space-around; margin-top: 1.5rem; padding-top: 1.2rem; border-top: 1px solid #1E293B;">
                <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
                <div style="width: 24px; height: 4px; background: #EAB308; border-radius: 2px; margin-bottom: 0.5rem;"></div>
                <span style="color: #E2E8F0; font-weight: 700; font-size: 0.85rem;">Variable X</span>
                <span style="color: #64748B; font-size: 0.75rem; font-weight: 600; margin-top: 0.2rem;">Talento STEM<br>(Matriculados)</span>
                </div>
                <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
                <div style="width: 24px; height: 4px; background: #A78BFA; border-radius: 2px; margin-bottom: 0.5rem;"></div>
                <span style="color: #E2E8F0; font-weight: 700; font-size: 0.85rem;">Variable Y</span>
                <span style="color: #64748B; font-size: 0.75rem; font-weight: 600; margin-top: 0.2rem;">Empleo Energía<br>(Miles)</span>
                </div>
            </div>
            </div>
            """).strip().format(slope=f"{modelo['slope']:.6f}", intercept=f"{modelo['intercept']:.2f}"),
            unsafe_allow_html=True,
        )

    with col_int:
        inc_1m = modelo["slope"] * 1_000_000
        st.markdown(insight(
            "Interpretación Ejecutiva",
            f"Con <b>r = {modelo['r']:.4f}</b> sobre 6 semestres (2022-2024), el modelo detecta "
            f"una tendencia positiva entre la formación STEM y el empleo energético. "
            f"La ecuación OLS estima que por cada <b>1 millón de estudiantes</b> adicionales en STEM, "
            f"el sector energético tiende a expandirse en <b>{inc_1m:.2f} mil empleos</b> formales.",
        ), unsafe_allow_html=True)
        st.markdown(alert(
            "Nota de Evaluación Científica",
            "El modelo OLS se ha entrenado exitosamente utilizando una serie histórica continua "
            "de 6 semestres (2022-2024). Esto otorga validez estadística a la pendiente (m) y al "
            "coeficiente de correlación (r), superando el sesgo de la muestra inicial.",
        ), unsafe_allow_html=True)

    divider()

    col_ols, col_top = st.columns([1, 1], gap="large")
    df_mod = modelo["df"]

    with col_ols:
        st.markdown(
            '<p style="font-size:1rem;font-weight:700;color:#94A3B8;margin-top:1.4rem;margin-bottom:0.2rem">'
            '📉 Recta de Regresión OLS</p>',
            unsafe_allow_html=True,
        )
        if not df_mod.empty:
            _ph_ols = st.empty()
            _ph_ols.markdown(skeleton(420), unsafe_allow_html=True)
            _ph_ols.plotly_chart(
                chart_regresion(df_mod, modelo["slope"], modelo["intercept"]),
                use_container_width=True,
            )

    with col_top:
        st.markdown(
            '<p style="font-size:1rem;font-weight:700;color:#94A3B8;margin-top:1.4rem;margin-bottom:0.2rem">'
            '🏆 Top 10 Áreas de Conocimiento STEM</p>',
            unsafe_allow_html=True,
        )
        if not df_top.empty:
            _ph_top = st.empty()
            _ph_top.markdown(skeleton(520), unsafe_allow_html=True)
            _ph_top.plotly_chart(chart_top_areas(df_top), use_container_width=True)

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
