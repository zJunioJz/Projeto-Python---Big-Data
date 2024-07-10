import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Desempenho Acadêmico", page_icon="", layout="wide")

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
st.success("Acompanhamento do Desempenho Acadêmico")

# Carregador de arquivos na barra lateral
uploaded_file = st.sidebar.file_uploader("Carregar arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Leitura dos dados cadastrais
    try:
        dados_cadastrais = pd.read_excel(uploaded_file, sheet_name='Dados Cadastrais', nrows=351)
        dados_cadastrais.columns = dados_cadastrais.columns.str.strip()
        dados_cadastrais = dados_cadastrais[['Nome', 'Sexo', 'Turma', 'Idade -Cálculo média']]
        st.write("### Dados Cadastrais Carregados")
        st.dataframe(dados_cadastrais.head())
    except Exception as e:
        st.error(f"Erro ao ler a planilha de dados cadastrais: {e}")
        st.stop()
    
    # Leitura da planilha de desempenho acadêmico
    try:
        desempenho_academico = pd.read_excel(uploaded_file, sheet_name='desempenho acadêmico', nrows=50)
        desempenho_academico.columns = desempenho_academico.columns.str.strip()
        if 'Nomes' in desempenho_academico.columns:
            desempenho_academico.rename(columns={'Nomes': 'Nome'}, inplace=True)
        st.write("### Desempenho Acadêmico Carregado")
        st.dataframe(desempenho_academico.head())
    except Exception as e:
        st.error(f"Erro ao ler a planilha de desempenho acadêmico: {e}")
        st.stop()
    
    # Definir as colunas necessárias
    colunas_necessarias = [
        'Nome', 'Desempenho acadêmico 1 bimestre',
        'Desempenho acadêmico 2 bimestre', 'Desempenho acadêmico 3 bimestre',
        'Desempenho acadêmico 4 bimestre'
    ]

    # Filtrar as colunas presentes na tabela
    colunas_presentes = [coluna for coluna in colunas_necessarias if coluna in desempenho_academico.columns]
    
    if len(colunas_presentes) != len(colunas_necessarias):
        st.error(f"As seguintes colunas necessárias estão ausentes: {[col for col in colunas_necessarias if col not in desempenho_academico.columns]}")
    else:
        # Mesclar as duas planilhas com base na coluna 'Nome'
        tabela = pd.merge(desempenho_academico, dados_cadastrais[['Nome', 'Turma']], on='Nome', how='left')

        # Remove valores NaN na coluna 'Turma'
        tabela = tabela.dropna(subset=['Turma'])

        # Converte a coluna 'Turma' para string e remove espaços em branco
        tabela['Turma'] = tabela['Turma'].astype(str).str.strip()

        # Verifica e exibe todas as turmas únicas para depuração
        turmas_unicas = tabela['Turma'].unique()
        st.write("### Turmas Únicas Detectadas")
        st.write(turmas_unicas)

        # Ordena as turmas, considerando que valores numéricos são priorizados
        def sort_key(value):
            try:
                return (not value.replace('.', '', 1).isdigit(), float(value))
            except ValueError:
                return (True, value)  # Caso não seja numérico, coloca no final

        turmas_ordenadas = sorted(set(turmas_unicas), key=sort_key)
        st.write("### Turmas Ordenadas")
        st.write(turmas_ordenadas)

        # Aplica o estilo do arquivo CSS
        try:
            with open('/mount/src/projeto-python---big-data/Big-data/style.css') as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("Arquivo de estilo não encontrado.")

        # Seleciona a turma
        selected_turma = st.selectbox('Selecione a Turma', turmas_ordenadas)

        # Filtra alunos da turma selecionada
        turma_data = tabela[tabela['Turma'] == selected_turma]

        # Verifica e exibe as primeiras linhas dos dados da turma selecionada para depuração
        st.write("### Dados da Turma Selecionada")
        st.dataframe(turma_data.head())

        # Seleciona o aluno
        selected_aluno = st.selectbox('Selecione o aluno', turma_data['Nome'].unique())

        # Filtra dados do aluno selecionado
        aluno_data = turma_data[turma_data['Nome'] == selected_aluno]

        # Seleciona as colunas para exibir
        colunas_selecionadas = [
            'Desempenho acadêmico 1 bimestre',
            'Desempenho acadêmico 2 bimestre',
            'Desempenho acadêmico 3 bimestre',
            'Desempenho acadêmico 4 bimestre'
        ]
        
        # Converte colunas selecionadas para numérico, forçando erros a NaN
        for coluna in colunas_selecionadas:
            if coluna in aluno_data.columns and coluna in turma_data.columns:
                aluno_data[coluna] = pd.to_numeric(aluno_data[coluna], errors='coerce')
                turma_data[coluna] = pd.to_numeric(turma_data[coluna], errors='coerce')
            else:
                st.error(f"A coluna {coluna} não está presente nos dados do aluno ou da turma.")
                continue

        # Exibe os dados cadastrais do aluno selecionado
        st.write(f"### Dados Cadastrais do Aluno: {selected_aluno}")
        dados_aluno = dados_cadastrais[dados_cadastrais['Nome'] == selected_aluno]
        st.dataframe(dados_aluno)

        # Exibe a idade do aluno
        if 'Idade -Cálculo média' in dados_aluno.columns:
            idade_aluno = dados_aluno['Idade -Cálculo média'].values[0]
            st.write(f"**Idade do Aluno:** {idade_aluno} anos")
        else:
            st.error("Coluna 'Idade' não encontrada nos dados do aluno.")

        # Prepara os dados do aluno para a comparação
        aluno_data_selecionadas = aluno_data[colunas_selecionadas].melt(var_name='Bimestre', value_name='Nota do Aluno')
        aluno_data_selecionadas['Nome'] = selected_aluno

        # Calcula a média da turma para cada bimestre
        turma_mean = turma_data[colunas_selecionadas].mean().reset_index()
        turma_mean.columns = ['Bimestre', 'Média da Turma']

        # Combina os dados do aluno e a média da turma
        comparacao_df = pd.merge(aluno_data_selecionadas, turma_mean, on='Bimestre')

        # Plotar gráfico "Comparação de Desempenho do Aluno"
        if colunas_selecionadas:
            try:
                if comparacao_df.empty:
                    st.error("Nenhum dado disponível para a comparação com a média da turma.")
                else:
                    fig = px.bar(comparacao_df, x='Bimestre', y=['Nota do Aluno', 'Média da Turma'], barmode='group', title=f'Comparação de Desempenho do Aluno(a) ({selected_aluno}) com a Média da Turma ({selected_turma})', text_auto=True)
                    fig.update_layout(
                        xaxis=dict(
                            tickfont=dict(size=20)
                        ),
                        yaxis=dict(
                            tickfont=dict(size=20)
                        ),
                        font=dict(size=15)
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de comparação: {e}")

else:
    st.warning("Por favor, carregue um arquivo Excel.")
