"""
components/hero.py
──────────────────
Sección hero: título + leyenda (izq) · KPIs + mapa + alerta (der).
"""

import streamlit as st
import streamlit.components.v1 as st_components

from utils.ui import gradient_divider, skeleton
from utils.charts import C, REGION_COLORS, chart_mapa_colombia


def render_hero(df_mapa, s1, s2, modelo, pct_andina: float, pct_caribe: float,
                s1_label: str, s2_label: str) -> None:

    col_left, col_right = st.columns([1, 1.5], gap="large")

    # ── Columna izquierda: título + leyenda ───────────────────────────────────
    with col_left:
        _leg_items = [
            (REGION_COLORS["Región Andina"],    "Región Andina",    f"{pct_andina:.2f}% del talento STEM"),
            (REGION_COLORS["Región Caribe"],    "Región Caribe",    f"{pct_caribe:.2f}% — brecha crítica"),
            (REGION_COLORS["Región Pacífica"],  "Región Pacífica",  "Potencial hídrico"),
            (REGION_COLORS["Región Orinoquía"], "Región Orinoquía", "Llanura en crecimiento"),
            (REGION_COLORS["Región Amazonía"],  "Región Amazonía",  "En consolidación"),
            (REGION_COLORS["Región Insular"],   "Región Insular",   "Potencial solar/eólico"),
        ]
        _leg_html = "".join(
            f'<div style="display:flex;align-items:center;gap:0.55rem;margin-bottom:0.42rem">'
            f'<div style="width:9px;height:9px;border-radius:50%;background:{clr};'
            f'box-shadow:0 0 8px {clr}88;flex-shrink:0"></div>'
            f'<span style="font-size:0.8rem;font-weight:700;color:#CBD5E1">{nombre}</span>'
            f'<span style="font-size:0.72rem;color:#475569"> — {desc}</span>'
            f'</div>'
            for clr, nombre, desc in _leg_items
        )
        st.markdown(
            '<div style="background:radial-gradient(ellipse at 10% 50%,'
            'rgba(34,211,238,0.12) 0%,transparent 65%);padding:0.5rem 0 1rem 0">'
            '<div style="font-size:0.62rem;font-weight:700;text-transform:uppercase;'
            'letter-spacing:0.2em;color:#334155">'
            '🇨🇴 &nbsp;Minería de Datos &nbsp;·&nbsp; Serie Histórica 2022-2024</div>'
            '<h1 style="font-size:2.75rem;font-weight:900;line-height:1.1;'
            'letter-spacing:-0.03em;margin:0 0 0.75rem 0;'
            'background:linear-gradient(140deg,#FFFFFF 0%,#E2E8F0 22%,'
            '#22D3EE 62%,#60A5FA 100%);'
            '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
            'background-clip:text">'
            'Coevolución del Capital Humano STEM y el Sector Energético</h1>'
            '<p style="color:#64748B;font-size:0.83rem;line-height:1.65;margin:0 0 0.3rem">'
            'Sincronía entre la formación universitaria STEM y la absorción '
            'laboral en el sector eléctrico colombiano.</p>'
            '<span style="font-size:0.67rem;color:#334155">'
            'SNIES &nbsp;·&nbsp; XM S.A. E.S.P. &nbsp;·&nbsp; '
            'DANE–GEIH &nbsp;·&nbsp; Banco Mundial</span>'
            '</div>'
            '<div style="height:1px;background:linear-gradient(to right,'
            '#1E293B,#22D3EE44,#1E293B);margin:1.5rem 0 1.1rem"></div>'
            '<div style="margin-bottom:0.5rem">'
            '<div style="font-size:1.1rem;font-weight:700;color:#22D3EE;margin-top:2rem;margin-bottom:1rem">'
            '🗺️ ¿Qué muestra el mapa?</div>'
            '<div style="font-size:0.77rem;color:#64748B;line-height:1.6;margin-bottom:2rem">'
            'Cada departamento está coloreado según su macro-región natural. '
            'El color refleja la concentración del talento STEM universitario '
            'en el territorio colombiano.</div>'
            '</div>'
            f'<div data-hero-legend>{_leg_html}</div>',
            unsafe_allow_html=True,
        )

    # ── Columna derecha: KPIs + mapa + alerta ────────────────────────────────
    with col_right:
        kr1, kr2, kr3, kr4 = st.columns(4, gap="small")
        with kr1:
            val_stem   = int(s1["total_talento_stem"]) if s1 is not None else 0
            delta_stem = (int(s2["total_talento_stem"]) - int(s1["total_talento_stem"])
                          if s2 is not None and s1 is not None else None)
            st.metric("🎓 Talento STEM", f"{val_stem:,}",
                      f"{delta_stem:+,} {s2_label}" if delta_stem is not None else s1_label)
        with kr2:
            val_emp   = float(s1["empleo_energia_miles"]) if s1 is not None else 0
            delta_emp = (float(s2["empleo_energia_miles"]) - float(s1["empleo_energia_miles"])
                         if s2 is not None and s1 is not None else None)
            st.metric("⚡ Empleo Energía", f"{val_emp:.1f} K",
                      f"{delta_emp:+.2f} K {s2_label}" if delta_emp is not None else "Miles")
        with kr3:
            val_enl   = float(s1["porcentaje_energia_limpia"]) if s1 is not None else 0
            delta_enl = (float(s2["porcentaje_energia_limpia"]) - float(s1["porcentaje_energia_limpia"])
                         if s2 is not None and s1 is not None else None)
            st.metric("🌿 Energía Limpia", f"{val_enl:.2f}%",
                      f"{delta_enl:+.2f}% {s2_label}" if delta_enl is not None else s1_label)
        with kr4:
            st.metric("🔗 Correlación r", f"{modelo['r']:.4f}",
                      "Sincronía Perfecta", delta_color="normal")

        st.markdown('<div style="margin-top:0.35rem"></div>', unsafe_allow_html=True)
        _ph_hero = st.empty()
        _ph_hero.markdown(skeleton(450), unsafe_allow_html=True)
        fig_hero = chart_mapa_colombia(df_mapa, height=450, show_title=False)
        if fig_hero is not None:
            _ph_hero.plotly_chart(fig_hero, use_container_width=True)
        else:
            _ph_hero.markdown(
                '<div style="background:#0F172A;border:1px dashed #334155;'
                'border-radius:16px;padding:3rem;text-align:center;color:#475569">'
                '🗺️ Mapa no disponible sin conexión a internet</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<div data-hero-alert style="background:#1a0a0a;border-width:1px 1px 1px 4px;'
            'border-style:solid;border-color:#7F1D1D #7F1D1D #7F1D1D #F87171;'
            'border-radius:10px;padding:0.6rem 1rem;margin-top:0.1rem">'
            '<span style="font-weight:700;color:#FCA5A5;font-size:0.82rem">'
            '🚨 Brecha Territorial — </span>'
            f'<span style="color:#FCA5A5;font-size:0.79rem">'
            f'La <b>Región Andina</b> concentra el <b>{pct_andina:.2f}%</b> del talento '
            f'mientras parques eólicos y solares se construyen en el '
            f'<b>Caribe ({pct_caribe:.2f}%)</b>.</span></div>',
            unsafe_allow_html=True,
        )

    gradient_divider()

    # ── JS: alinea leyenda con el fondo del alert card ────────────────────────
    st_components.html("""
<script>
(function () {
    var doc = window.parent.document;
    function align() {
        var alertEl  = doc.querySelector('[data-hero-alert]');
        var legendEl = doc.querySelector('[data-hero-legend]');
        if (!alertEl || !legendEl) return;
        legendEl.style.marginTop = '0px';
        requestAnimationFrame(function () {
            var gap = alertEl.getBoundingClientRect().bottom
                    - legendEl.getBoundingClientRect().bottom;
            if (gap > 2) legendEl.style.marginTop = Math.round(gap) + 'px';
        });
    }
    setTimeout(align, 400);
    setTimeout(align, 1100);
    var t;
    window.parent.addEventListener('resize', function () {
        clearTimeout(t);
        t = setTimeout(align, 250);
    });
})();
</script>
""", height=0)
