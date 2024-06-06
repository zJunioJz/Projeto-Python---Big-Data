import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_excel('Gráfico atualizado.xlsx', sheet_name='Dados Cadastrais', nrows=351)
df = df[['Nome', 'Sexo', 'Turma', 'Idade -Cálculo média']]

st.set_page_config(page_title="Home", page_icon="", layout="wide")
st.success("Outros gráficos ")

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

idade_counts = df['Idade -Cálculo média'].value_counts().reset_index()
idade_counts.columns = ['Idade', 'Count']

fig = px.pie(idade_counts, values='Count', names='Idade', title='Média Total das Idades')
fig.update_traces(
    textposition='inside',
    textinfo='percent+label'
)
st.plotly_chart(fig, use_container_width=True)

color_discrete_map = {'M': 'Blue', 'F': 'pink'}
fig_sexo = px.histogram(df, x='Turma',nbins=30,color='Sexo',title='Distribuição do sexo por turma',
                        color_discrete_map=color_discrete_map)
fig_sexo.update_layout(
    plot_bgcolor='white',
    xaxis_title='Sexo',
    yaxis_title='Frequência',
    bargap=0.1 
)
st.plotly_chart(fig_sexo, use_container_width=True)

