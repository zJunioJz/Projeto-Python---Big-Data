import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Gráfico de Tempo", page_icon="", layout="wide")

# Estilização da barra lateral
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

# Exibe o logo na barra lateral
st.sidebar.image("/mount/src/projeto-python---big-data/Big-data/logo.png", use_column_width=True)

# Mensagem de sucesso
st.success("Gráfico de Tempo")

# Carregador de arquivos na barra lateral
uploaded_file = st.sidebar.file_uploader("Carregar arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Leitura do arquivo Excel
    tabela = pd.read_excel(uploaded_file, sheet_name='Aptidão Física', nrows=350)
    tabela = tabela[['Nome', 'Turma', 'Shuttle run', 'Velocidade / aceleração', 'Tempo de reação direita', 'Tempo de reação 1 direita', 'Tempo de reação 2 direita', 'Tempo de reação 3 direita', 'Tempo de reação esquerda', 'Tempo de reação esquerda 1', 'Tempo de reação esquerda 2', 'Tempo de reação esquerda 3']]

    # Aplica o estilo do arquivo CSS
    try:
        with open('/mount/src/projeto-python---big-data/Big-data/style.css') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Arquivo de estilo não encontrado.")

    # Seleciona a turma
    selected_turma = st.selectbox('Selecione a Turma', tabela['Turma'].unique())

    # Filtra alunos da turma selecionada
    turma_data = tabela[tabela['Turma'] == selected_turma]

    # Seleciona o aluno
    selected_aluno = st.selectbox('Selecione o aluno', turma_data['Nome'].unique())

    # Filtra dados do aluno selecionado
    aluno_data = turma_data[turma_data['Nome'] == selected_aluno]

    # Seleciona as colunas para exibir
    colunas_disponiveis = ['Shuttle run', 'Velocidade / aceleração', 'Tempo de reação direita', 'Tempo de reação 1 direita', 'Tempo de reação 2 direita', 'Tempo de reação 3 direita', 'Tempo de reação esquerda', 'Tempo de reação esquerda 1', 'Tempo de reação esquerda 2', 'Tempo de reação esquerda 3', 'tempo de sustentação']
    colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)

    st.write("### Todos os Dados")
    st.dataframe(tabela[['Nome'] + colunas_selecionadas])

    st.write("### Dados do Aluno Selecionado")
    st.dataframe(aluno_data[['Nome'] + colunas_selecionadas])

    # Calcula a média da turma
    turma_mean = turma_data[colunas_selecionadas].mean().reset_index()
    turma_mean.columns = ['Métrica', 'Média da Turma']

    # Prepara os dados do aluno para a comparação
    aluno_data_selecionadas = aluno_data[colunas_selecionadas].melt(var_name='Métrica', value_name='Valor do Aluno')
    aluno_data_selecionadas['Nome'] = selected_aluno
    comparacao_df = pd.merge(aluno_data_selecionadas, turma_mean, on='Métrica')

    # Plotar gráfico "Dados de tempo do aluno"
    if colunas_selecionadas:
        fig = px.bar(aluno_data, x='Nome', y=colunas_selecionadas, barmode='group', title='Dados de tempo do aluno', text_auto=True)
        fig.update_layout(
            title={
                'text': 'Dados de tempo do aluno',
                'x': 0.45  # Posição centralizada
            },
            bargap=0.60,     
            bargroupgap=0.1,
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

        for trace in fig.data:
            trace.width = 0.10  

        st.plotly_chart(fig, use_container_width=True)

    # Plotar gráfico "Comparação de Tempo do Aluno"
    if colunas_selecionadas:
        fig = px.bar(comparacao_df, x='Métrica', y=['Valor do Aluno', 'Média da Turma'], barmode='group', title=f'Comparação de Tempo do Aluno ({selected_aluno}) com a Média da Turma ({selected_turma})', text_auto=True)
        fig.update_layout(
            title={
                'text': f'Comparação de Tempo do Aluno ({selected_aluno}) com a Média da Turma ({selected_turma})',
                'x': 0.35  # Posição centralizada
            },
            bargap=0.40,
            bargroupgap=0.1,
            xaxis=dict(
                tickfont=dict(
                    size=20  # Tamanho da fonte para o eixo x
                )
            ),
            yaxis=dict(
                tickfont=dict(
                    size=20  
                )
            ),
            font=dict(
                size=15  # Tamanho da fonte
            )
        )
        for trace in fig.data:
            trace.width = 0.30
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Por favor, carregue um arquivo Excel.")
