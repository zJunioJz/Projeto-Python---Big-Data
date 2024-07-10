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
    try:
        aptidao_fisica = pd.read_excel(uploaded_file, sheet_name='APTIDÃO FÍSICA')
        dados_cadastrais = pd.read_excel(uploaded_file, sheet_name='Dados Cadastrais')
    except Exception as e:
        st.error(f"Erro ao ler as planilhas: {e}")
        st.stop()

    # Verificar e limpar nomes das colunas
    aptidao_fisica.columns = aptidao_fisica.columns.str.strip()
    dados_cadastrais.columns = dados_cadastrais.columns.str.strip()

    # Renomear as colunas para garantir consistência
    if 'Nomes' in aptidao_fisica.columns:
        aptidao_fisica.rename(columns={'Nomes': 'Nome'}, inplace=True)
    
    if 'nome' in dados_cadastrais.columns:
        dados_cadastrais.rename(columns={'nome': 'Nome'}, inplace=True)
    
    if 'turma' in dados_cadastrais.columns:
        dados_cadastrais.rename(columns={'turma': 'Turma'}, inplace=True)

    # Verificar se as colunas necessárias estão presentes
    if 'Nome' not in aptidao_fisica.columns or 'Nome' not in dados_cadastrais.columns or 'Turma' not in dados_cadastrais.columns:
        st.error("As colunas 'Nome' ou 'Turma' não estão presentes em ambas as planilhas.")
    else:
        # Mesclar as duas planilhas com base na coluna 'Nome'
        tabela = pd.merge(aptidao_fisica, dados_cadastrais[['Nome', 'Turma']], on='Nome', how='left')

        # Definir as colunas necessárias
        colunas_necessarias = [
            'Nome', 'Turma', 'Shuttle run', 'Velocidade / aceleração',
            'Tempo de reação direita', 'Tempo de reação 1 direita',
            'Tempo de reação 2 direita', 'Tempo de reação 3 direita',
            'Tempo de reação esquerda', 'Tempo de reação 1 esquerda',
            'Tempo de reação 2 esquerda', 'Tempo de reação 3 esquerda'
        ]

        # Filtrar as colunas presentes na tabela
        colunas_faltantes = [coluna for coluna in colunas_necessarias if coluna not in tabela.columns]
        if colunas_faltantes:
            st.error(f"Colunas faltantes no arquivo: {', '.join(colunas_faltantes)}")
        else:
            tabela = tabela[colunas_necessarias]

            # Seleciona a turma
            turmas = sorted(tabela['Turma'].dropna().unique())
            selected_turma = st.selectbox('Selecione a Turma', turmas)

            # Filtra alunos da turma selecionada
            turma_data = tabela[tabela['Turma'] == selected_turma]

            # Ordena os alunos em ordem alfabética
            turma_data = turma_data.sort_values(by='Nome')

            # Seleciona o aluno
            selected_aluno = st.selectbox('Selecione o aluno', sorted(turma_data['Nome'].unique()))

            # Filtra dados do aluno selecionado
            aluno_data = turma_data[turma_data['Nome'] == selected_aluno]

            # Seleciona as colunas para exibir
            colunas_disponiveis = [coluna for coluna in colunas_necessarias if coluna in tabela.columns][2:]  # Exclui 'Nome' e 'Turma'
            colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)

            # Converte colunas selecionadas para numérico, forçando erros a NaN
            for coluna in colunas_selecionadas:
                if coluna in turma_data.columns:
                    turma_data[coluna] = pd.to_numeric(turma_data[coluna], errors='coerce')
                if coluna in aluno_data.columns:
                    aluno_data[coluna] = pd.to_numeric(aluno_data[coluna], errors='coerce')

            st.write("### Todos os Dados")
            st.dataframe(tabela[['Nome'] + colunas_selecionadas])

            st.write("### Dados do Aluno Selecionado")
            st.dataframe(aluno_data[['Nome'] + colunas_selecionadas])

            # Calcula a média da turma
            colunas_selecionadas = [col for col in colunas_selecionadas if col in turma_data.columns]
            if colunas_selecionadas:
                turma_data[colunas_selecionadas] = turma_data[colunas_selecionadas].apply(pd.to_numeric, errors='coerce')
                turma_mean = turma_data[colunas_selecionadas].mean().reset_index()
                turma_mean.columns = ['Métrica', 'Média da Turma']

                # Prepara os dados do aluno para a comparação
                aluno_data_selecionadas = aluno_data[colunas_selecionadas].melt(var_name='Métrica', value_name='Valor do Aluno')
                aluno_data_selecionadas['Nome'] = selected_aluno
                comparacao_df = pd.merge(aluno_data_selecionadas, turma_mean, on='Métrica')

                # Plotar gráfico "Dados de Tempo do Aluno"
                if colunas_selecionadas:
                    try:
                        if aluno_data[colunas_selecionadas].empty:
                            st.error("Nenhum dado disponível para o gráfico do aluno.")
                        else:
                            fig = px.bar(aluno_data, x='Nome', y=colunas_selecionadas, barmode='group', title='Dados de Tempo do Aluno', text_auto=True)
                            fig.update_layout(
                                title={
                                    'text': 'Dados de Tempo do Aluno',
                                    'x': 0.5  # Centraliza o título
                                },
                                bargap=0.3,  # Ajusta o espaço entre as barras
                                bargroupgap=0.1,  # Ajusta o espaço entre grupos de barras
                                xaxis=dict(
                                    tickfont=dict(size=14),
                                    title='Nome'
                                ),
                                yaxis=dict(
                                    tickfont=dict(size=14),
                                    title='Tempo'
                                ),
                                font=dict(size=12)
                            )

                            st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Erro ao gerar o gráfico do aluno: {e}")

                # Plotar gráfico "Comparação de Tempo do Aluno"
                if colunas_selecionadas:
                    try:
                        if comparacao_df.empty:
                            st.error("Nenhum dado disponível para a comparação com a média da turma.")
                        else:
                            fig = px.bar(comparacao_df, x='Métrica', y=['Valor do Aluno', 'Média da Turma'], barmode='group', title=f'Comparação de Tempo do Aluno ({selected_aluno}) com a Média da Turma ({selected_turma})', text_auto=True)
                            fig.update_layout(
                                title={
                                    'text': f'Comparação de Tempo do Aluno ({selected_aluno}) com a Média da Turma ({selected_turma})',
                                    'x': 0.5  # Centraliza o título
                                },
                                bargap=0.4,  # Ajusta o espaço entre as barras
                                bargroupgap=0.1,  # Ajusta o espaço entre grupos de barras
                                xaxis=dict(
                                    tickfont=dict(size=14),
                                    title='Métrica'
                                ),
                                yaxis=dict(
                                    tickfont=dict(size=14),
                                    title='Tempo'
                                ),
                                font=dict(size=12)
                            )

                            st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"Erro ao gerar o gráfico de comparação com a média da turma: {e}")

            else:
                st.warning("Nenhuma coluna selecionada para exibição.")
else:
    st.info("Carregue um arquivo Excel para visualizar os gráficos.")
