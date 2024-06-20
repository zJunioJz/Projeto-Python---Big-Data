import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Medidas Fisiológicas", page_icon="", layout="wide")

# Função para carregar os dados do Excel
@st.cache_data
def load_data(file):
    data = pd.read_excel(file, sheet_name='Medidas fisiológicas', nrows=350)
    data = data[['Turma', 'Nome', 'FC rep', 'PA rep', 'FCmáx polar', 'FCmáx teste', 'Teste FC', 'FCmáx prev.', 'FC Polar leve', 'FC Polar mod.', 'FC Polar méd.', 'FC Polar forte', 'FC Polar máx', 'FCteste leve', 'FCteste mod.', 'FCteste méd.', 'FCteste forte', 'FCteste máx', 'FCprev leve', 'FCprev mod.', 'FCprev méd.', 'FCprev forte', 'FCprev máx']]
    for col in data.columns[2:]:
        data[col] = pd.to_numeric(data[col], errors='coerce')
    return data

# Carregar o arquivo do Excel
uploaded_file = st.file_uploader("Faça o upload do arquivo Excel", type=["xlsx"])
if uploaded_file:
    tabela_fisio = load_data(uploaded_file)
    
    # Aplicar estilo
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

    st.sidebar.image("/mount/src/projeto-python---big-data/Big-data/logo.png", use_column_width=True)

    st.success("**Medidas Fisiológicas**")

    # Seleção da turma e do aluno
    selected_turma = st.selectbox('Selecione a Turma', tabela_fisio['Turma'].unique())
    alunos_turma = tabela_fisio[tabela_fisio['Turma'] == selected_turma]['Nome'].unique()
    selected_aluno = st.selectbox('Selecione o aluno', alunos_turma)

    # Dados do aluno selecionado
    aluno_data_fisio = tabela_fisio[(tabela_fisio['Turma'] == selected_turma) & (tabela_fisio['Nome'] == selected_aluno)]

    # Seleção das colunas a serem exibidas
    colunas_disponiveis_fisio = ['FC rep', 'PA rep', 'FCmáx polar', 'FCmáx teste', 'Teste FC', 'FCmáx prev.', 'FC Polar leve', 'FC Polar mod.', 'FC Polar méd.', 'FC Polar forte', 'FC Polar máx', 'FCteste leve', 'FCteste mod.', 'FCteste méd.', 'FCteste forte', 'FCteste máx', 'FCprev leve', 'FCprev mod.', 'FCprev méd.', 'FCprev forte', 'FCprev máx']
    colunas_selecionadas_fisio = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis_fisio, default=colunas_disponiveis_fisio)

    # Exibir os dados
    st.write("### Todos os Dados")
    st.dataframe(tabela_fisio[['Nome'] + colunas_selecionadas_fisio])

    st.write("### Dados do Aluno Selecionado")
    st.dataframe(aluno_data_fisio[['Nome'] + colunas_selecionadas_fisio])

    # Gerar gráficos
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

        # Atualizando o layout para espaçar as barras e centralizar o título
        fig_fisio.update_layout(
            title=dict(
                text='Dados Fisiológicos do Aluno',
                x=0.40
            ),
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

        tabela_fisio.replace([float('inf'), float('-inf')], pd.NA, inplace=True)

        media_turma = tabela_fisio[tabela_fisio['Turma'] == selected_turma][colunas_grafico_fisio].mean().round(2)

        fig_comparacao = go.Figure()

        fig_comparacao.add_trace(go.Bar(
            x=colunas_grafico_fisio,
            y=aluno_data_fisio[colunas_grafico_fisio].values.flatten(),
            name='Aluno',
            marker_color='darkblue',
            text=aluno_data_fisio[colunas_grafico_fisio].values.flatten(),
            textposition='auto',
            textfont=dict(
                size=15
            )
        ))

        fig_comparacao.add_trace(go.Bar(
            x=colunas_grafico_fisio,
            y=media_turma.values,
            name='Média da Turma',
            marker_color='lightblue',
            text=media_turma.values,
            textposition='auto',
            textfont=dict(
                size=15
            )
        ))

        fig_comparacao.update_layout(
            title=dict(
                text='Comparação do Aluno com a Média da Turma',
                x=0.35
            ),
            barmode='group',
            bargap=0.15,  # Espaçamento entre grupos de barras
            bargroupgap=0.1,  # Espaçamento entre as barras dentro de um grupo
            xaxis=dict(
                tickfont=dict(
                    size=15  # Tamanho da fonte para o eixo x
                )
            ),
            yaxis=dict(
                tickfont=dict(
                    size=15 
                )
            )
        )

        st.plotly_chart(fig_comparacao, use_container_width=True)
else:
    st.warning("Por favor, faça o upload de um arquivo Excel para começar.")
