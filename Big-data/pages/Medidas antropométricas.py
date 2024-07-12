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
    try:
        medidas_antropometricas = pd.read_excel(uploaded_file, sheet_name='Antropometria', nrows=350)
        dados_cadastrais = pd.read_excel(uploaded_file, sheet_name='Dados Cadastrais')
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")
        st.stop()

    # Verificar e limpar nomes das colunas
    medidas_antropometricas.columns = medidas_antropometricas.columns.str.strip()
    dados_cadastrais.columns = dados_cadastrais.columns.str.strip()

    # Renomear as colunas para garantir consistência
    if 'Nomes' in medidas_antropometricas.columns:
        medidas_antropometricas.rename(columns={'Nomes': 'Nome'}, inplace=True)
    if 'nome' in dados_cadastrais.columns:
        dados_cadastrais.rename(columns={'nome': 'Nome'}, inplace=True)
    if 'turma' in dados_cadastrais.columns:
        dados_cadastrais.rename(columns={'turma': 'Turma'}, inplace=True)

    # Verificar se a coluna 'Nome' e 'Turma' estão presentes em ambas as planilhas
    if 'Nome' not in medidas_antropometricas.columns or 'Nome' not in dados_cadastrais.columns or 'Turma' not in dados_cadastrais.columns:
        st.error("A coluna 'Nome' ou 'Turma' não está presente em ambas as planilhas.")
    else:
        # Mesclar as duas planilhas com base na coluna 'Nome'
        tabela = pd.merge(medidas_antropometricas, dados_cadastrais[['Nome', 'Turma']], on='Nome', how='left')

        # Garantir que a coluna 'Turma' não contenha valores nulos e converter para string
        tabela['Turma'] = tabela['Turma'].fillna('').astype(str)

        # Ordenar as turmas e remover valores vazios
        turmas = sorted(set(tabela['Turma'].str.strip()) - {''}, key=str.lower)

        # Seleciona a turma
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
        colunas_disponiveis = ['IMC', 'Peso', 'Estatura', 'Envergadura']
        colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)

        # Converte as colunas selecionadas para numérico, forçando erros a NaN
        for coluna in colunas_selecionadas:
            turma_data[coluna] = pd.to_numeric(turma_data[coluna], errors='coerce')
            aluno_data[coluna] = pd.to_numeric(aluno_data[coluna], errors='coerce')

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

        # Gráfico das medidas antropométricas do aluno
        if colunas_selecionadas:
            fig = px.bar(aluno_data, x='Nome', y=colunas_selecionadas, barmode='group', title=f'Medidas Antropométricas do Aluno(a) ( {selected_aluno})', text_auto=True)
            fig.update_layout(
                title={
                    'text': f'Medidas Antropométricas do Aluno(a) ( {selected_aluno})',
                    'x': 0.35  # Posição centralizada
                },
                bargap=0.50,
                bargroupgap=0.1,
                xaxis=dict(
                    tickfont=dict(size=20)
                ),
                yaxis=dict(
                    tickfont=dict(size=20)
                ),
                font=dict(size=15)
            )
            for trace in fig.data:
                    trace.width = 0.08
            st.plotly_chart(fig, use_container_width=True)

        # Gráfico de comparação entre o aluno e a média da turma
        if colunas_selecionadas:
            fig_comparacao = px.bar(comparacao_df, x='Métrica', y=['Valor do Aluno', 'Média da Turma'], barmode='group',
                                   title=f'Comparação de Medidas Antropométricas do Aluno(a) ({selected_aluno}) com a Média da Turma ({selected_turma})',
                                   text_auto=True)
            fig_comparacao.update_layout(
                title={
                     'text': f'Comparação de Medidas Antropométricas do Aluno(a) ({selected_aluno}) com a Média da Turma ( {selected_turma})',
                        'x': 0.20  # Centraliza o título
                },
                xaxis=dict(
                    tickfont=dict(size=20)
                ),
                yaxis=dict(
                    tickfont=dict(size=20)
                ),
                font=dict(size=15)
            )
            for trace in fig.data:
                trace.width = 0.05
            st.plotly_chart(fig_comparacao, use_container_width=True)

else:
    st.warning("Por favor, carregue um arquivo Excel.")
