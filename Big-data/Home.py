import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Configurar layout da página
st.set_page_config(page_title="Medidas Fisiológicas", page_icon="", layout="wide")

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

st.success("**Medidas Fisiológicas**")

# Carregar dados do Excel
tabela_fisio = pd.read_excel('Dados.xlsx', sheet_name='Medidas fisiológicas', nrows=350)
tabela_fisio = tabela_fisio[['Turma', 'Nome', 'FC rep', 'PA rep', 'FCmáx polar', 'FCmáx teste', 'Teste FC', 'FCmáx prev.', 'FC Polar leve', 'FC Polar mod.', 'FC Polar méd.', 'FC Polar forte', 'FC Polar máx', 'FCteste leve', 'FCteste mod.', 'FCteste méd.', 'FCteste forte', 'FCteste máx', 'FCprev leve', 'FCprev mod.', 'FCprev méd.', 'FCprev forte', 'FCprev máx']]

# Substituir valores não identificados por "-"
tabela_fisio = tabela_fisio.replace(',', '-')

# Substituir "-" por " - " para manter o intervalo
tabela_fisio = tabela_fisio.replace(',', ' - ', regex=True)

# Converter para tipo numérico, ignorando os valores não numéricos
tabela_fisio = tabela_fisio.apply(pd.to_numeric, errors='ignore')

for col in tabela_fisio.columns[2:]:
    tabela_fisio[col] = pd.to_numeric(tabela_fisio[col], errors='coerce')

# Carregar estilo CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Selecionar turma
selected_turma = st.selectbox('Selecione a Turma', tabela_fisio['Turma'].unique())

# Filtrar alunos da turma selecionada
alunos_turma = tabela_fisio[tabela_fisio['Turma'] == selected_turma]['Nome'].unique()

# Selecionar aluno
selected_aluno = st.selectbox('Selecione o aluno', alunos_turma)

# Filtrar dados do aluno selecionado
aluno_data_fisio = tabela_fisio[(tabela_fisio['Turma'] == selected_turma) & (tabela_fisio['Nome'] == selected_aluno)]

# Selecionar colunas para exibir
colunas_disponiveis_fisio = ['FC rep', 'PA rep', 'FCmáx polar', 'FCmáx teste', 'Teste FC', 'FCmáx prev.', 'FC Polar leve', 'FC Polar mod.', 'FC Polar méd.', 'FC Polar forte', 'FC Polar máx', 'FCteste leve', 'FCteste mod.', 'FCteste méd.', 'FCteste forte', 'FCteste máx', 'FCprev leve', 'FCprev mod.', 'FCprev méd.', 'FCprev forte', 'FCprev máx']
colunas_selecionadas_fisio = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis_fisio, default=colunas_disponiveis_fisio)

st.write("### Todos os Dados")
st.dataframe(tabela_fisio[['Nome'] + colunas_selecionadas_fisio])

# Mostrar os dados do aluno selecionado com as colunas selecionadas
st.write("### Dados do Aluno Selecionado")
st.dataframe(aluno_data_fisio[['Nome'] + colunas_selecionadas_fisio])

# Visualização com Plotly para o aluno selecionado, com colunas específicas
colunas_grafico_fisio = ['FC rep', 'PA rep', 'FCmáx polar', 'FCmáx teste', 'Teste FC']
if colunas_grafico_fisio:
    fig_fisio = go.Figure()

    fig_fisio.add_trace(go.Bar(
        x=[selected_aluno],
        y=aluno_data_fisio['FC rep'],
        name='FC rep',
        width=0.05,
        marker_color='blue',
        text=aluno_data_fisio['FC rep'],
        textposition='auto',
        textfont=dict(
        size=15  # Tamanho da fonte para o texto das barras
    )  
    ))

    fig_fisio.add_trace(go.Bar(
        x=[selected_aluno],
        y=aluno_data_fisio['PA rep'],
        name='PA rep',
        width=0.05,
        marker_color='lightblue',
        text=aluno_data_fisio['PA rep'],
        textposition='auto',
        textfont=dict(
        size=15  
    )
    ))

    fig_fisio.add_trace(go.Bar(
        x=[selected_aluno],
        y=aluno_data_fisio['FCmáx polar'],
        name='FCmáx polar',
        width=0.05,
        marker_color='red',
        text=aluno_data_fisio['FCmáx polar'],
        textposition='auto',
        textfont=dict(
        size=15
        )
    ))

    fig_fisio.add_trace(go.Bar(
        x=[selected_aluno],
        y=aluno_data_fisio['FCmáx teste'],
        name='FCmáx teste',
        width=0.05,
        marker_color='pink',
        text=aluno_data_fisio['FCmáx teste'],
        textposition='auto',
        textfont=dict(
        size=15  
    )
    ))

    fig_fisio.add_trace(go.Bar(
        x=[selected_aluno],
        y=aluno_data_fisio['Teste FC'],
        name='Teste FC',
        width=0.05,
        marker_color='green',
        text=aluno_data_fisio['Teste FC'],
        textposition='auto',
        textfont=dict(
        size=15  
    )
    ))

    # Atualizando o layout para espaçar as barras
    fig_fisio.update_layout(
        title='Dados Fisiológicos do Aluno',
        barmode='group',
        bargap=0.60,  # Espaçamento entre grupos de barras
        bargroupgap=0.1,  # Espaçamento entre as barras dentro de um grupo
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

    st.plotly_chart(fig_fisio, use_container_width=True)

#usar para rodar > python -m streamlit run Medidas Fisiológicas.py
