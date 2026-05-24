# Minería de Datos: Coevolución del Capital Humano STEM y el Mercado Laboral Energético en Colombia (2023)

## 📌 Descripción del Proyecto
Este proyecto de minería de datos tiene como objetivo evaluar y modelar la **coevolución y simbiosis** entre la formación de talento en áreas **STEM** (Ciencia, Tecnología, Ingeniería y Matemáticas), la dinámica del **mercado laboral formal** y la **infraestructura de generación de energía** en Colombia durante el año 2023.

A través de la integración analítica de múltiples fuentes de datos nacionales e internacionales, el sistema consolida un repositorio unificado en la nube (**Supabase/PostgreSQL**) estructurado bajo un **Modelo en Galaxia (Star Schema Avanzado)**. Utilizando técnicas de modelado estadístico relacional, el proyecto describe de manera matemática exacta el impacto socioeconómico y la alineación de competencias de cara a la transición energética del país.

---

## 🛠️ Arquitectura de Datos y Modelo en Galaxia
Para evitar la redundancia y mitigar problemas críticos de almacenamiento (como la explosión cartesiana en cruces masivos), se implementó un almacenamiento multidimensional:

* **Tablas de Dimensiones:**
    * `dim_time`: Indexación temporal por año y semestre (2023-1, 2023-2).
    * `dim_region`: Catastro geográfico y político de departamentos agrupados por Macro-Regiones Naturales de Colombia.
* **Tablas de Hechos (Múltiples Centros):**
    * `fact_education`: Datos analíticos de matrículas universitarias STEM (Fuente: **SNIES - Ministerio de Educación**).
    * `fact_energy`: Registros de generación eléctrica diaria en kWh y tipo de recurso (Fuente: **XM S.A. E.S.P.**).
    * `fact_formal_employment`: Series de tiempo de ocupación sectorial y tasa de desempleo (Fuente: **DANE - GEIH**).
    * `fact_development`: Indicadores de desarrollo macroeconómico (Fuente: **Banco Mundial**).

---

## 🚀 Hallazgos del Modelo Estadístico (Fase de Evaluación)
El pipeline analítico ejecutó algoritmos de asociación y regresión en el entorno de producción, arrojando los siguientes parámetros matemáticos óptimos:

1.  **Algoritmo de Correlación de Pearson ($r$):** `1.0000`
    * *Evaluación:* Coevolución positiva muy fuerte. Existe una sincronía perfecta entre el ingreso de estudiantes a carreras STEM y la absorción de mano de obra en el sector energético durante los semestres analizados.
2.  **Modelo de Regresión Lineal (OLS):**
    * *Ecuación de la Recta:* $Y = 0.001041X - 1924.44$
    * *Coeficiente de Determinación ($R^2$):* `1.0000` (Ajuste perfecto como descriptor exacto de la muestra analizada).
    * *Interpretación:* **Por cada incremento de 10,000 estudiantes matriculados en programas STEM, el ecosistema económico absorbe un estimado de 10.41 mil empleos formales** en el sector de servicios públicos (electricidad, gas y agua).

### 🚨 Brechas Críticas Detectadas (Insights para el Negocio/Estado)
* **Centralización Geográfica del Capital Humano:** La **Región Andina concentra el 68.54%** del total del talento STEM nacional. 
* **Desconexión Territorial:** La **Región Caribe cuenta únicamente con el 16.47%** de los estudiantes STEM matriculados, evidenciando una brecha estructural compleja: los proyectos neurálgicos de transición (parques eólicos en La Guajira, granjas solares en Cesar) se construyen en el Caribe, pero el talento técnico se está concentrando y educando en el centro del país.
* **Evolución de Competencias:** Las disciplinas nativas digitales ganan terreno en el Top 10 nacional, lideradas por *"Desarrollo y análisis de software"* (Puesto 5 con 26,637 estudiantes) y *"Electrónica y automatización"* (Puesto 8), garantizando el perfil para la modernización de redes inteligentes.

---

## 🎯 Objetivo de la Fase Actual: Despliegue con Streamlit
El siguiente paso del ciclo de vida es el **Despliegue (Deployment)**. Se requiere migrar el código analítico actual desde Google Colab hacia un entorno local en **Visual Studio Code** y construir una interfaz web interactiva utilizando **Streamlit**.

### 🗺️ Estructura del Dashboard en Streamlit
La aplicación debe constar de una arquitectura multipágina o modular organizada en tres pestañas/secciones de control:

1.  **Pestaña 1: Balance de Coevolución Nacional**
    * **Métricas Clave (`st.metric`):** Mostrar el Porcentaje de Energía Limpia, Total Talento STEM, Empleo en Energía (en miles) y Tasa de Desempleo País para los semestres del 2023.
    * **Visualización:** Gráfico de doble eje Y (`plotly.subplots`) que contraste las líneas de tendencia de estudiantes STEM vs. Ocupados del Sector.
2.  **Pestaña 2: Distribución y Brechas Regionales**
    * **Visualización Principal:** Gráfico de torta/donas interactivo (`px.pie`) que muestre la participación porcentual del talento por macro-región, destacando visualmente la alerta de centralización andina.
    * **Filtros Dinámicos:** Selector de macro-región (`st.selectbox`) para desglosar la cantidad de departamentos afectados.
3.  **Pestaña 3: Modelo Matemático y Competencias**
    * **KPIs del Modelo:** Desplegar de forma ejecutiva los valores óptimos ($r = 1.0$, $R^2 = 1.0$, Pendiente $m$).
    * **Visualización:** Gráfico de barras horizontales (`px.bar`) con el Top 10 de áreas de conocimiento más demandadas, aplicando una escala cromática estilizada (`Blugrn`).

---

## 📋 Requerimientos Técnicos para Claude (VS Code Prompting)
Para proceder con la implementación, Claude debe ayudar a estructurar el código garantizando las siguientes directrices de ingeniería de software:

1.  **Gestión de Conexiones Seguras:**
    * Uso de `st.connection("postgresql", type="sql")` o `create_engine` con `poolclass=NullPool` para evitar fugas de memoria con Supabase.
    * Manejo de variables de entorno mediante un archivo `.env` o el archivo nativo `.streamlit/secrets.toml` para proteger las credenciales (`DB_HOST`, `DB_PASSWORD`).
2.  **Optimización Analítica (Caching):**
    * Decorar las funciones de consulta SQL con `@st.cache_data` para que el dashboard no sature el servidor Supabase con peticiones repetitivas cada vez que el usuario interactúe con un filtro.
3.  **Tratamiento de Datos Seguros:**
    * Mantener el empaquetado de consultas mediante `sqlalchemy.text()` para evitar conflictos de tipos (`immutabledict`).
    * Preservar el manejo flexible con filtros `ILIKE` en PostgreSQL para la correcta extracción del sector laboral del DANE.
4.  **Estilo Visual Profesional:**
    * Configurar la página con `st.set_page_config(layout="wide", page_title="Dashboard Coevolución STEM", page_icon="⚡")`.
    * Utilizar tipografías limpias y paletas de colores sobrias y ejecutivas acordes al entorno científico del proyecto.

---
**Créditos:** Desarrollado por Camila Acosta  
**Organización:** Blackbird Labs (Bblabs) / Proyecto de Investigación en Minería de Datos  
**Fecha:** Mayo 2026