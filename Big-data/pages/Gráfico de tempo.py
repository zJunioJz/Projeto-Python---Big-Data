import streamlit as st
import pandas as pd
import plotly.express as px


tabela = pd.read_excel('/mount/src/projeto-python---big-data/Big-data/Gráfico atualizado.xlsx', sheet_name='Aptidão Física (2)', nrows=350)
tabela = tabela[['Nome', 'Turma','Velocidade / aceleração','Tempo de reação direita','Tempo de reação esquerda']]

st.sidebar.image("/mount/src/projeto-python---big-data/Big-data/logo.png", use_column_width=True)
st.success("Gráfico de Tempo ")

selected_turma = st.selectbox('Selecione a Turma', tabela['Turma'].unique())

with open('/mount/src/projeto-python---big-data/Big-data/style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

turma_data = tabela[tabela['Turma'] == selected_turma]

selected_aluno = st.selectbox('Selecione o aluno', turma_data['Nome'].unique())

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
                size=20  # Tamanho da fonte para o eixo y
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
