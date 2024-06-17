import streamlit as st
import pandas as pd
import plotly.express as px


tabela = pd.read_excel('/mount/src/projeto-python---big-data/Big-data/Gráfico atualizado.xlsx', sheet_name='Aptidão Física', nrows=350)
tabela = tabela[['Nome', 'Turma', 'Salto horizontal 1', 'Salto horizontal 2', 'Salto vertical', 'Salto vertical 1', 'Salto vertical 2']]

st.sidebar.image("/mount/src/projeto-python---big-data/Big-data/logo.png", use_column_width=True)
st.success("Gráfico de força ")


selected_turma = st.selectbox('Selecione a Turma', tabela['Turma'].unique())


with open('/mount/src/projeto-python---big-data/Big-data/style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



turma_data = tabela[tabela['Turma'] == selected_turma]


selected_aluno = st.selectbox('Selecione o aluno', turma_data['Nome'].unique())


aluno_data = turma_data[turma_data['Nome'] == selected_aluno]


colunas_disponiveis = ['Salto horizontal 1', 'Salto horizontal 2', 'Salto vertical', 'Salto vertical 1', 'Salto vertical 2']
colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)


st.write("### Todos os Dados")
st.dataframe(turma_data[['Nome'] + colunas_selecionadas])


st.write("### Dados do Aluno Selecionado")
st.dataframe(aluno_data[['Nome'] + colunas_selecionadas])


turma_mean = turma_data[colunas_selecionadas].mean().reset_index()
turma_mean.columns = ['Métrica', 'Média da Turma']


aluno_data_selecionadas = aluno_data[colunas_selecionadas].melt(var_name='Métrica', value_name='Valor do Aluno')
aluno_data_selecionadas['Nome'] = selected_aluno
comparacao_df = pd.merge(aluno_data_selecionadas, turma_mean, on='Métrica')

# Plotar gráficos
if colunas_selecionadas:
    fig = px.bar(aluno_data, x='Nome', y=colunas_selecionadas, barmode='group', title='Dados de Força do Aluno', text_auto=True)
    for trace in fig.data:
        trace.width = 0.08  
    fig.update_layout(
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
    
    st.plotly_chart(fig, use_container_width=True)

if colunas_selecionadas:
    fig = px.bar(comparacao_df, x='Métrica', y=['Valor do Aluno', 'Média da Turma'], barmode='group', title=f'Comparação de Força do Aluno ({selected_aluno}) com a Média da Turma ({selected_turma})', text_auto=True)
    fig.update_layout(
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
#usar para rodar > python -m streamlit run Home.py
