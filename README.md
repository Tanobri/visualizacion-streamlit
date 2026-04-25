# Dashboard Premium Analítico de Churn (Streamlit)

Un dashboard interactivo construido con **Python** y **Streamlit**, orientado al análisis de retención de clientes bancarios. A diferencia de una exploración genérica de datos, este proyecto aplica ingeniería analítica directa sobre las **Tasas Relativas de Churn** (porcentajes de abandono sobre la masa instalada), convirtiendo 10,000 registros en inteligencia accionable para la toma de decisiones.

## 🛠️ Tecnologías Empleadas

- **Streamlit:** Framework de Python para construir aplicaciones web de datos de manera declarativa, sin necesidad de HTML, CSS ni JavaScript. Convierte scripts de análisis en apps interactivas con pocas líneas de código.
- **Plotly (Python):** Motor de visualización interactiva con soporte completo de hover, zoom y tooltips HTML. Permite gráficas de alta calidad visual con total control sobre colores, layouts y anotaciones.
- **Pandas:** Procesamiento y manipulación de datos tabulares: agrupaciones (`groupby`), filtros, cálculo de tasas y transformaciones de columnas.
- **NumPy:** Soporte numérico para cálculos estadísticos como percentiles (`np.percentile`) y operaciones vectorizadas sobre el dataset.

## 🚀 Cómo Ejecutar Localmente

1. Asegúrate de tener **Python 3.8+** instalado.
2. Instala las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```
3. Coloca el archivo `Churn_Modelling.csv` en la misma carpeta que `streamlit_app.py`.
4. Lanza la aplicación:
   ```bash
   streamlit run streamlit_app.py
   ```
5. Se abrirá automáticamente en tu navegador en `http://localhost:8501`.

---

## 📊 Arquitectura de Visualizaciones (Analíticas)

El dashboard implementa filtrado interactivo cruzado usando Pandas (`st.selectbox`), recalculando la narrativa analítica y la data de Plotly según la geografía seleccionada. Todas las gráficas aplican el cálculo directo de **Tasas Relativas de Churn**:

### 1. Resumen Global (Donut Chart KPI)
- **Visualización:** Gráfico de anillo con anotación central del total de clientes. Panel lateral con indicadores KPI de clientes que permanecen y que abandonan en cifras absolutas y porcentuales.
- **Objetivo:** Establecer la tasa base de abandono del corporativo como punto de referencia para todo el análisis posterior.

### 2. Tasa de Churn por País (Bar Chart Semaforizado)
- **Visualización:** Barras ordenadas por urgencia con colorimetría semafórica: rojo para riesgo alto (>25%), ámbar para riesgo medio (15–25%) y verde para riesgo saludable (<15%). Etiquetas porcentuales sobre cada barra.
- **Objetivo:** Identificar los mercados geográficos con mayor desviación de la tasa base para priorizar intervenciones regionales diferenciadas.

### 3. Tasa de Churn por Rango de Edad (Histograma Superpuesto)
- **Visualización:** Histograma de doble capa: fondo translúcido verde para el total de clientes y barras rojas sobre la tasa de churn por intervalo etario de 2 años. Zona crítica de 40 a 55 años destacada con rectángulo y anotación.
- **Objetivo:** Superar la lectura de volumen etario y revelar el segmento demográfico de mayor sensibilidad al abandono.

### 4. Perfil Financiero (Heatmap de Riesgo 3×3)
- **Visualización:** Matriz bidimensional cruzando nivel de salario (terciles calculados con NumPy) y score crediticio (tres rangos). Cada celda muestra el porcentaje de churn con color proporcional al riesgo.
- **Objetivo:** Demostrar con nueve celdas que el factor determinante del abandono es el score crediticio, independientemente del nivel de ingresos del cliente.

### 5. Tenencia Evolutiva (Time-Series con Marcadores Críticos)
- **Visualización:** Línea suavizada con marcadores coloreados por zona de riesgo (sobre/bajo el promedio global). Línea de referencia punteada del promedio base y anotaciones que señalan la falla de onboarding (T=0), la zona estable y el riesgo tardío (T=9).
- **Objetivo:** Radiografiar el ciclo de vida del cliente e identificar los momentos críticos de intervención para retención.

### 6. Conclusión Estratégica (Data-Driven)
- **Visualización:** Diseño de tres columnas nativas (`st.columns`) presentando tarjetas de impacto con conclusiones procesables.
- **Objetivo:** Consolidar el storytelling de los datos en campañas ejecutables: *Onboarding Seguro*, *Fidelización Senior* y *Alivio Financiero*.

---

## 📁 Estructura del Proyecto

```
visualizacion-streamlit/
├── streamlit_app.py       # Aplicación completa (UI + lógica analítica)
├── Churn_Modelling.csv    # Dataset fuente (10,000 registros)
└── requirements.txt       # Dependencias Python del proyecto
```

## 📦 Dependencias (`requirements.txt`)

```
streamlit
pandas
plotly
numpy
```
