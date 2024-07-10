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
st.success("Gráfico de tempo")

# Carregador de arquivos na barra lateral
uploaded_file = st.sidebar.file_uploader("Carregar arquivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Leitura das planilhas do arquivo Excel
    try:
        aptidao_fisica = pd.read_excel(uploaded_file, sheet_name='APTIDÃO FÍSICA', nrows=350)
        dados_cadastrais = pd.read_excel(uploaded_file, sheet_name='Dados Cadastrais')

        # Verificar e limpar nomes das colunas
        aptidao_fisica.columns = aptidao_fisica.columns.str.strip()
        dados_cadastrais.columns = dados_cadastrais.columns.str.strip()

        # Renomeia a coluna 'Nomes' para 'Nome' se necessário
        if 'Nomes' in aptidao_fisica.columns:
            aptidao_fisica.rename(columns={'Nomes': 'Nome'}, inplace=True)

    except Exception as e:
        st.error(f"Erro ao ler as planilhas: {e}")
        st.stop()

    # Verificar se a coluna 'Nome' está presente em ambas as planilhas
    if 'Nome' not in aptidao_fisica.columns or 'Nome' not in dados_cadastrais.columns:
        st.error("A coluna 'Nome' não está presente em ambas as planilhas.")
    else:
        # Mesclar as duas planilhas com base na coluna 'Nome'
        tabela = pd.merge(aptidao_fisica, dados_cadastrais[['Nome', 'Turma']], on='Nome', how='left')

        # Garantir que a coluna 'Turma' não contenha valores nulos e converter para string
        tabela['Turma'] = tabela['Turma'].fillna('').astype(str)

        # Remover valores vazios e garantir que todos os valores são strings
        turmas = sorted(set(tabela['Turma'].str.strip()) - {''}, key=str.lower)

        # Definir as colunas necessárias (ajustado com base nas colunas disponíveis)
        colunas_necessarias = [
            'Nome', 'Turma', 'Tempo Total', 'Tempo de Sustentação', 'Tempo de Abdominal', 
            'Tempo de Apoio de Frente', 'Tempo de Salto Horizontal', 'Tempo de Salto Vertical', 
            'Tempo de Preensão Manual'
        ]

        colunas_faltantes = [coluna for coluna in colunas_necessarias if coluna not in tabela.columns]

        if colunas_faltantes:
            st.error(f"Colunas faltantes no arquivo: {', '.join(colunas_faltantes)}")
        else:
            tabela = tabela[colunas_necessarias]

            # Aplica o estilo do arquivo CSS
            try:
                with open('/mount/src/projeto-python---big-data/Big-data/style.css') as f:
                    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
            except FileNotFoundError:
                st.error("Arquivo de estilo não encontrado.")

            # Seleciona a turma
            selected_turma = st.selectbox('Selecione a Turma', turmas)

            # Filtra alunos da turma selecionada
            turma_data = tabela[tabela['Turma'] == selected_turma]

            # Ordena os alunos em ordem alfabética
            turma_data = turma_data.sort_values(by='Nome')

            # Seleciona o aluno
            selected_aluno = st.selectbox('Selecione o aluno', turma_data['Nome'].unique())

            # Filtra dados do aluno selecionado
            aluno_data = turma_data[turma_data['Nome'] == selected_aluno]

            # Seleciona as colunas para exibir
            colunas_disponiveis = [coluna for coluna in colunas_necessarias if coluna in tabela.columns][2:]  # Exclui 'Nome' e 'Turma'
            colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)

            # Converte colunas selecionadas para numérico, forçando erros a NaN
            for coluna in colunas_selecionadas:
                aluno_data[coluna] = pd.to_numeric(aluno_data[coluna], errors='coerce')
                turma_data[coluna] = pd.to_numeric(turma_data[coluna], errors='coerce')

            # Ordena todos os dados em ordem alfabética pelo Nome
            tabela_sorted = tabela.sort_values(by='Nome')

            st.write("### Todos os Dados")
            st.dataframe(tabela_sorted[['Nome'] + colunas_selecionadas])

            st.write("### Dados do Aluno Selecionado")
            st.dataframe(aluno_data[['Nome'] + colunas_selecionadas])

            # Plotar gráfico "Tempo do Aluno"
            if colunas_selecionadas:
                try:
                    if aluno_data[colunas_selecionadas].empty:
                        st.error("Nenhum dado disponível para o gráfico do aluno.")
                    else:
                        fig = px.bar(aluno_data, x='Nome', y=colunas_selecionadas, barmode='group', title='Dados de Tempo do Aluno(a)', text_auto=True)
                        
                        # Atualiza o layout do gráfico para ajustar o espaçamento das barras
                        fig.update_layout(
                            xaxis=dict(
                                tickfont=dict(size=20)
                            ),
                            yaxis=dict(
                                tickfont=dict(size=20)
                            ),
                            font=dict(size=15),
                            bargap=0.2,
                            bargroupgap=0.1
                        )
                        st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Erro ao gerar o gráfico do aluno: {e}")

else:
    st.warning("Por favor, carregue um arquivo Excel.")
