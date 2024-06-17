import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_excel('/mount/src/projeto-python---big-data/Big-data/pages/Gráfico atualizado.xlsx', sheet_name='Dados Cadastrais', nrows=351)
df = df[['Nome', 'Sexo', 'Turma', 'Idade -Cálculo média']]


st.set_page_config(page_title="Home", page_icon="", layout="wide")
st.success("Outros gráficos ")


with open('/mount/src/projeto-python---big-data/Big-data/style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


idade_counts = df['Idade -Cálculo média'].value_counts().reset_index()
idade_counts.columns = ['Idade', 'Count']


fig = px.pie(idade_counts, values='Count', names='Idade', title='Média Total das Idades')
fig.update_traces(
    textposition='inside',
    textinfo='percent+label'
)
fig.update_layout(
    font=dict(
        size=15  
    ),
    title={
        'text': 'Média Total das Idades',
        'x': 0.5  # Centralizar o título
    }
)
st.plotly_chart(fig, use_container_width=True)

# Gráfico de histograma de distribuição do sexo por turma
color_discrete_map = {'M': 'Blue', 'F': 'Pink'}
fig_sexo = px.histogram(df, x='Turma', nbins=30, color='Sexo', title='Distribuição do sexo por turma',
                        color_discrete_map=color_discrete_map, text_auto=True)
fig_sexo.update_layout(
    plot_bgcolor='white',
    xaxis_title='Turma',
    yaxis_title='Frequência',
    bargap=0.1,
    title={
        'text': 'Distribuição do sexo por turma',
        'x': 0.5  # Centralizar o título
    },
    xaxis=dict(
        tickfont=dict(
            size=20  
        )
    ),
    yaxis=dict(
        tickfont=dict(
            size=20  
        )
    ),
    font=dict(
        size=15  
    )
)
st.plotly_chart(fig_sexo, use_container_width=True)

st.sidebar.markdown(
    """
    <style>
        .sidebar .sidebar-content {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .sidebar .sidebar-content .block-container {
            margin-top: 20px;
        }
        .sidebar .sidebar-content .stImage {
            margin-bottom: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.image("logo.png", use_column_width=True)

# Usar para rodar > python -m streamlit run Home.py
