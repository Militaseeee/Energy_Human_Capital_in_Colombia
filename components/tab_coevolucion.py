"""
components/tab_coevolucion.py
──────────────────────────────
Tab 1 — Balance de Coevolución Nacional.
"""

import streamlit as st

from utils.ui import divider, card_metrica, skeleton, insight
from utils.charts import C, chart_coevolucion
from queries.analytics import get_resource_types_diagnostico


def render_tab_coevolucion(df_coev, modelo) -> None:
    st.markdown(
        '<h3 style="font-size:1.1rem;font-weight:700;color:#F1F5F9;margin-bottom:0.15rem">'
        '📊 Balance de Coevolución — Serie Histórica 2022-2024</h3>'
        '<p style="font-size:0.82rem;color:#64748B;margin-top:0">'
        'Indicadores cruzados SNIES · XM · DANE por semestre académico.</p>',
        unsafe_allow_html=True,
    )

    if not df_coev.empty:
        opciones = [f"{int(r['year'])} — S{int(r['semester'])}" for _, r in df_coev.iterrows()]
        periodo_sel = st.radio("Periodo:", opciones, index=len(opciones) - 1,
                               horizontal=True, key="t1_sem")
        fila = df_coev.iloc[opciones.index(periodo_sel)]
    else:
        fila = None

    divider()

    if fila is not None:
        mc1, mc2, mc3, mc4 = st.columns(4, gap="medium")
        for col, ico, val, lbl, sub, color, exp in [
            (mc1, "🌿", f"{float(fila['porcentaje_energia_limpia']):.2f}%",
             "Energía Limpia", "Generación renovable", C["green"],
             "Porcentaje de la electricidad colombiana producida por fuentes renovables: hidráulica, solar, eólica y biomasa. Fuente: XM S.A. E.S.P."),
            (mc2, "🎓", f"{int(fila['total_talento_stem']):,}",
             "Talento STEM", "Matrículas universitarias", C["blue"],
             "Total de estudiantes matriculados en carreras de Ciencias, Tecnología, Ingeniería y Matemáticas en universidades colombianas. Fuente: SNIES."),
            (mc3, "⚡", f"{float(fila['empleo_energia_miles']):.2f} K",
             "Empleo en Energía", "Miles de trabajadores", C["gold"],
             "Personas ocupadas formalmente en el sector de suministro de electricidad y gas, expresado en miles de trabajadores. Fuente: DANE-GEIH."),
            (mc4, "📉", f"{float(fila['tasa_desempleo_pais']):.2f}%",
             "Tasa de Desempleo", "Total nacional · DANE", C["red"],
             "Porcentaje de la población económicamente activa que busca empleo sin encontrarlo. Se incluye como contexto macroeconómico nacional. Fuente: DANE."),
        ]:
            with col:
                st.markdown(card_metrica(ico, val, lbl, sub, color, exp), unsafe_allow_html=True)

    st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)

    if not df_coev.empty:
        _ph = st.empty()
        _ph.markdown(skeleton(460), unsafe_allow_html=True)
        _ph.plotly_chart(chart_coevolucion(df_coev), use_container_width=True)
        st.markdown(
            '<div style="margin-top:-2.3rem;padding-left:0.5rem;padding-bottom:2rem">'
            '<details>'
            '<summary style="list-style:none;width:26px;height:26px;border-radius:50%;'
            'background:#1E293B;border:1px solid #334155;display:flex;align-items:center;'
            'justify-content:center;cursor:pointer;font-size:0.72rem;font-weight:700;'
            'color:#94A3B8;outline:none;user-select:none">ℹ</summary>'
            '<div style="background:#0F172A;border:1px solid #334155;border-radius:12px;'
            'padding:1rem 1.2rem;margin-top:0.5rem;'
            'font-size:0.78rem;color:#94A3B8;line-height:1.65;'
            'box-shadow:0 4px 20px rgba(0,0,0,0.5)">'
            '<b style="color:#F1F5F9;font-size:0.82rem">📊 ¿Qué muestra este gráfico?</b>'
            '<br><br>Evolución paralela del <b style="color:#60A5FA">Talento STEM</b> '
            '(eje izquierdo) y el <b style="color:#FBBF24">Empleo en Energía</b> '
            '(eje derecho) durante los 6 semestres 2022-2024. El área azul refleja '
            'el crecimiento de matrículas universitarias; la línea dorada muestra '
            'la absorción laboral en el sector eléctrico colombiano. Su sincronía '
            'evidencia la coevolución cuantificada por el modelo OLS.</div>'
            '</details></div>',
            unsafe_allow_html=True,
        )

    st.markdown(insight(
        "¿Qué nos dice el gráfico?",
        f"La serie histórica de 6 semestres (2022-2024) muestra la evolución paralela del talento STEM "
        f"y el empleo energético. El modelo OLS cuantifica esta coevolución con "
        f"<b>r = {modelo['r']:.4f}</b> y <b>R² = {modelo['r2']:.4f}</b> — ver pestaña Modelo.",
    ), unsafe_allow_html=True)

    st.markdown('<div style="height:2rem"></div>', unsafe_allow_html=True)

    with st.expander("🔍 Ver tabla de datos completa"):
        st.markdown(
            '<p style="font-size:0.8rem;color:#94A3B8;margin:0">'
            'Serie histórica semestral con los cuatro indicadores cruzados del modelo: '
            'porcentaje de energía limpia (XM), estudiantes STEM matriculados (SNIES), '
            'empleo formal en el sector energético y tasa de desempleo nacional (DANE-GEIH).</p>'
            '<div style="height:1rem"></div>',
            unsafe_allow_html=True,
        )
        st.dataframe(df_coev.rename(columns={
            "year": "Año", "semester": "Semestre",
            "porcentaje_energia_limpia": "% Energía Limpia",
            "total_talento_stem": "Talento STEM",
            "empleo_energia_miles": "Empleo Energía (K)",
            "tasa_desempleo_pais": "Tasa Desempleo %",
        }), use_container_width=True, hide_index=True)

    with st.expander("🔧 Diagnóstico: tipos de energía en la BD"):
        st.markdown(
            '<p style="font-size:0.8rem;color:#94A3B8;margin:0">'
            'Fuentes de generación eléctrica registradas por XM S.A. E.S.P. en el Mercado de Energía '
            'Mayorista de Colombia. Cada fila corresponde a un tipo de recurso con su volumen total '
            'generado en el periodo 2022-2024, expresado en gigavatios-hora (GWh).</p>'
            '<div style="height:1rem"></div>',
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
                tipos   = df_diag["resource_type"].str.upper().tolist()
                limpios = [t for t in tipos if any(
                    k in t for k in ["HIDRAUL", "SOLAR", "EOLIC", "MENORES",
                                     "BIOMASA", "BAGAZO", "GEOTERM", "RENOVABLE"]
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
