import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Configuración
st.set_page_config(page_title="Churn Bancario", layout="wide")

# Cargar datos
@st.cache_data
def load_data():
    csv_path = Path(__file__).parent / "Churn_Modelling.csv"
    return pd.read_csv(csv_path)

df = load_data()

st.title("Dashboard de Churn Bancario")
st.subheader("Obrian Sanchez y Andres Cardoso")

#///////////////////////////////////

import plotly.graph_objects as go

st.subheader("Resumen de Fidelidad de Clientes")

# Datos
total = len(df)
churn = df["Exited"].sum()
stay = total - churn

# Donut
fig = go.Figure(data=[go.Pie(
    labels=["Permanecen", "Abandonan"],
    values=[stay, churn],
    hole=0.65,  # un poco más grande el hueco
    marker=dict(colors=["#1ABC9C", "#FF4B5C"]),
    textinfo="percent",
    textfont=dict(size=18)  # números más grandes
)])

# Layout del gráfico
fig.update_layout(
    height=500,  # 🔥 MÁS GRANDE
    margin=dict(t=0, b=0, l=0, r=0),
    showlegend=False,
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    annotations=[
        dict(
            text=f"Total Clientes<br><b>{total:,}</b>",
            x=0.5, y=0.5,
            showarrow=False,
            align="center",
            font=dict(size=32),  # controla todo el bloque
        )
    ]
)

# Layout en columnas (mejor proporción)
col1, col2 = st.columns([1, 2.5])  # 🔥 más espacio al gráfico

with col1:
    st.markdown(f"""
    ### 🟢 Permanecen  
    {stay:,} = {stay/total*100:.1f}%

    ### 🔴 Abandonan  
    {churn:,} = {churn/total*100:.1f}%

    """)
    
    st.info("""
    Los datos muestran que el 20.4% de los clientes ha abandonado el banco, advirtiendo una deserción severa y un claro problema de retención.
    """)

with col2:
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
    -----
    
    """)

#///////////////////////////////////

import plotly.graph_objects as go

st.subheader("Tasa de Churn por País")

# =========================
# 1. PREPARAR DATOS
# =========================
geo = df.groupby("Geography")["Exited"].mean().reset_index()

# Ordenar de mayor a menor
geo = geo.sort_values("Exited", ascending=False)

# Clasificación de riesgo
def riesgo(x):
    if x > 0.25:
        return "Alto"
    elif x > 0.15:
        return "Medio"
    else:
        return "Bajo"

geo["Riesgo"] = geo["Exited"].apply(riesgo)

# Colores (igual a tu D3)
colores = {
    "Alto": "#FF4B5C",
    "Medio": "#F59E0B",
    "Bajo": "#1ABC9C"
}

geo["Color"] = geo["Riesgo"].map(colores)

# =========================
# 2. CREAR GRÁFICO
# =========================
fig = go.Figure()

fig.add_trace(go.Bar(
    x=geo["Geography"],
    y=geo["Exited"],
    text=[f"{x*100:.1f}%" for x in geo["Exited"]],
    textposition="outside",
    marker=dict(
        color=geo["Color"],
        line=dict(width=0)
    )
))

# =========================
# 3. ESTILO (AQUÍ ESTÁ LA MAGIA 🔥)
# =========================
fig.update_layout(
    height=550,  # 🔥 más alto (clave)
    
    margin=dict(t=40, b=40, l=40, r=40),
    
    yaxis=dict(
        title="Tasa de Abandono (%)",
        tickformat=".0%",
        range=[0, 0.4],
        gridcolor="rgba(255,255,255,0.1)"
    ),
    
    xaxis=dict(
        title="Mercados Regionales (Países)"
    ),
    
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    
    font=dict(color="white"),
    
    showlegend=False,
    
    bargap=0.4  # 🔥 separación entre barras
)

# =========================
# 4. CENTRAR EL GRÁFICO
# =========================
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    st.plotly_chart(fig, use_container_width=True)

# =========================
# 5. LEYENDA VISUAL
# =========================
st.markdown("""
### 🔴 Riesgo Alto (>25%)  
### 🟡 Riesgo Medio (15% - 25%)  
### 🟢 Riesgo Bajo (<15%)
""")

# =========================
# 6. INSIGHT
# =========================
st.info("""
Alemania presenta la tasa de abandono más alta (32.4%), duplicando a Francia y España, lo que sugiere un problema específico en ese mercado regional.
""")

st.markdown("""
    -----
    
    """)
#///////////////////////////////////


st.subheader("Tasa de Churn por Rango de Edad")

import numpy as np
import plotly.graph_objects as go

# =========================
# 1. BINS
# =========================
bins = np.arange(18, 90, 3)
df["AgeBin"] = pd.cut(df["Age"], bins=bins)

# =========================
# 2. MÉTRICAS
# =========================
age_stats = df.groupby("AgeBin").agg(
    total=("Exited", "size"),
    churn=("Exited", "mean")
).reset_index()

# Filtrar ruido
age_stats = age_stats[age_stats["total"] > 5]

# Centro del bin (para eje correcto)
age_stats["AgeMid"] = age_stats["AgeBin"].apply(lambda x: x.mid)

# Label del rango (para tooltip)
age_stats["AgeLabel"] = age_stats["AgeBin"].apply(
    lambda x: f"{int(x.left)} - {int(x.right)}"
)

# =========================
# 3. FIGURA
# =========================
fig = go.Figure()

# 🔥 FONDO VERDE (100%)
fig.add_trace(go.Bar(
    x=age_stats["AgeMid"],
    y=[1]*len(age_stats),
    marker_color="#10B981",
    opacity=0.15,
    name="Permanecen",
    hoverinfo="skip"
))

# 🔥 CHURN ROJO
fig.add_trace(go.Bar(
    x=age_stats["AgeMid"],
    y=age_stats["churn"],
    marker_color="#F43F5E",
    name="Abandonan",
    
    customdata=age_stats["AgeLabel"],
    
    hovertemplate=(
        "Edad: %{customdata} años<br>" +
        "Churn: %{y:.1%}<extra></extra>"
    )
))

# =========================
# 4. ZONA DE RIESGO
# =========================
fig.add_vrect(
    x0=40, x1=55,
    fillcolor="#F43F5E",
    opacity=0.08,
    line_width=1,
    line_dash="dash"
)

fig.add_annotation(
    x=47,
    y=1.05,
    text="Zona de Alto Riesgo (40–55)",
    showarrow=False,
    font=dict(color="#F43F5E", size=14)
)

# =========================
# 5. ESTILO
# =========================
fig.update_layout(
    barmode="overlay",
    height=500,
    
    xaxis=dict(
        title="Edad del Cliente (Años)",
        tickmode="array",
        tickvals=[20,30,40,50,55,60,70,80]
    ),
    
    yaxis=dict(
        title="Tasa de Churn (%)",
        tickformat=".0%",
        range=[0,1],
        gridcolor="rgba(255,255,255,0.1)"
    ),
    
    legend=dict(
        orientation="h",
        y=1.1,
        x=0.5,
        xanchor="center"
    ),
    
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    
    font=dict(color="white"),
    
    bargap=0.05
)

# =========================
# 6. MOSTRAR
# =========================
st.plotly_chart(fig, use_container_width=True)

# =========================
# 7. INSIGHT
# =========================
st.info("""
Los clientes entre 40 y 55 años presentan la mayor tasa de abandono, lo que indica un segmento crítico que requiere estrategias de retención específicas.
""")

st.markdown("""
    -----
    
    """)

#///////////////////////////////////

st.subheader("Tasa de Churn por Perfil Financiero")

import numpy as np
import pandas as pd
import plotly.graph_objects as go

# =========================
# 1. GRUPOS (IGUAL QUE TENÍAS)
# =========================

q1 = df["EstimatedSalary"].quantile(0.3333)
q2 = df["EstimatedSalary"].quantile(0.6666)

def salary_group(x):
    if x <= q1:
        return f"Bajo (< ${int(q1/1000)}k)"
    elif x <= q2:
        return f"Medio (${int(q1/1000)}k - ${int(q2/1000)}k)"
    else:
        return f"Alto (> ${int(q2/1000)}k)"

def score_group(x):
    if x < 500:
        return "Bajo (300-500)"
    elif x <= 700:
        return "Medio (500-700)"
    else:
        return "Alto (700-850)"

df["SalaryGroup"] = df["EstimatedSalary"].apply(salary_group)
df["ScoreGroup"] = df["CreditScore"].apply(score_group)

# =========================
# 🔥 ORDEN CORREGIDO (ÚNICO CAMBIO IMPORTANTE)
# =========================

x_order = [
    f"Bajo (< ${int(q1/1000)}k)",
    f"Medio (${int(q1/1000)}k - ${int(q2/1000)}k)",
    f"Alto (> ${int(q2/1000)}k)"
]

y_order = [
    "Alto (700-850)",
    "Medio (500-700)",
    "Bajo (300-500)"
]

# =========================
# 2. MATRIZ
# =========================
heatmap_data = []

for y in y_order:
    row = []
    for x in x_order:
        subset = df[(df["ScoreGroup"] == y) & (df["SalaryGroup"] == x)]
        total = len(subset)
        exited = subset["Exited"].sum()
        rate = exited / total if total > 0 else 0
        row.append(rate)
    heatmap_data.append(row)

heatmap_data = np.array(heatmap_data)

# =========================
# 3. COLORES (IGUAL)
# =========================
def color_scale(v):
    if v >= 0.25:
        return "#F43F5E"
    elif v >= 0.18:
        return "#F59E0B"
    else:
        return "#10B981"

colors = [[color_scale(v) for v in row] for row in heatmap_data]

# =========================
# 4. GRÁFICO (SOLO TEXTO MÁS GRANDE)
# =========================
fig = go.Figure()

for i, y in enumerate(y_order):
    for j, x in enumerate(x_order):
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode="markers+text",
            
            marker=dict(
                size=140,  # 🔥 un poco más grande
                color=colors[i][j],
                symbol="square"
            ),
            
            text=f"{heatmap_data[i][j]*100:.1f}%",
            textfont=dict(size=34, color="white"),  # 🔥 TEXTO MÁS GRANDE
            
            hovertemplate=(
                f"Perfil: {y} y {x}<br>" +
                f"Tasa Churn: {heatmap_data[i][j]*100:.1f}%<extra></extra>"
            ),
            
            showlegend=False
        ))

# =========================
# 5. ESTILO (NO TOCADO)
# =========================
fig.update_layout(
    height=650,
    
    xaxis=dict(
        title="Nivel de Salario",
        categoryorder="array",
        categoryarray=x_order
    ),
    
    yaxis=dict(
        title="Nivel de Score Crediticio",
        categoryorder="array",
        categoryarray=y_order
    ),
    
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    
    font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# 6. INSIGHT (IGUAL)
# =========================
st.info("""
Los clientes con bajo score crediticio presentan mayor abandono sin importar su salario, lo que indica que el score es el principal factor de riesgo.
""")

st.markdown("""
    -----
    
    """)

#///////////////////////////////////

st.subheader("Tasa de Churn según Años de Tenencia")

import plotly.graph_objects as go
import pandas as pd

# =========================
# 1. PROCESAMIENTO
# =========================

tenure_df = df.groupby("Tenure").agg(
    total=("Exited", "count"),
    exited=("Exited", "sum")
).reset_index()

tenure_df["rate"] = tenure_df["exited"] / tenure_df["total"]

# Promedio global
global_rate = df["Exited"].mean()

# =========================
# 2. COLORES (MISMA LÓGICA)
# =========================

def get_color(rate):
    if rate > global_rate + 0.005:
        return "#f43f5e"  # rojo
    elif rate < global_rate - 0.005:
        return "#10b981"  # verde
    else:
        return "#f59e0b"  # amarillo

tenure_df["color"] = tenure_df["rate"].apply(get_color)

# =========================
# 3. FIGURA
# =========================

fig = go.Figure()

# 🔵 Línea suavizada
fig.add_trace(go.Scatter(
    x=tenure_df["Tenure"],
    y=tenure_df["rate"],
    mode="lines",
    line=dict(
        color="rgba(99, 102, 241, 0.6)",
        width=4,
        shape="spline"
    ),
    name="Tendencia"
))

# 🔴🟡🟢 Puntos
fig.add_trace(go.Scatter(
    x=tenure_df["Tenure"],
    y=tenure_df["rate"],
    mode="markers",
    marker=dict(
        size=12,
        color=tenure_df["color"],
        line=dict(width=2, color="#0E1117")
    ),
    hovertemplate=
        "⏳ Tenencia: %{x} años<br>" +
        "Churn: %{y:.1%}<br>" +
        "<extra></extra>",
    showlegend=False
))

# =========================
# 4. LÍNEA PROMEDIO
# =========================

fig.add_hline(
    y=global_rate,
    line_dash="dash",
    line_color="#94a3b8"
)

fig.add_annotation(
    x=tenure_df["Tenure"].max(),
    y=global_rate,
    text=f"Promedio Base ({global_rate*100:.1f}%)",
    showarrow=False,
    font=dict(color="#94a3b8", size=13),
    xanchor="right",
    yshift=10
)

# =========================
# 5. ANOTACIONES (BIEN POSICIONADAS)
# =========================

def add_annotation(x_val, text, color, align):
    point = tenure_df[tenure_df["Tenure"] == x_val]
    if len(point) == 0:
        return
    
    y_val = point["rate"].values[0]

    fig.add_annotation(
        x=x_val,
        y=y_val,
        text=text,
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-50,
        font=dict(color=color, size=13),
        xanchor=align
    )

# 🔥 Ajustadas correctamente
add_annotation(0, "Riesgo de Onboarding", "#f43f5e", "left")
add_annotation(5, "Etapa Estable", "#10b981", "center")
add_annotation(9, "Riesgo Tardío", "#f43f5e", "right")

# =========================
# 6. ESTILO FINAL
# =========================

fig.update_layout(
    height=600,
    
    paper_bgcolor="#0E1117",
    plot_bgcolor="#0E1117",
    
    font=dict(color="white"),
    
    xaxis=dict(
        title="Años de Tenencia en el Banco",
        showgrid=False
    ),
    
    yaxis=dict(
        title="Tasa de Abandono (Churn %)",
        tickformat=".0%",
        range=[0.15, tenure_df["rate"].max() * 1.1],  # 🔥 AQUÍ EL FIX CLAVE
        gridcolor="rgba(255,255,255,0.05)"
    )
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# 7. INSIGHT
# =========================

st.info("""
El abandono es más alto al inicio (problemas de onboarding), luego se estabiliza, y vuelve a aumentar en clientes antiguos, lo que puede indicar fatiga o competencia.
""")
st.markdown("""
    -----
    
    """)