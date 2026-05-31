"""
components/tab_regional.py
───────────────────────────
Tab 2 — Brechas Regionales.
"""

import streamlit as st

from utils.ui import alert, insight, divider, skeleton
from utils.charts import C, REGION_COLORS, chart_mapa_colombia, chart_distribucion_regional


def render_tab_regional(df_s1, df_s2, df_mapa, pct_andina: float, pct_caribe: float) -> None:
    st.markdown(
        '<h3 style="font-size:1.1rem;font-weight:700;color:#F1F5F9;margin-bottom:0.15rem">'
        '🗺️ Radiografía Geográfica del Talento STEM — 2022-2024</h3>'
        '<p style="font-size:0.82rem;color:#64748B;margin-top:0">'
        '¿Dónde se forma el capital humano? ¿Coincide con las zonas de mayor potencial energético?</p>',
        unsafe_allow_html=True,
    )

    st.markdown(alert(
        "Brecha Territorial Crítica",
        f"La <b>Región Andina concentra el {pct_andina:.2f}%</b> del talento STEM, mientras la "
        f"<b>Región Caribe apenas alcanza el {pct_caribe:.2f}%</b>. Los parques eólicos de La Guajira "
        f"y las granjas solares de Cesar se construyen donde menos ingenieros se forman.",
    ), unsafe_allow_html=True)

    sem_reg = st.selectbox("📅 Semestre:", [1, 2],
                           format_func=lambda x: f"Semestre {x} — Serie 2022-2024", key="t2_sem")
    df_reg = df_s1 if sem_reg == 1 else df_s2

    divider()

    _ph_mapa = st.empty()
    _ph_mapa.markdown(skeleton(580), unsafe_allow_html=True)
    fig_mapa = chart_mapa_colombia(df_mapa, height=580, show_title=True)
    if fig_mapa is not None:
        _ph_mapa.plotly_chart(fig_mapa, use_container_width=True)
    else:
        _ph_mapa.info("⚠️ Sin conexión — mostrando distribución alternativa.")

    divider()

    col_dona, col_det = st.columns([5, 4], gap="large")

    with col_dona:
        st.markdown(
            '<p style="font-size:0.83rem;font-weight:600;color:#94A3B8;margin-bottom:0.3rem">'
            'Participación % por Macro-Región</p>',
            unsafe_allow_html=True,
        )
        if not df_reg.empty:
            _ph_dona = st.empty()
            _ph_dona.markdown(skeleton(400), unsafe_allow_html=True)
            _ph_dona.plotly_chart(chart_distribucion_regional(df_reg), use_container_width=True)

    with col_det:
        st.markdown(
            '<p style="font-size:0.83rem;font-weight:600;color:#94A3B8;margin-bottom:0.5rem">'
            '🔎 Detalle por Región</p>',
            unsafe_allow_html=True,
        )
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
                    fn = insight if tipo == "insight" else alert
                    st.markdown(fn(titulo, cuerpo), unsafe_allow_html=True)
                    break

    with st.expander("📊 Tabla regional completa"):
        st.dataframe(df_reg.rename(columns={
            "macro_region": "Macro-Región",
            "cantidad_departamentos": "Departamentos",
            "estudiantes_matriculados": "Estudiantes STEM",
            "porcentaje_participacion_talento": "Participación %",
        }), use_container_width=True, hide_index=True)
