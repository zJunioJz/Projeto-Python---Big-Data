import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados do Excel
tabela = pd.read_excel('Gráfico atualizado.xlsx', sheet_name='Medidas antropométricas', nrows=350)
tabela = tabela[['Nome', 'Turma', 'IMC', 'Peso', 'Estatura']]
tabela['IMC'] = pd.to_numeric(tabela['IMC'], errors='coerce')
tabela['Peso'] = pd.to_numeric(tabela['Peso'], errors='coerce')
tabela['Estatura'] = pd.to_numeric(tabela['Estatura'], errors='coerce')

# Configurar layout da página
st.set_page_config(page_title="Home", page_icon="", layout="wide")

st.success("**Medidas antropométricas**")

# Carregar estilo CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Selecionar turma
selected_turma = st.selectbox('Selecione a Turma', tabela['Turma'].unique())

# Filtrar dados da turma selecionada
turma_data = tabela[tabela['Turma'] == selected_turma]

# Selecionar aluno dentro da turma selecionada
selected_aluno = st.selectbox('Selecione o aluno', turma_data['Nome'].unique())

# Filtrar dados do aluno selecionado
aluno_data = turma_data[turma_data['Nome'] == selected_aluno]

# Selecionar colunas para exibir
colunas_disponiveis = ['IMC', 'Peso', 'Estatura']
colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)

# Mostrar todos os dados na tabela completa
st.write("### Todos os Dados")
st.dataframe(tabela[['Nome']+colunas_selecionadas])

# Mostrar os dados do aluno selecionado com as colunas selecionadas
st.write("### Dados do Aluno Selecionado")
st.dataframe(aluno_data[['Nome'] + colunas_selecionadas])

# Visualização com Plotly para o aluno selecionado, se houver colunas selecionadas
if colunas_selecionadas:
    fig = px.bar(aluno_data, x='Nome', y=colunas_selecionadas, barmode='group', title='')
    fig.update_layout(
        title={
            'text': f'Medidas antropométricas do aluno ({selected_aluno})',
            'x': 0.45  # Posição centralizada
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# Gráfico de dispersão IMC vs Peso
fig_scatter = px.scatter(turma_data, x='IMC', y='Peso', title='Relação entre IMC e Peso', color='Nome', hover_name='Nome')
fig_scatter.update_layout(
    title={
        'text': 'Relação entre IMC e Peso',
        'x': 0.5  # Posição centralizada
    }
)
st.plotly_chart(fig_scatter, use_container_width=True)

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
