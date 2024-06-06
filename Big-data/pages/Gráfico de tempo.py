import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar dados do Excel
tabela = pd.read_excel('Gráfico atualizado.xlsx', sheet_name='Aptidão Física (2)', nrows=350)
tabela = tabela[['Nome', 'Turma','Velocidade / aceleração','Tempo de reação direita','Tempo de reação esquerda']]

# Configurar layout da página
st.set_page_config(page_title="Home", page_icon="", layout="wide")
st.success("Gráfico de Tempo ")

# Selecionar turma
selected_turma = st.selectbox('Selecione a Turma', tabela['Turma'].unique())

with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Filtrar dados da turma selecionada
turma_data = tabela[tabela['Turma'] == selected_turma]

# Selecionar aluno dentro da turma selecionada
selected_aluno = st.selectbox('Selecione o aluno', turma_data['Nome'].unique())

# Filtrar dados do aluno selecionado
aluno_data = turma_data[turma_data['Nome'] == selected_aluno]

colunas_disponiveis = ['Velocidade / aceleração', 'Tempo de reação direita','Tempo de reação esquerda']
colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)

st.write("### Todos os Dados")
st.dataframe(tabela[['Nome'] + colunas_selecionadas])

st.write("### Dados do Aluno Selecionado")
st.dataframe(aluno_data[['Nome'] + colunas_selecionadas])

turma_mean = turma_data[colunas_selecionadas].mean().reset_index()
turma_mean.columns = ['Métrica', 'Média da Turma']

aluno_data_selecionadas = aluno_data[colunas_selecionadas].melt(var_name='Métrica', value_name='Valor do Aluno')
aluno_data_selecionadas['Nome'] = selected_aluno

comparacao_df = pd.merge(aluno_data_selecionadas, turma_mean, on='Métrica')

# Plotar gráfico "Dados de tempo do aluno"
if colunas_selecionadas:
    fig = px.bar(aluno_data, x='Nome', y=colunas_selecionadas, barmode='group', title='Dados de tempo do aluno') 
    fig.update_layout(
        title={
            'text': 'Dados de tempo do aluno',
            'x': 0.45  # Posição centralizada
        }
    )
    st.plotly_chart(fig, use_container_width=True)

# Plotar gráfico "Comparação de Tempo do Aluno"
if colunas_selecionadas:
    fig = px.bar(comparacao_df, x='Métrica', y=['Valor do Aluno', 'Média da Turma'], barmode='group', title=f'Comparação de Tempo do Aluno ({selected_aluno}) com a Média da Turma ({selected_turma})')
    fig.update_layout(
        title={
            'text': f'Comparação de Tempo do Aluno ({selected_aluno}) com a Média da Turma ({selected_turma})',
            'x': 0.35  # Posição centralizada
        }
    )
    st.plotly_chart(fig, use_container_width=True)

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
