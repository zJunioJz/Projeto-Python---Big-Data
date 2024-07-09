import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Outros Gráficos", page_icon="", layout="wide")

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
st.success("Outros gráficos")

# Carregador de arquivos na barra lateral
uploaded_file = st.sidebar.file_uploader("Carregar arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Leitura do arquivo Excel
    df = pd.read_excel(uploaded_file, sheet_name='Dados Cadastrais', nrows=351)
    df = df[['Nome', 'Sexo', 'Turma', 'Idade -Cálculo média']]

    # Aplica o estilo do arquivo CSS
    try:
        with open('/mount/src/projeto-python---big-data/Big-data/style.css') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Arquivo de estilo não encontrado.")

    # Cálculo da média de idades
    idade_counts = df['Idade -Cálculo média'].value_counts().reset_index()
    idade_counts.columns = ['Idade', 'Count']

    # Gráfico de pizza da média total das idades
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
        bargap=0.5,
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

else:
    st.warning("Por favor, carregue um arquivo Excel.")

# Rodar o comando: python -m streamlit run Home.py
