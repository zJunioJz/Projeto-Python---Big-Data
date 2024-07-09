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
    try:
        # Leitura das planilhas do arquivo Excel
        aptidao_fisica = pd.read_excel(uploaded_file, sheet_name='APTIDÃO FÍSICA', nrows=350)
        dados_cadastrais = pd.read_excel(uploaded_file, sheet_name='Dados Cadastrais')
        
        # Verificar e limpar nomes das colunas
        aptidao_fisica.columns = aptidao_fisica.columns.str.strip()
        dados_cadastrais.columns = dados_cadastrais.columns.str.strip()
        
        # Exibir as colunas após a leitura
        st.write("Colunas em 'APTIDÃO FÍSICA':", aptidao_fisica.columns.tolist())
        st.write("Colunas em 'Dados Cadastrais':", dados_cadastrais.columns.tolist())
        
        # Renomeia a coluna 'Nomes' para 'Nome' se necessário
        if 'Nomes' in aptidao_fisica.columns:
            aptidao_fisica.rename(columns={'Nomes': 'Nome'}, inplace=True)
        
        if 'Nome completo' in aptidao_fisica.columns:
            aptidao_fisica.rename(columns={'Nome completo': 'Nome'}, inplace=True)

    except Exception as e:
        st.error(f"Erro ao ler as planilhas: {e}")
        st.stop()

    # Verificar se a coluna 'Nome' está presente em ambas as planilhas
    if 'Nome' not in aptidao_fisica.columns or 'Nome' not in dados_cadastrais.columns or 'Turma' not in dados_cadastrais.columns:
        st.error("A coluna 'Nome' ou 'Turma' não está presente em ambas as planilhas.")
    else:
        # Mesclar as duas planilhas com base na coluna 'Nome'
        tabela = pd.merge(aptidao_fisica, dados_cadastrais[['Nome', 'Turma']], on='Nome', how='left')

        # Remove colunas duplicadas
        tabela = tabela.loc[:, ~tabela.columns.duplicated()]

        # Exibir as colunas após a mesclagem
        st.write("Colunas após mesclagem:", tabela.columns.tolist())

        # Definir as colunas necessárias (ajustado com base nas colunas disponíveis)
        colunas_necessarias = [
            'Nome', 'Turma', 'Shuttle run', 'Velocidade / aceleração', 
            'Tempo de reação direita', 'Tempo de reação 1 direita', 
            'Tempo de reação 2 direita', 'Tempo de reação 3 direita', 
            'Tempo de reação esquerda', 'Tempo de reação 1 esquerda', 
            'Tempo de reação 2 esquerda', 'Tempo de reação 3 esquerda'
        ]

        # Verificar quais colunas estão presentes
        colunas_presentes = [coluna for coluna in colunas_necessarias if coluna in tabela.columns]
        colunas_faltantes = [coluna for coluna in colunas_necessarias if coluna not in tabela.columns]

        if colunas_faltantes:
            st.warning(f"Colunas faltantes no arquivo: {', '.join(colunas_faltantes)}")

        # Atualizar colunas_necessarias para conter apenas as colunas presentes
        colunas_necessarias = colunas_presentes
        tabela = tabela[colunas_necessarias]

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

        # Exibir as colunas da turma selecionada
        st.write("Colunas da turma selecionada:", turma_data.columns.tolist())

        # Seleciona o aluno
        selected_aluno = st.selectbox('Selecione o aluno', turma_data['Nome'].unique())

        # Filtra dados do aluno selecionado
        aluno_data = turma_data[turma_data['Nome'] == selected_aluno]

        # Exibir as colunas do aluno selecionado
        st.write("Colunas do aluno selecionado:", aluno_data.columns.tolist())

        # Seleciona as colunas para exibir
        colunas_disponiveis = [coluna for coluna in colunas_necessarias if coluna not in ['Nome', 'Turma']]
        colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)

        # Verifica colunas selecionadas
        st.write("Colunas selecionadas:", colunas_selecionadas)

        # Converte colunas selecionadas para numérico, forçando erros a NaN
        for coluna in colunas_selecionadas:
            if coluna in aluno_data.columns:
                try:
                    # Verifica se a coluna é do tipo object antes de converter
                    if aluno_data[coluna].dtype == 'object':
                        aluno_data[coluna] = pd.to_numeric(aluno_data[coluna], errors='coerce')
                        turma_data[coluna] = pd.to_numeric(turma_data[coluna], errors='coerce')
                except Exception as e:
                    st.error(f"Erro ao converter a coluna {coluna}: {e}")

        # Remove colunas que não puderam ser convertidas
        aluno_data = aluno_data.dropna(axis=1, how='all')
        turma_data = turma_data.dropna(axis=1, how='all')

        # Remove colunas duplicadas após a conversão
        aluno_data = aluno_data.loc[:, ~aluno_data.columns.duplicated()]
        turma_data = turma_data.loc[:, ~turma_data.columns.duplicated()]

        st.write("### Todos os Dados")
        try:
            st.write("Colunas disponíveis na turma:", turma_data.columns.tolist())
            st.dataframe(turma_data[['Nome'] + colunas_selecionadas])
        except Exception as e:
            st.error(f"Erro ao exibir a tabela da turma: {e}")

        st.write("### Dados do Aluno Selecionado")
        try:
            st.write("Colunas disponíveis no aluno:", aluno_data.columns.tolist())
            st.dataframe(aluno_data[['Nome'] + colunas_selecionadas])
        except Exception as e:
            st.error(f"Erro ao exibir a tabela do aluno: {e}")

        # Calcula a média da turma
        try:
            # Selecione apenas as colunas numéricas para calcular a média
            colunas_numericas = turma_data[colunas_selecionadas].select_dtypes(include='number').columns
            turma_mean = turma_data[colunas_numericas].mean().reset_index()
            turma_mean.columns = ['Métrica', 'Média da Turma']
        except Exception as e:
            st.error(f"Erro ao calcular a média da turma: {e}")
            turma_mean = pd.DataFrame(columns=['Métrica', 'Média da Turma'])

        # Prepara os dados do aluno para a comparação
        try:
            aluno_data_selecionadas = aluno_data[colunas_selecionadas].melt(var_name='Métrica', value_name='Valor do Aluno')
            aluno_data_selecionadas['Nome'] = selected_aluno
            comparacao_df = pd.merge(aluno_data_selecionadas, turma_mean, on='Métrica', how='left')
        except Exception as e:
            st.error(f"Erro ao preparar os dados para a comparação: {e}")
            comparacao_df = pd.DataFrame()

        # Plotar gráfico "Dados de tempo do aluno"
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
                        bargap=0.4,  # Ajusta o espaço entre as barras
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

                    for trace in fig.data:
                        trace.width = 0.30

                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de dados do aluno: {e}")

        # Plotar gráfico "Comparação com a média da turma"
        if comparacao_df.empty:
            st.error("Nenhum dado disponível para a comparação com a média da turma.")
        else:
            try:
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

                for trace in fig.data:
                    trace.width = 0.30

                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de comparação: {e}")

else:
    st.warning("Por favor, carregue um arquivo Excel.")
