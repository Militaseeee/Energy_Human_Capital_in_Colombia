"""
queries/analytics.py
─────────────────────
Todas las consultas SQL al modelo en Galaxia de Supabase.

Directrices técnicas aplicadas:
  • @st.cache_data(ttl=600) → cachea el DataFrame resultante 10 min; evita saturar
    Supabase con cada interacción del usuario con filtros o sliders.
  • sqlalchemy.text()        → empaqueta el string SQL como objeto TextClause;
    previene el error de tipo `immutabledict` con SQLAlchemy 2.0 + pandas.
  • Filtros ILIKE            → comparación insensible a mayúsculas/minúsculas
    para el sector económico del DANE.
  • Parámetros nombrados     → :param en el SQL + params={} en read_sql_query;
    previene inyección SQL y errores de formato.
"""

import pandas as pd
from scipy import stats
from sqlalchemy import text
import streamlit as st

from db.connection import get_engine


# ─────────────────────────────────────────────────────────────────────────────
# DIAGNÓSTICO — Ver qué valores reales hay en resource_type
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=600, show_spinner=False)
def get_resource_types_diagnostico() -> pd.DataFrame:
    """
    Retorna los valores únicos de resource_type en fact_energy con su
    volumen de generación acumulado. Útil para identificar el nombre
    exacto de los tipos renovables que cargó el ETL de XM.
    """
    sql = text("""
        SELECT
            resource_type,
            COUNT(*)                                    AS registros,
            ROUND(SUM(generation_kwh)::numeric / 1e9, 2) AS gwh_total
        FROM fact_energy
        GROUP BY resource_type
        ORDER BY gwh_total DESC;
    """)
    with get_engine().connect() as conn:
        return pd.read_sql_query(sql, conn)


@st.cache_data(ttl=600, show_spinner=False)
def get_time_alignment_diagnostico() -> dict:
    """
    Compara time_ids entre fact_energy y dim_time para detectar desalineaciones.
    Retorna muestras de IDs de cada tabla y el conteo de registros que coinciden.
    """
    sql_fe = text("SELECT DISTINCT time_id FROM fact_energy ORDER BY time_id LIMIT 8;")
    sql_dt = text(
        "SELECT time_id, year, semester FROM dim_time "
        "WHERE year IN (2022,2023,2024) ORDER BY time_id;"
    )
    sql_match = text("""
        SELECT COUNT(*) AS registros_coincidentes
        FROM fact_energy fe
        INNER JOIN dim_time t ON t.time_id = fe.time_id
        WHERE t.year IN (2022, 2023, 2024);
    """)
    with get_engine().connect() as conn:
        df_fe    = pd.read_sql_query(sql_fe,    conn)
        df_dt    = pd.read_sql_query(sql_dt,    conn)
        df_match = pd.read_sql_query(sql_match, conn)
    return {
        "fact_energy_ids":       df_fe,
        "dim_time_ids":          df_dt,
        "registros_coincidentes": int(df_match["registros_coincidentes"].iloc[0]),
    }


# ─────────────────────────────────────────────────────────────────────────────
# PESTAÑA 1 — Balance de Coevolución Nacional
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=600, show_spinner="⚡ Consultando Balance de Coevolución Nacional…")
def get_coevolucion_nacional() -> pd.DataFrame:
    """
    Métricas cruzadas 2022-2024 por semestre:
      - porcentaje_energia_limpia  (% global de generación renovable sobre total)
      - total_talento_stem         (matrículas universitarias STEM)
      - empleo_energia_miles       (ocupados sector electricidad/gas, en miles)
      - tasa_desempleo_pais        (tasa general de desocupación DANE)

    NOTA: el porcentaje de energía limpia se calcula sobre todos los registros de
    fact_energy (sin filtrar por time_id) porque el ETL de XM puede haber cargado
    datos con granularidad diaria cuyos time_id difieren de los semestrales de dim_time.
    """
    sql = text("""
        WITH data_energia AS (
            -- Porcentaje global de energía limpia — evita el mismatch de time_id
            -- entre fact_energy (posiblemente diario) y dim_time (semestral).
            SELECT
                ROUND(
                    SUM(CASE
                        WHEN resource_type ILIKE '%HIDRAUL%'
                          OR resource_type ILIKE '%SOLAR%'
                          OR resource_type ILIKE '%EOLIC%'
                          OR resource_type ILIKE '%MENORES%'
                          OR resource_type ILIKE '%BIOMASA%'
                          OR resource_type ILIKE '%BAGAZO%'
                          OR resource_type ILIKE '%GEOTERM%'
                          OR resource_type ILIKE '%RENOVABLE%'
                        THEN generation_kwh ELSE 0 END
                    )::numeric * 100
                    / NULLIF(SUM(generation_kwh)::numeric, 0),
                    2
                ) AS porcentaje_energia_limpia
            FROM fact_energy
        ),
        data_educacion AS (
            SELECT
                time_id,
                SUM(stem_enrolled) AS estudiantes_stem
            FROM fact_education
            GROUP BY time_id
        ),
        data_empleo AS (
            SELECT
                time_id,
                AVG(formal_employment_thousands) AS ocupados_sector_miles,
                AVG(unemployment_rate)           AS tasa_desempleo_general
            FROM fact_formal_employment
            WHERE economic_sector ILIKE '%Suministro de electricidad%'
               OR economic_sector ILIKE '%electricidad, gas%'
            GROUP BY time_id
        )
        SELECT
            t.year,
            t.semester,
            (SELECT porcentaje_energia_limpia FROM data_energia)              AS porcentaje_energia_limpia,
            COALESCE(ed.estudiantes_stem, 0)                                  AS total_talento_stem,
            ROUND(COALESCE(em.ocupados_sector_miles::numeric, 0), 2)          AS empleo_energia_miles,
            ROUND(COALESCE(em.tasa_desempleo_general::numeric, 0), 2)         AS tasa_desempleo_pais
        FROM dim_time t
        LEFT JOIN data_educacion ed ON ed.time_id = t.time_id
        LEFT JOIN data_empleo    em ON em.time_id = t.time_id
        WHERE t.year IN (2022, 2023, 2024)
        ORDER BY t.year, t.semester;
    """)
    with get_engine().connect() as conn:
        return pd.read_sql_query(sql, conn)


# ─────────────────────────────────────────────────────────────────────────────
# PESTAÑA 2 — Distribución y Brechas Regionales (macro-región)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=600, show_spinner="🗺️ Cargando Distribución Regional…")
def get_distribucion_regional(semester: int = 1) -> pd.DataFrame:
    """
    Participación porcentual del talento STEM por macro-región
    para el semestre indicado (1 o 2) del año 2023.
    """
    sql = text("""
        SELECT
            r.region_name                             AS macro_region,
            COUNT(DISTINCT r.departments)             AS cantidad_departamentos,
            SUM(ed.stem_enrolled)                     AS estudiantes_matriculados,
            ROUND(
                SUM(ed.stem_enrolled)::numeric
                / NULLIF(
                    (SELECT SUM(fe2.stem_enrolled)
                     FROM   fact_education fe2
                     INNER JOIN dim_time t2 ON t2.time_id = fe2.time_id
                     WHERE  t2.year IN (2022, 2023, 2024)
                       AND  t2.semester = :semester),
                    0
                ) * 100,
                2
            )                                         AS porcentaje_participacion_talento
        FROM dim_time t
        INNER JOIN fact_education ed ON ed.time_id = t.time_id
        INNER JOIN dim_region r      ON r.region_id = ed.region_id
        WHERE t.year IN (2022, 2023, 2024)
          AND t.semester = :semester
        GROUP BY r.region_name, ed.time_id
        ORDER BY estudiantes_matriculados DESC;
    """)
    with get_engine().connect() as conn:
        return pd.read_sql_query(sql, conn, params={"semester": semester})


@st.cache_data(ttl=600, show_spinner="🗺️ Cargando datos para mapa de Colombia…")
def get_mapa_colombia() -> pd.DataFrame:
    """
    Retorna datos a nivel de DEPARTAMENTO para el mapa coroplético.
    Trae el nombre del departamento, su macro-región y el total de
    estudiantes STEM matriculados en 2023 (ambos semestres).
    Excluye los registros del nodo 'Consolidado Nacional'.
    """
    sql = text("""
        SELECT
            r.departments                            AS departamento,
            r.region_name                            AS macro_region,
            COALESCE(SUM(ed.stem_enrolled), 0)       AS total_stem
        FROM dim_region r
        LEFT JOIN fact_education ed ON ed.region_id = r.region_id
        LEFT JOIN dim_time t        ON t.time_id = ed.time_id
            AND t.year IN (2022, 2023, 2024)
        WHERE r.region_name NOT ILIKE '%Consolidado%'
        GROUP BY r.departments, r.region_name
        ORDER BY total_stem DESC;
    """)
    with get_engine().connect() as conn:
        return pd.read_sql_query(sql, conn)


# ─────────────────────────────────────────────────────────────────────────────
# PESTAÑA 3 — Top 10 Áreas de Conocimiento
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=600, show_spinner="🏆 Cargando Top 10 Áreas de Conocimiento…")
def get_top_areas_conocimiento() -> pd.DataFrame:
    """
    Top 10 áreas de conocimiento STEM con mayor número de estudiantes
    matriculados en el año 2023 (ambos semestres consolidados).
    """
    sql = text("""
        SELECT
            ed.field_of_study                                      AS area_conocimiento,
            SUM(ed.stem_enrolled)                                  AS total_estudiantes,
            RANK() OVER (ORDER BY SUM(ed.stem_enrolled) DESC)      AS ranking_nacional
        FROM fact_education ed
        INNER JOIN dim_time t ON t.time_id = ed.time_id
        WHERE t.year IN (2022, 2023, 2024)
        GROUP BY ed.field_of_study
        ORDER BY total_estudiantes DESC
        LIMIT 10;
    """)
    with get_engine().connect() as conn:
        return pd.read_sql_query(sql, conn)


# ─────────────────────────────────────────────────────────────────────────────
# PESTAÑA 3 — Modelo Estadístico (Pearson + OLS)
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data(ttl=600, show_spinner="🧮 Ejecutando Modelo Estadístico Relacional…")
def get_modelo_estadistico() -> dict:
    """
    Aplica Correlación de Pearson y Regresión Lineal OLS sobre
    los dos semestres del 2023.

    Retorna dict con: df, r, r2, slope, intercept.
    """
    sql = text("""
        WITH data_educacion AS (
            SELECT time_id, SUM(stem_enrolled) AS talento_stem
            FROM fact_education
            GROUP BY time_id
        ),
        data_empleo AS (
            SELECT time_id, AVG(formal_employment_thousands) AS empleo_energia
            FROM fact_formal_employment
            WHERE economic_sector ILIKE '%Suministro de electricidad%'
               OR economic_sector ILIKE '%electricidad, gas%'
            GROUP BY time_id
        )
        SELECT
            t.semester,
            COALESCE(ed.talento_stem, 0)                                 AS talento_stem,
            ROUND(COALESCE(em.empleo_energia::numeric, 0), 2)            AS empleo_energia
        FROM dim_time t
        LEFT JOIN data_educacion ed ON ed.time_id = t.time_id
        LEFT JOIN data_empleo    em ON em.time_id = t.time_id
        WHERE t.year IN (2022, 2023, 2024)
        ORDER BY t.year, t.semester;
    """)
    with get_engine().connect() as conn:
        df = pd.read_sql_query(sql, conn)

    X = df["talento_stem"].values.astype(float)
    Y = df["empleo_energia"].values.astype(float)

    r, _                             = stats.pearsonr(X, Y)
    slope, intercept, r_value, _, _  = stats.linregress(X, Y)

    return {
        "df":        df,
        "r":         round(float(r), 4),
        "r2":        round(float(r_value ** 2), 4),
        "slope":     round(float(slope), 6),
        "intercept": round(float(intercept), 2),
    }
