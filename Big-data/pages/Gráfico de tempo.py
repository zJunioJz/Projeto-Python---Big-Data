import streamlit as st
import pandas as pd
import plotly.express as px

# Função para limpar e converter coluna para numérico
def clean_column(series):
    if not isinstance(series, pd.Series):
        raise TypeError("A entrada deve ser uma série (pd.Series).")
    
    if series.dtype == 'object':  # Verifica se a série é do tipo 'object'
        series = series.replace({',': '.'}, regex=True)  # Substitui vírgulas por pontos
        series = series.str.replace(r'[^\d.]+', '', regex=True)  # Remove caracteres não numéricos, exceto ponto
    return pd.to_numeric(series, errors='coerce')

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
    # Leitura das planilhas do arquivo Excel
    aptidao_fisica = pd.read_excel(uploaded_file, sheet_name='APTIDÃO FÍSICA', nrows=350)
    dados_cadastrais = pd.read_excel(uploaded_file, sheet_name='Dados Cadastrais')

    # Verificar e limpar nomes das colunas
    aptidao_fisica.columns = aptidao_fisica.columns.str.strip()
    dados_cadastrais.columns = dados_cadastrais.columns.str.strip()

    # Renomear colunas para garantir consistência
    if 'Nomes' in aptidao_fisica.columns:
        aptidao_fisica.rename(columns={'Nomes': 'Nome'}, inplace=True)
    if 'nome' in dados_cadastrais.columns:
        dados_cadastrais.rename(columns={'nome': 'Nome'}, inplace=True)
    if 'Turma' not in dados_cadastrais.columns and 'turma' in dados_cadastrais.columns:
        dados_cadastrais.rename(columns={'turma': 'Turma'}, inplace=True)

    # Verificar se a coluna 'Nome' está presente em ambas as planilhas
    if 'Nome' not in aptidao_fisica.columns or 'Nome' not in dados_cadastrais.columns or 'Turma' not in dados_cadastrais.columns:
        st.error("A coluna 'Nome' ou 'Turma' não está presente em ambas as planilhas.")
    else:
        # Mesclar as duas planilhas com base na coluna 'Nome'
        tabela = pd.merge(aptidao_fisica, dados_cadastrais[['Nome', 'Turma']], on='Nome', how='left')

        # Definir as colunas necessárias (ajustado com base nas colunas disponíveis)
        colunas_necessarias = [
            'Nome', 'Turma', 'Shuttle run', 'Velocidade / aceleração', 
            'Tempo de reação direita', 'Tempo de reação 1 direita', 
            'Tempo de reação 2 direita', 'Tempo de reação 3 direita', 
            'Tempo de reação esquerda', 'Tempo de reação 1 esquerda', 
            'Tempo de reação 2 esquerda', 'Tempo de reação 3 esquerda'
        ]

        colunas_faltantes = [coluna for coluna in colunas_necessarias if coluna not in tabela.columns]

        if colunas_faltantes:
            st.warning(f"Colunas faltantes no arquivo: {', '.join(colunas_faltantes)}")
        
        # Atualizar colunas_necessarias para conter apenas as colunas presentes
        colunas_necessarias = [coluna for coluna in colunas_necessarias if coluna in tabela.columns]
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

        # Seleciona o aluno
        selected_aluno = st.selectbox('Selecione o aluno', turma_data['Nome'].unique())

        # Filtra dados do aluno selecionado
        aluno_data = turma_data[turma_data['Nome'] == selected_aluno]

        # Seleciona as colunas para exibir
        colunas_disponiveis = [coluna for coluna in colunas_necessarias if coluna not in ['Nome', 'Turma']]
        colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)
        
        # Limpeza e conversão das colunas selecionadas
        for coluna in colunas_selecionadas:
            if coluna in aluno_data.columns and coluna in turma_data.columns:
                try:
                    aluno_data[coluna] = clean_column(aluno_data[coluna])
                    turma_data[coluna] = clean_column(turma_data[coluna])
                except Exception as e:
                    st.error(f"Erro ao converter a coluna {coluna} para numérico: {e}")
                    st.stop()
            else:
                st.warning(f"A coluna {coluna} não está presente nos dados do aluno ou da turma.")

        st.write("### Todos os Dados")
        st.dataframe(turma_data[['Nome'] + colunas_selecionadas])

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

                    for trace in fig.data:
                        trace.width = 0.05

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

                    for trace in fig.data:
                        trace.width = 0.30

                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de comparação: {e}")

else:
    st.warning("Por favor, carregue um arquivo Excel.")
