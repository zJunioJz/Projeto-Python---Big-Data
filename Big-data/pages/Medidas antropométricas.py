import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados do Excel
tabela = pd.read_excel('Dados.xlsx', sheet_name='Medidas antropométricas', nrows=350)
tabela = tabela[['Nome', 'IMC', 'Peso', 'Estatura']]
tabela['IMC'] = pd.to_numeric(tabela['IMC'], errors='coerce')
tabela['Peso'] = pd.to_numeric(tabela['Peso'], errors='coerce')
tabela['Estatura'] = pd.to_numeric(tabela['Estatura'], errors='coerce')

# Configurar layout da página
st.set_page_config(page_title="Home", page_icon="", layout="wide")

st.success("**Medidas antropométricas**")

# Carregar estilo CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Selecionar aluno
selected_aluno = st.selectbox('Selecione o aluno', tabela['Nome'].unique())

# Filtrar dados do aluno selecionado
aluno_data = tabela[tabela['Nome'] == selected_aluno]


# Selecionar colunas para exibir
colunas_disponiveis = ['IMC', 'Peso', 'Estatura']
colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)

# Mostrar todos os dados na tabela completa
st.write("### Todos os Dados")
st.dataframe(tabela)

# Mostrar os dados do aluno selecionado com as colunas selecionadas
st.write("### Dados do Aluno Selecionado")
st.dataframe(aluno_data[['Nome'] + colunas_selecionadas])


# Visualização com Plotly para o aluno selecionado, se houver colunas selecionadas
if colunas_selecionadas:
    fig = px.bar(aluno_data, x='Nome', y=colunas_selecionadas, barmode='group', title='')
    st.plotly_chart(fig, use_container_width=True)
