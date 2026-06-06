# ⚡ Coevolución del Capital Humano STEM y el Sector Energético — Colombia 2022-2024

Dashboard ejecutivo interactivo que visualiza la sincronía entre la formación universitaria STEM y la absorción laboral en el sector eléctrico colombiano, construido con **Streamlit** y **Supabase**.

> **Autores:** Camila Acosta & Cristian Robledo · Talento Tech · Mayo 2026

---

## 📁 Estructura del Proyecto

```
Energy_Human_Capital_in_Colombia/
│
├── app.py                        ← Punto de entrada (orquestador)
│
├── components/                   ← Componentes visuales (frontend)
│   ├── __init__.py
│   ├── hero.py                   ← Sección principal: título, mapa y KPIs
│   ├── tab_coevolucion.py        ← Tab 1: Balance de Coevolución Nacional
│   ├── tab_regional.py           ← Tab 2: Brechas Regionales
│   └── tab_modelo.py             ← Tab 3: Modelo Estadístico (Pearson + OLS)
│
├── utils/                        ← Utilidades reutilizables
│   ├── ui.py                     ← CSS global y helpers HTML
│   └── charts.py                 ← Constructores de gráficos Plotly
│
├── queries/
│   └── analytics.py              ← Todas las consultas SQL a Supabase
│
├── db/
│   └── connection.py             ← Conexión al motor de base de datos
│
└── README.md
```

---

## 🗂️ Descripción de Archivos

### `app.py` — Punto de entrada
Orquestador mínimo del dashboard. Solo hace tres cosas:
1. Configura la página (`st.set_page_config`)
2. Carga todos los datos desde Supabase con caché de 10 minutos
3. Llama a los componentes de render en orden

No contiene lógica de UI ni SQL. Si quieres cambiar el layout general, este es el archivo.

---

### `components/` — Frontend

#### `hero.py`
Renderiza la sección principal de la página:
- **Columna izquierda:** título con degradado, descripción del proyecto, separador y leyenda de macro-regiones con puntos de color.
- **Columna derecha:** 4 métricas ejecutivas (Talento STEM, Empleo Energía, Energía Limpia, Correlación r), mapa coroplético interactivo de Colombia y tarjeta de alerta de brecha territorial.
- **JavaScript:** alinea la leyenda de regiones con el borde inferior de la tarjeta de alerta usando `getBoundingClientRect()`.

#### `tab_coevolucion.py`
Renderiza la pestaña **📊 Coevolución Nacional**:
- Selector de periodo (radio buttons por semestre)
- 4 tarjetas de métricas con flecha desplegable que explica cada indicador
- Gráfico de doble eje Y: Talento STEM (área azul) vs Empleo Energía (línea dorada)
- Botón `ℹ` que despliega la explicación del gráfico
- Tarjeta de insight con los valores r y R²
- Expander con tabla de datos completa
- Expander de diagnóstico con tipos de energía registrados en la BD

#### `tab_regional.py`
Renderiza la pestaña **🗺️ Brechas Regionales**:
- Alerta de brecha territorial con porcentajes dinámicos
- Selector de semestre
- Mapa coroplético de Colombia coloreado por macro-región
- Gráfico de dona con participación % por región
- Panel de detalle por región seleccionada (departamentos, participación, estudiantes)
- Tarjeta contextual (insight o alerta) según la región elegida
- Expander con tabla regional completa

#### `tab_modelo.py`
Renderiza la pestaña **🧮 Modelo Estadístico**:
- 4 KPI cards: r (Pearson), R² (OLS), pendiente m, intercepto b
- Ecuación del modelo en LaTeX
- Tarjeta de interpretación ejecutiva con proyección a 1 millón de estudiantes
- Gráfico de recta de regresión OLS con puntos reales
- Gráfico de barras horizontales con Top 10 Áreas de Conocimiento STEM
- Expanders con tablas de datos fuente

---

### `utils/` — Utilidades

#### `ui.py`
Contiene:
- **`CSS`** — string con todos los estilos globales del dashboard: fuente Plus Jakarta Sans, fondos oscuros, tarjetas de métricas, pestañas, expanders, animaciones fadeUp/shimmer y ocultamiento del toolbar de Streamlit.
- **`divider(color)`** — línea separadora horizontal.
- **`gradient_divider()`** — separador con degradado teal→azul.
- **`alert(titulo, cuerpo)`** → HTML de tarjeta roja de alerta.
- **`insight(titulo, cuerpo)`** → HTML de tarjeta verde de insight.
- **`card_metrica(...)`** → HTML de tarjeta de métrica con flecha desplegable `▶ ¿Qué es esto?`.
- **`skeleton(height)`** → HTML de placeholder con animación shimmer mientras carga un gráfico.
- **`kpi_card(...)`** → HTML de tarjeta KPI para el modelo estadístico.

#### `charts.py`
Constructores de gráficos Plotly optimizados para tema oscuro:
- `chart_mapa_colombia()` — mapa coroplético con GeoJSON de Colombia (fuente: john-guerra)
- `chart_coevolucion()` — gráfico de doble eje Y con área + línea
- `chart_distribucion_regional()` — gráfico de dona por macro-región
- `chart_top_areas()` — barras horizontales Top 10
- `chart_regresion()` — scatter + recta OLS

Paleta de colores `REGION_COLORS` y diccionario de acentos `C` definidos aquí.

---

### `queries/analytics.py` — Backend SQL

Todas las consultas a Supabase. Cada función usa `@st.cache_data(ttl=600)` para cachear resultados 10 minutos y `sqlalchemy.text()` para compatibilidad con SQLAlchemy 2.0.

| Función | Descripción |
|---|---|
| `get_coevolucion_nacional()` | Métricas cruzadas por semestre: % energía limpia, talento STEM, empleo energía, desempleo |
| `get_distribucion_regional(semester)` | Participación % de talento STEM por macro-región |
| `get_mapa_colombia()` | Datos a nivel departamento para el mapa coroplético |
| `get_top_areas_conocimiento()` | Top 10 áreas STEM por total de estudiantes |
| `get_modelo_estadistico()` | Correlación de Pearson + regresión OLS sobre la serie histórica |
| `get_resource_types_diagnostico()` | Tipos de recurso energético en `fact_energy` con GWh totales |
| `get_time_alignment_diagnostico()` | Verifica alineación de `time_id` entre `fact_energy` y `dim_time` |

---

### `db/connection.py` — Conexión
Crea y devuelve el motor SQLAlchemy conectado a Supabase. La cadena de conexión se lee desde los secretos de Streamlit (`st.secrets`).

---

## 🗄️ Modelo de Datos (Supabase)

```
dim_time                ← time_id, year, semester
dim_region              ← region_id, region_name, departments
fact_energy             ← time_id, resource_type, generation_kwh
fact_education          ← time_id, region_id, field_of_study, stem_enrolled
fact_formal_employment  ← time_id, economic_sector, formal_employment_thousands, unemployment_rate
```

---

## 📊 Fuentes de Datos

| Fuente | Datos |
|---|---|
| **SNIES** (MEN) | Matrículas universitarias STEM por área y región |
| **XM S.A. E.S.P.** | Generación eléctrica por tipo de recurso (Mercado Mayorista) |
| **DANE – GEIH** | Empleo formal y desempleo por sector económico |
| **Banco Mundial** | Contexto macroeconómico de referencia |

---

## 🚀 Cómo Ejecutar

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar secretos de Supabase en .streamlit/secrets.toml
[supabase]
connection_string = "postgresql://..."

# 3. Lanzar el dashboard
streamlit run app.py
```

---

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| **Python 3.11+** | Lenguaje base |
| **Streamlit** | Framework del dashboard |
| **Plotly** | Visualizaciones interactivas |
| **SQLAlchemy + psycopg2** | Conexión a PostgreSQL/Supabase |
| **Pandas + SciPy** | Procesamiento de datos y estadística |
| **Supabase** | Base de datos PostgreSQL en la nube |
