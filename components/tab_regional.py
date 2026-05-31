"""
components/tab_regional.py
───────────────────────────
Tab 2 — Brechas Regionales.
"""

import unicodedata
import streamlit as st

from queries.analytics import get_distribucion_regional
from utils.ui import alert, insight, divider, skeleton
from utils.charts import C, REGION_COLORS, chart_mapa_colombia, chart_distribucion_regional


def _norm_dept(name: str) -> str:
    nfkd = unicodedata.normalize("NFKD", str(name).upper().strip())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def _section_header(titulo: str, subtitulo: str = "") -> None:
    sub = (
        f'<p style="font-size:0.78rem;color:#475569;margin:0.15rem 0 0">{subtitulo}</p>'
        if subtitulo else ""
    )
    st.markdown(
        f'<div style="margin:1.5rem 0 0.6rem">'
        f'<p style="font-size:0.62rem;font-weight:700;text-transform:uppercase;'
        f'letter-spacing:0.14em;color:#334155;margin:0">━━ {titulo}</p>'
        f'{sub}</div>',
        unsafe_allow_html=True,
    )


def render_tab_regional(df_coev, df_mapa, pct_andina: float, pct_caribe: float) -> None:

    # ── Encabezado ────────────────────────────────────────────────────────────
    st.markdown(
        '<h3 style="font-size:1.1rem;font-weight:700;color:#F1F5F9;margin-bottom:0.15rem">'
        '🗺️ Radiografía Geográfica del Talento STEM — 2022-2024</h3>'
        '<p style="font-size:0.82rem;color:#64748B;margin-top:0">'
        'Análisis territorial de dónde se forma el capital humano STEM y si coincide '
        'con las zonas de mayor demanda y potencial energético en Colombia.</p>',
        unsafe_allow_html=True,
    )

    # Lookup: dept_norm → info del departamento
    dept_to_region: dict[str, str] = {}
    dept_to_info:   dict[str, dict] = {}
    for _, row in df_mapa.iterrows():
        norm = _norm_dept(row["departamento"])
        dept_to_region[norm] = row["macro_region"]
        dept_to_info[norm] = {
            "departamento": row["departamento"],
            "macro_region": row["macro_region"],
            "total_stem":   int(row["total_stem"]),
        }

    # ══ LAYOUT: mapa izquierda · alerta+contexto derecha ════════════════════
    col_map, col_right = st.columns([6, 5], gap="large")

    evento_mapa = None
    with col_map:
        _ph_mapa = st.empty()
        _ph_mapa.markdown(skeleton(420), unsafe_allow_html=True)
        fig_mapa = chart_mapa_colombia(df_mapa, height=420, show_title=False)
        if fig_mapa is not None:
            evento_mapa = _ph_mapa.plotly_chart(
                fig_mapa,
                use_container_width=True,
                on_select="rerun",
                selection_mode="points",
                key="mapa_brechas",
            )
        else:
            _ph_mapa.info("⚠️ Sin conexión — mapa no disponible.")

    # Detectar departamento y región clicados en el mapa
    _region_click = None
    _dept_click:  dict = {}
    if evento_mapa:
        _puntos = evento_mapa.get("selection", {}).get("points", [])
        if _puntos:
            _loc = _puntos[0].get("location", "")
            _region_click = dept_to_region.get(_loc)
            _dept_click   = dept_to_info.get(_loc, {})

    _contextos_right = {
        "Andina":    ("insight", "Epicentro del talento STEM",
                      "Alta densidad de IES. Requiere estrategias de movilidad hacia regiones con demanda energética real."),
        "Caribe":    ("alert",   "Brecha estructural urgente",
                      "Alta demanda eólica y solar en La Guajira y Cesar, pero baja oferta local de ingenieros."),
        "Pacífica":  ("alert",   "Déficit de ingeniería eléctrica",
                      "Alto potencial hídrico sin aprovechar por falta de ingenieros locales en la región."),
        "Orinoquía": ("alert",   "Baja densidad de formación STEM",
                      "Región en crecimiento energético pero con escasa oferta universitaria STEM para atender la demanda."),
        "Amazonía":  ("alert",   "En consolidación — cobertura insuficiente",
                      "La formación STEM aún no cubre las necesidades de energía renovable aislada en la región."),
        "Insular":   ("alert",   "Alta dependencia de diésel",
                      "Potencial solar y eólico sin explotar por falta de ingenieros y programas STEM en el archipiélago."),
    }

    with col_right:
        st.markdown(
            '<div style="background:#0F172A;border:1px solid #1E293B;border-radius:12px;'
            'padding:1rem 1.4rem;margin:0 0 0.8rem">'
            '<p style="font-size:0.8rem;color:#94A3B8;line-height:1.7;margin:0">'
            'Colombia concentra su formación universitaria STEM en el interior del país mientras '
            'que los grandes proyectos de energía renovable —parques eólicos en La Guajira y granjas '
            'solares en el Cesar— se desarrollan en regiones con escasa oferta local de ingenieros. '
            'Esta pestaña cuantifica esa brecha y permite explorarla por región y periodo.</p>'
            '</div>',
            unsafe_allow_html=True,
        )
        # Card dinámica: cambia según el departamento clicado en el mapa
        if _region_click and _dept_click:
            _dept_nombre = _dept_click.get("departamento", _region_click)
            _dept_stem   = _dept_click.get("total_stem", 0)
            for key, (tipo, titulo, cuerpo) in _contextos_right.items():
                if key in _region_click:
                    _color_card = "#4ADE80" if tipo == "insight" else "#F87171"
                    _bg_card    = "#052e16" if tipo == "insight" else "#1a0a0a"
                    _border_col = "#166534" if tipo == "insight" else "#7f1d1d"
                    _icon       = "✅" if tipo == "insight" else "🚨"
                    st.markdown(
                        f'<div style="background:{_bg_card};border:1px solid {_border_col};'
                        f'border-left:5px solid {_color_card};border-radius:14px;'
                        f'padding:1.2rem 1.5rem;margin:0.8rem 0">'
                        f'<div style="font-size:1.15rem;font-weight:800;color:{_color_card};margin-bottom:0.1rem">'
                        f'{_dept_nombre}</div>'
                        f'<div style="font-size:0.78rem;color:#94A3B8;margin-bottom:0.8rem">{_region_click}</div>'
                        f'<div style="background:rgba(255,255,255,0.04);border-radius:10px;'
                        f'padding:0.6rem 0.9rem;margin-bottom:0.8rem;display:flex;'
                        f'align-items:center;gap:0.7rem">'
                        f'<div style="font-size:1.3rem;font-weight:800;color:{_color_card}">'
                        f'{_dept_stem:,}</div>'
                        f'<div style="font-size:0.65rem;color:#64748B;text-transform:uppercase;font-weight:600">'
                        f'estudiantes STEM<br>matriculados</div>'
                        f'</div>'
                        f'<div style="font-size:0.7rem;font-weight:700;color:{_color_card};margin-bottom:0.2rem">'
                        f'{_icon} {titulo}</div>'
                        f'<div style="font-size:0.75rem;color:#94A3B8;line-height:1.6">{cuerpo}</div>'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
                    break
        else:
            st.markdown(alert(
                "Brecha Territorial Crítica",
                f"La <b>Región Andina concentra el {pct_andina:.2f}%</b> del talento STEM, mientras la "
                f"<b>Región Caribe apenas alcanza el {pct_caribe:.2f}%</b>. Los parques eólicos de La Guajira "
                f"y las granjas solares de Cesar se construyen donde menos ingenieros se forman.",
            ), unsafe_allow_html=True)

    # ── Filtro de periodo ─────────────────────────────────────────────────────
    _section_header(
        "FILTRO DE PERIODO",
        "Selecciona un año y semestre específico para ver la distribución de ese periodo.",
    )
    periodos = [
        (int(r["year"]), int(r["semester"]))
        for _, r in df_coev.iterrows()
    ]
    opciones = {
        f"{y} · Semestre {s}  {'(Ene – Jun)' if s == 1 else '(Jul – Dic)'}": (y, s)
        for y, s in periodos
    }
    periodo_sel = st.selectbox(
        "Periodo académico:",
        list(opciones.keys()),
        index=len(opciones) - 1,
        key="t2_periodo",
    )
    year_sel, sem_sel = opciones[periodo_sel]
    df_reg = get_distribucion_regional(year_sel, sem_sel)

    # ══ DONA + DETALLE (ancho completo, debajo del mapa) ═════════════════════
    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
    col_dona, col_det = st.columns([1, 1], gap="large")

    with col_dona:
        st.markdown(
            '<p style="font-size:0.62rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:0.14em;color:#334155;margin:0 0 0.5rem">📊 ANÁLISIS POR REGIÓN</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p style="font-size:0.75rem;font-weight:600;color:#64748B;margin-bottom:0.2rem">'
            f'Participación % · {year_sel} Sem. {sem_sel}</p>',
            unsafe_allow_html=True,
        )
        if not df_reg.empty:
            _ph_dona = st.empty()
            _ph_dona.markdown(skeleton(340), unsafe_allow_html=True)
            _ph_dona.plotly_chart(chart_distribucion_regional(df_reg), use_container_width=True)

    with col_det:
        st.markdown(
            '<p style="font-size:0.75rem;font-weight:600;color:#64748B;margin-bottom:0.2rem">'
            '🔎 Detalle por región</p>',
            unsafe_allow_html=True,
        )
        if not df_reg.empty:
            reg_sel = st.selectbox(
                "Región:",
                df_reg["macro_region"].dropna().unique().tolist(),
                key="t2_reg",
            )
            fila_r  = df_reg[df_reg["macro_region"] == reg_sel].iloc[0]
            color_r = REGION_COLORS.get(reg_sel, C["teal"])

            st.markdown(
                f'<div style="background:#0F172A;border-radius:14px;padding:1.2rem;'
                f'border-left:5px solid {color_r};box-shadow:0 4px 20px rgba(0,0,0,0.4);margin-top:0.4rem">'
                f'<div style="font-size:0.62rem;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#475569">Macro-Región</div>'
                f'<div style="font-size:1rem;font-weight:800;color:{color_r};margin:0.2rem 0 0.8rem">{reg_sel}</div>'
                f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.6rem">'
                f'<div style="background:#1E293B;border-radius:10px;padding:0.7rem;text-align:center">'
                f'<div style="font-size:1.4rem;font-weight:800;color:#F1F5F9">{int(fila_r["cantidad_departamentos"])}</div>'
                f'<div style="font-size:0.6rem;color:#64748B;text-transform:uppercase;font-weight:600;margin-top:0.15rem">Departamentos</div></div>'
                f'<div style="background:#1E293B;border-radius:10px;padding:0.7rem;text-align:center">'
                f'<div style="font-size:1.4rem;font-weight:800;color:{color_r}">{float(fila_r["porcentaje_participacion_talento"]):.1f}%</div>'
                f'<div style="font-size:0.6rem;color:#64748B;text-transform:uppercase;font-weight:600;margin-top:0.15rem">Participación</div></div></div>'
                f'<div style="margin-top:0.8rem;padding-top:0.7rem;border-top:1px solid #1E293B;'
                f'font-size:0.78rem;color:#94A3B8;font-weight:600">'
                f'🎓 {int(fila_r["estudiantes_matriculados"]):,} estudiantes</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

            contextos = {
                "Andina":    ("insight", "Epicentro del talento STEM.",
                              "Alta densidad de IES. Requiere estrategias de movilidad hacia regiones con demanda energética real."),
                "Caribe":    ("alert",   "Brecha estructural urgente.",
                              "Alta demanda eólica y solar en La Guajira y Cesar, pero baja oferta local de ingenieros."),
                "Pacífica":  ("insight", "Potencial hídrico elevado.",
                              "Déficit de ingeniería eléctrica para aprovechar los recursos del litoral."),
                "Orinoquía": ("insight", "Llanura en expansión.",
                              "Región en crecimiento energético con baja densidad de formación STEM."),
                "Amazonía":  ("insight", "En consolidación.",
                              "Énfasis en sostenibilidad y energía renovable aislada."),
                "Insular":   ("insight", "Archipiélago estratégico.",
                              "Alta dependencia diésel; potencial solar y eólico sin explotar."),
            }
            st.markdown('<div style="height:0.4rem"></div>', unsafe_allow_html=True)
            for key, (tipo, titulo, cuerpo) in contextos.items():
                if key in reg_sel:
                    fn = insight if tipo == "insight" else alert
                    st.markdown(fn(titulo, cuerpo), unsafe_allow_html=True)
                    break

    # ── Tabla ─────────────────────────────────────────────────────────────────
    st.markdown('<div style="height:0.5rem"></div>', unsafe_allow_html=True)
    with st.expander("📊 Ver tabla regional completa"):
        st.markdown(
            '<p style="font-size:0.8rem;color:#94A3B8;margin:0">'
            f'Distribución del talento STEM por macro-región · '
            f'<b style="color:#F1F5F9">{year_sel} · Semestre {sem_sel}</b>. '
            'Incluye número de departamentos, estudiantes matriculados y participación porcentual.</p>'
            '<div style="height:1rem"></div>',
            unsafe_allow_html=True,
        )
        st.dataframe(df_reg.rename(columns={
            "macro_region":                    "Macro-Región",
            "cantidad_departamentos":          "Departamentos",
            "estudiantes_matriculados":        "Estudiantes STEM",
            "porcentaje_participacion_talento": "Participación %",
        }), use_container_width=True, hide_index=True)
