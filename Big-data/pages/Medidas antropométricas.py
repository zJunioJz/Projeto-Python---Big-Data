import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Medidas Antropométricas", page_icon="", layout="wide")

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
st.success("**Medidas antropométricas**")

# Carregador de arquivos na barra lateral
uploaded_file = st.sidebar.file_uploader("Carregar arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Leitura do arquivo Excel
    tabela = pd.read_excel(uploaded_file, sheet_name='Medidas antropométricas', nrows=350)
    tabela = tabela[['Nome', 'Turma', 'IMC', 'Peso', 'Estatura']]
    tabela['IMC'] = pd.to_numeric(tabela['IMC'], errors='coerce')
    tabela['Peso'] = pd.to_numeric(tabela['Peso'], errors='coerce')
    tabela['Estatura'] = pd.to_numeric(tabela['Estatura'], errors='coerce')
    tabela['Envergadura'] = pd.to_numeric(tabela['Envergadura'], errors='coerce')

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
    colunas_disponiveis = ['IMC', 'Peso', 'Estatura', 'Envergadura']
    colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)

    st.write("### Todos os Dados")
    st.dataframe(tabela[['Nome']+colunas_selecionadas])

    st.write("### Dados do Aluno Selecionado")
    st.dataframe(aluno_data[['Nome'] + colunas_selecionadas])

    # Gráfico das medidas antropométricas do aluno
    if colunas_selecionadas:
        fig = px.bar(aluno_data, x='Nome', y=colunas_selecionadas, barmode='group', title='', text_auto=True)
        fig.update_layout(
            title={
                'text': f'Medidas antropométricas do aluno ({selected_aluno})',
                'x': 0.45  # Posição centralizada
            },
            bargap=0.60,     
            bargroupgap=0.1,
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
        
        for trace in fig.data:
            trace.width = 0.05  # Espessura das colunas
        
        st.plotly_chart(fig, use_container_width=True)

    # Gráfico de dispersão IMC vs Peso
    fig_scatter = px.scatter(turma_data, x='IMC', y='Peso', title='Relação entre IMC e Peso', color='Nome', hover_name='Nome')
    fig_scatter.update_layout(
        title={
            'text': 'Relação entre IMC e Peso',
            'x': 0.5  # Posição centralizada
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

else:
    st.warning("Por favor, carregue um arquivo Excel.")
