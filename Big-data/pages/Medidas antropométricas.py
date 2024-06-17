import streamlit as st
import pandas as pd
import plotly.express as px

tabela = pd.read_excel('/mount/src/projeto-python---big-data/Big-data/Gráfico atualizado.xlsx', sheet_name='Medidas antropométricas', nrows=350)
tabela = tabela[['Nome', 'Turma', 'IMC', 'Peso', 'Estatura']]
tabela['IMC'] = pd.to_numeric(tabela['IMC'], errors='coerce')
tabela['Peso'] = pd.to_numeric(tabela['Peso'], errors='coerce')
tabela['Estatura'] = pd.to_numeric(tabela['Estatura'], errors='coerce')

st.sidebar.image("/mount/src/projeto-python---big-data/Big-data/logo.png", use_column_width=True)
st.success("**Medidas antropométricas**")

with open('/mount/src/projeto-python---big-data/Big-data/style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

selected_turma = st.selectbox('Selecione a Turma', tabela['Turma'].unique())

turma_data = tabela[tabela['Turma'] == selected_turma]

selected_aluno = st.selectbox('Selecione o aluno', turma_data['Nome'].unique())

aluno_data = turma_data[turma_data['Nome'] == selected_aluno]

colunas_disponiveis = ['IMC', 'Peso', 'Estatura']
colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)

st.write("### Todos os Dados")
st.dataframe(tabela[['Nome']+colunas_selecionadas])

st.write("### Dados do Aluno Selecionado")
st.dataframe(aluno_data[['Nome'] + colunas_selecionadas])

if colunas_selecionadas:
    fig = px.bar(aluno_data, x='Nome', y=colunas_selecionadas, barmode='group', title='', text_auto=True)
    fig.update_layout(
        title={
            'text': f'Medidas antropométricas do aluno ({selected_aluno})',
            'x': 0.45  # Posição centralizada
        },
        bargap=0.60,     
        bargroupgap=0.1
    )
    
    for trace in fig.data:
        trace.width = 0.05  # Espessura das colunas
        fig.update_layout(
        xaxis=dict(
            tickfont=dict(
                size=20  # Tamanho da fonte para o eixo x
            )
        ),
        yaxis=dict(
            tickfont=dict(
                size=20  # Tamanho da fonte para o eixo y
            )
        ),
        font=dict(
            size=15  # Tamanho da fonte
        )
    )
    st.plotly_chart(fig, use_container_width=True)

# Gráfico de dispersão IMC vs Peso
fig_scatter = px.scatter(turma_data, x='IMC', y='Peso', title='Relação entre IMC e Peso', color='Nome', hover_name='Nome')
fig_scatter.update_layout(
    title={
        'text': 'Relação entre IMC e Peso',
        'x': 0.5 
        
    },
    xaxis=dict(
            tickfont=dict(
                size=20  # Tamanho da fonte para o eixo x
            )
        ),
        yaxis=dict(
            tickfont=dict(
                size=20  # Tamanho da fonte para o eixo y
            )
        )
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
