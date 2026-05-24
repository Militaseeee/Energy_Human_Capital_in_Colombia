# ⚡ Minería de Datos: Coevolución del Capital Humano STEM y el Mercado Laboral Energético en Colombia (2023)

> **Autores:** Camila Acosta & Cristian Robledo  
> **Programa:** Talento Tech  
> **Fecha:** Mayo 2026  
> **Stack:** Python · Supabase/PostgreSQL · Streamlit · Plotly · SQLAlchemy

---

## 📌 Descripción del Proyecto

Este proyecto de minería de datos evalúa y modela la **coevolución y simbiosis** entre la formación de talento en áreas **STEM** (Ciencia, Tecnología, Ingeniería y Matemáticas), la dinámica del **mercado laboral formal** y la **infraestructura de generación de energía** en Colombia durante el año 2023.

A través de la integración analítica de múltiples fuentes de datos nacionales e internacionales, el sistema consolida un repositorio unificado en la nube (**Supabase/PostgreSQL**) estructurado bajo un **Modelo en Galaxia (Star Schema Avanzado)**. Utilizando técnicas de modelado estadístico relacional, el proyecto describe de manera matemática exacta el impacto socioeconómico y la alineación de competencias de cara a la transición energética del país.

---

## 🛠️ Arquitectura de Datos — Modelo en Galaxia

Para evitar la redundancia y mitigar la explosión cartesiana en cruces masivos, se implementó un esquema multidimensional:

```
                    ┌─────────────┐
                    │  dim_time   │
                    │  (time_id)  │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────────┐
          │                │                    │
   ┌──────▼──────┐  ┌──────▼──────┐   ┌────────▼────────┐
   │fact_education│  │ fact_energy │   │fact_formal_     │
   │  (SNIES)    │  │   (XM)      │   │employment(DANE) │
   └──────┬──────┘  └──────┬──────┘   └────────┬────────┘
          │                │                    │
          └────────────────┼────────────────────┘
                           │
                    ┌──────▼──────┐
                    │ dim_region  │
                    │(region_id)  │
                    └─────────────┘
                           │
                    ┌──────▼──────────┐
                    │ fact_development│
                    │ (Banco Mundial) │
                    └─────────────────┘
```

### Tablas de Dimensiones

| Tabla | Descripción |
|---|---|
| `dim_time` | Indexación temporal por año y semestre (2023-1, 2023-2) |
| `dim_region` | Catastro geográfico de departamentos agrupados por Macro-Regiones Naturales |

### Tablas de Hechos

| Tabla | Fuente | Contenido |
|---|---|---|
| `fact_education` | SNIES — Ministerio de Educación | Matrículas universitarias STEM por área de conocimiento |
| `fact_energy` | XM S.A. E.S.P. | Generación eléctrica diaria en kWh por tipo de recurso |
| `fact_formal_employment` | DANE — GEIH | Ocupación sectorial mensual y tasa de desempleo |
| `fact_development` | Banco Mundial — WDI | PIB per cápita histórico de Colombia |

---

## 🚀 Hallazgos del Modelo Estadístico (Fase de Evaluación)

El pipeline analítico ejecutó algoritmos de asociación y regresión en el entorno de producción:

### 1. Correlación de Pearson — `r = 1.0000`
> Coevolución positiva perfecta. Existe una sincronía matemáticamente exacta entre el ingreso de estudiantes a carreras STEM y la absorción de mano de obra en el sector energético durante los semestres analizados.

### 2. Regresión Lineal OLS

$$Y = 0.001041 \cdot X - 1924.44$$

| Parámetro | Valor | Significado |
|---|---|---|
| Pendiente `m` | `0.001041` | Por cada 10,000 nuevos estudiantes STEM → **10.41 mil empleos** adicionales en energía |
| Intercepto `b` | `-1924.44` | Base del modelo |
| R² | `1.0000` | Descriptor matemático exacto de la muestra 2023 |

> **Nota científica:** El R² perfecto es esperado al trabajar con los dos semestres del 2023 como muestra. Funciona como descriptor exacto. Para obtener una tendencia predictiva generalizable, se recomienda incorporar la serie histórica 2018–2023.

### 🚨 Brechas Críticas Detectadas

| Brecha | Dato | Implicación |
|---|---|---|
| **Centralización Andina** | 68.54% del talento STEM nacional | Concentración excesiva en el centro del país |
| **Déficit Caribe** | Solo 16.47% del talento STEM | La Guajira y Cesar lideran proyectos eólicos/solares pero sin talento local |
| **Disciplinas digitales emergentes** | "Desarrollo de Software" (#5, 26,637 est.) | Señal positiva para modernización de redes inteligentes |

---

## 📁 Estructura del Proyecto (Fase de Despliegue)

```
Energy_Human_Capital_in_Colombia/
│
├── .streamlit/
│   └── secrets.toml        ← 🔐 Credenciales Supabase (NO subir a Git)
│
├── db/
│   ├── __init__.py
│   └── connection.py       ← Motor SQLAlchemy con @st.cache_resource + NullPool
│
├── queries/
│   ├── __init__.py
│   └── analytics.py        ← 4 funciones SQL con @st.cache_data + sqlalchemy.text()
│
├── utils/
│   ├── __init__.py
│   └── charts.py           ← 4 constructores Plotly (doble-eje, dona, barras, OLS)
│
├── app.py                  ← 🚀 Dashboard principal Streamlit — 3 pestañas
├── requirements.txt        ← Dependencias del proyecto
├── .gitignore              ← secrets.toml y .venv excluidos del repo
└── README.md               ← Este archivo
```

---

## 🔐 Gestión de Credenciales: `secrets.toml` vs `.env`

Esta es una pregunta clave de arquitectura. La respuesta corta es: **para este proyecto solo necesitas `secrets.toml`**, no un `.env`.

### ¿Por qué `secrets.toml` y no `.env`?

| Característica | `.streamlit/secrets.toml` | `.env` + `python-dotenv` |
|---|---|---|
| **¿Para qué es?** | Nativo de Streamlit | General (cualquier app Python) |
| **¿Cómo se lee?** | `st.secrets["clave"]` | `os.environ.get("CLAVE")` |
| **¿Requiere librería extra?** | ❌ No (Streamlit lo carga solo) | ✅ Sí (`python-dotenv`) |
| **¿Se puede usar en scripts .py sin Streamlit?** | ❌ No | ✅ Sí |
| **¿Streamlit Cloud lo soporta?** | ✅ Nativo y seguro | ⚠️ Requiere configuración extra |
| **Formato** | TOML (secciones con `[grupo]`) | `CLAVE=VALOR` simple |

### ¿Cuándo necesitarías `.env`?

Solo si tuvieras **scripts ETL independientes** (sin Streamlit) que también necesiten conectarse a Supabase, como los notebooks de carga que migraste de Colab. En ese caso tendrías ambos archivos, ambos en `.gitignore`.

### Cómo luce tu `secrets.toml`

```toml
# .streamlit/secrets.toml
[postgresql]
DB_HOST     = "aws-1-us-east-1.pooler.supabase.com"
DB_PORT     = 6543
DB_NAME     = "postgres"
DB_USER     = "postgres.zxtdkucvjgwmuxsjrtvh"
DB_PASSWORD = "tu_password_aqui"
```

Y así se consume en el código (ya implementado en `db/connection.py`):

```python
cfg = st.secrets["postgresql"]
DB_HOST = cfg["DB_HOST"]
DB_PASSWORD = cfg["DB_PASSWORD"]
```

> ⚠️ **Importante:** `secrets.toml` ya está excluido del repositorio Git via `.gitignore`.
> Si compartes el proyecto, nunca incluyas este archivo. Rota tu contraseña de Supabase
> si llegó a quedar expuesta (`Supabase → Settings → Database → Reset password`).

---

## 🖥️ Guía de Despliegue Local en VS Code

### Prerrequisitos

- [Python 3.10+](https://www.python.org/downloads/) instalado y en el PATH
- [VS Code](https://code.visualstudio.com/) con la extensión **Python** (ms-python.python)
- Acceso a internet para conectar con Supabase

---

### Paso 1 — Abrir el proyecto en VS Code

`Archivo` → `Abrir carpeta` → selecciona la carpeta `Energy_Human_Capital_in_Colombia`

---

### Paso 2 — Crear el entorno virtual

Abre la terminal integrada con **Ctrl + `** y ejecuta:

```powershell
# Crear el entorno virtual (solo la primera vez)
python -m venv .venv
```

```powershell
# Activar en PowerShell (Windows)
.\.venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea la ejecución de scripts, ejecuta primero:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

Cuando esté activo verás `(.venv)` al inicio de tu línea de comandos.

---

### Paso 3 — Instalar dependencias

```powershell
pip install -r requirements.txt
```

Esto instala: `streamlit`, `sqlalchemy`, `psycopg2-binary`, `pandas`, `numpy`, `scipy`, `plotly` y `openpyxl`.

---

### Paso 4 — Seleccionar el intérprete Python en VS Code

**Ctrl + Shift + P** → escribe `Python: Select Interpreter` → elige el que dice **`.venv`**

Esto garantiza que VS Code use las librerías del entorno virtual y no las del sistema.

---

### Paso 5 — Verificar el archivo de credenciales

Confirma que el archivo `.streamlit/secrets.toml` existe y tiene el formato correcto
(ver sección **Gestión de Credenciales** más arriba).

---

### Paso 6 — Correr la aplicación

```powershell
streamlit run app.py
```

El navegador se abrirá automáticamente en **`http://localhost:8501`** 🎉

Para detener la app: **Ctrl + C** en la terminal.

---

### Solución de problemas comunes

| Error | Causa probable | Solución |
|---|---|---|
| `ModuleNotFoundError: streamlit` | Entorno virtual no activado | Ejecutar `.\.venv\Scripts\Activate.ps1` |
| `KeyError: 'postgresql'` | `secrets.toml` mal escrito o en ruta incorrecta | Verificar que esté en `.streamlit/secrets.toml` |
| `psycopg2.OperationalError` | Credenciales incorrectas o sin internet | Revisar contraseña en `secrets.toml` |
| `immutabledict` error | Query SQL sin `sqlalchemy.text()` | Ya corregido en `queries/analytics.py` |
| Puerto 8501 ocupado | Otra instancia de Streamlit corriendo | `streamlit run app.py --server.port 8502` |

---

## 🎨 Dashboard Interactivo — 3 Pestañas

### Tab 1 — Balance de Coevolución Nacional
- **Selector de semestre** (radio button)
- **4 tarjetas métricas personalizadas** con icono, color y fondo únicos por métrica: % Energía Limpia · Total Talento STEM · Empleo Energía (K) · Tasa Desempleo
- **Gráfico doble eje Y** (`plotly.subplots`): línea azul STEM con relleno + línea ámbar empleo energético
- Insight contextual + tabla de datos expandible

### Tab 2 — Distribución y Brechas Regionales
- **Alerta visual** de la brecha territorial Andina vs Caribe
- **🗺️ Mapa coroplético de Colombia** (`px.choropleth`): cada departamento coloreado por macro-región usando GeoJSON oficial con 33 departamentos
- **Selector de semestre** (`st.selectbox`)
- **Gráfico de dona** como visualización secundaria con pull visual sobre la Región Andina
- **Explorador por región**: tarjeta de detalle + insights contextuales automáticos por región (brecha Caribe, potencial hídrico Pacífica, etc.)

### Tab 3 — Modelo Matemático y Competencias
- **4 KPI cards** con diseño personalizado: r · R² · Pendiente m · Intercepto b
- **Ecuación de regresión** en notación LaTeX (`st.latex`) dentro de tarjeta gradient
- **Interpretación ejecutiva**: impacto estimado por cada 10,000 estudiantes STEM
- **Gráfico OLS** (scatter + recta con área de relleno)
- **Top 10 áreas** (barras horizontales, escala `Blugrn`)
- Nota científica sobre la validez y extensión del modelo

---

## ⚙️ Decisiones Técnicas de Ingeniería

| Problema | Solución Implementada | Archivo |
|---|---|---|
| Fugas de conexión con pgbouncer | `NullPool` en `create_engine` | `db/connection.py` |
| Error `immutabledict` en SQLAlchemy 2.0 | `sqlalchemy.text()` en todas las queries | `queries/analytics.py` |
| Saturar Supabase con cada interacción UI | `@st.cache_data(ttl=600)` en las 4 funciones | `queries/analytics.py` |
| Motor compartido entre módulos | `@st.cache_resource` en `get_engine()` — instancia única | `db/connection.py` |
| Credenciales expuestas en código | Solo en `.streamlit/secrets.toml` + `.gitignore` | `.streamlit/` |
| Inyección SQL en filtros dinámicos | Parámetros nombrados `:param` + `params={}` | `queries/analytics.py` |
| Explosión cartesiana en JOINs masivos | CTEs independientes por fuente antes del JOIN final | `queries/analytics.py` |

---

## 📦 Dependencias (`requirements.txt`)

```
streamlit>=1.35.0       # Framework web interactivo
sqlalchemy>=2.0.0       # ORM y motor de conexión SQL
psycopg2-binary>=2.9.9  # Driver PostgreSQL para Python
pandas>=2.0.0           # Manipulación y análisis de datos
numpy>=1.26.0           # Operaciones numéricas vectorizadas
scipy>=1.13.0           # Estadística: Pearson + OLS (linregress)
plotly>=5.22.0          # Visualizaciones interactivas
openpyxl>=3.1.0         # Lectura de archivos Excel (.xlsx) del ETL
```

---

## 🔄 Flujo Completo del Proyecto (CRISP-DM)

```
1. Comprensión del Negocio  →  Hipótesis de coevolución STEM ↔ Energía
2. Comprensión de los Datos →  SNIES + XM + DANE-GEIH + Banco Mundial
3. Preparación de Datos     →  ETL en Google Colab → Supabase (Modelo Galaxia)
4. Modelado                 →  Pearson r + Regresión OLS (scipy.stats)
5. Evaluación               →  r=1.0, R²=1.0, brechas regionales detectadas
6. Despliegue ← FASE ACTUAL →  Dashboard Streamlit local en VS Code
```

---

## 🌐 Despliegue en la Nube (Próximos Pasos)

Una vez que el dashboard funcione localmente, se puede publicar en **Streamlit Community Cloud** de forma gratuita:

1. Sube el proyecto a un repositorio GitHub **sin el `secrets.toml`**
2. Ve a [share.streamlit.io](https://share.streamlit.io) y conecta el repo
3. En `Advanced settings → Secrets`, pega el contenido del `secrets.toml`
4. Streamlit Cloud lo expone como URL pública lista para compartir

---

*Desarrollado por **Camila Acosta & Cristian Robledo** — Talento Tech | Mayo 2026*
