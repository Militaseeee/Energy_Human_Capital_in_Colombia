"""
db/connection.py
────────────────
Motor SQLAlchemy singleton para Supabase (pgbouncer, puerto 6543).

Decisiones de ingeniería:
  • @st.cache_resource  → cachea el objeto Engine entre reruns sin serializarlo
                          (cache_data no sirve aquí; los Engine no son picklables).
  • NullPool            → cierra la conexión después de cada uso; evita leaks con
                          pgbouncer en modo "transaction pooling" de Supabase.
  • sslmode=require     → conexión cifrada obligatoria con el servidor remoto.
  • Las credenciales se leen SOLO desde .streamlit/secrets.toml (nunca hardcodeadas).
"""

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.pool import NullPool
import streamlit as st


@st.cache_resource(show_spinner="🔌 Conectando con Supabase…")
def get_engine():
    """
    Crea y cachea un único motor SQLAlchemy para toda la sesión de la app.
    Llama a esta función en cualquier módulo; solo se instancia una vez.
    """
    cfg = st.secrets["postgresql"]

    connection_url = URL.create(
        drivername="postgresql+psycopg2",
        username=cfg["DB_USER"],
        password=cfg["DB_PASSWORD"],
        host=cfg["DB_HOST"],
        port=int(cfg["DB_PORT"]),
        database=cfg["DB_NAME"],
        query={"sslmode": "require"},
    )

    engine = create_engine(connection_url, poolclass=NullPool)

    # Prueba de conectividad al iniciar — falla rápido si hay un error de credenciales
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    return engine
