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
    try:
        desempenho_academico = pd.read_excel(uploaded_file, sheet_name='desempenho acadêmico', nrows=350)
        dados_cadastrais = pd.read_excel(uploaded_file, sheet_name='Dados Cadastrais')
        
        desempenho_academico.columns = desempenho_academico.columns.str.strip()
        dados_cadastrais.columns = dados_cadastrais.columns.str.strip()
        
        if 'Nomes' in desempenho_academico.columns:
            desempenho_academico.rename(columns={'Nomes': 'Nome'}, inplace=True)
            
    except Exception as e:
        st.error(f"Erro ao ler a planilha de dados: {e}")
        st.stop()
            
    if 'Nome' not in desempenho_academico.columns or 'Nome' not in dados_cadastrais.columns:
        st.error("A coluna 'Nome' não está presente em ambas as planilhas.")
    else:
        tabela = pd.merge(desempenho_academico, dados_cadastrais[['Nome', 'Turma']], on='Nome', how='left')
        tabela['Turma'] = tabela['Turma'].fillna('').astype(str)
        turmas = sorted(set(tabela['Turma'].str.strip()) - {''}, key=str.lower)
    
    colunas_necessarias = [
        'Nome', 'Turma', 'Desempenho acadêmico 1 bimestre',
        'Desempenho acadêmico 2 bimestre', 'Desempenho acadêmico 3 bimestre',
        'Desempenho acadêmico 4 bimestre'
    ]

    colunas_faltantes = [coluna for coluna in colunas_necessarias if coluna not in tabela.columns]
    
    if colunas_faltantes:
        st.error(f"Colunas faltantes no arquivo: {', '.join(colunas_faltantes)}")
    else:
        tabela = tabela[colunas_necessarias]
       
        try:
            with open('/mount/src/projeto-python---big-data/Big-data/style.css') as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except FileNotFoundError:
            st.error("Arquivo de estilo não encontrado.")

        selected_turma = st.selectbox('Selecione a Turma', turmas)
        turma_data = tabela[tabela['Turma'] == selected_turma]
        turma_data = turma_data.sort_values(by='Nome')
        selected_aluno = st.selectbox('Selecione o aluno', turma_data['Nome'].unique())
        aluno_data = turma_data[turma_data['Nome'] == selected_aluno]
        
        if 'Idade -Cálculo média' in aluno_data.columns:
            idade_aluno = aluno_data['Idade -Cálculo média'].values[0]
        else:
            idade_aluno = None
        
        colunas_disponiveis = [coluna for coluna in colunas_necessarias if coluna in tabela.columns][2:]
        colunas_selecionadas = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis, default=colunas_disponiveis)

        for coluna in colunas_selecionadas:
            aluno_data[coluna] = pd.to_numeric(aluno_data[coluna], errors='coerce')
            turma_data[coluna] = pd.to_numeric(turma_data[coluna], errors='coerce')

        colunas_a_exibir = ['Nome', 'Turma', 'Idade -Cálculo média'] + colunas_selecionadas
        colunas_a_exibir = [coluna for coluna in colunas_a_exibir if coluna in aluno_data.columns]
        
        st.write(f"### Dados Cadastrais do Aluno: {selected_aluno} - Idade: {idade_aluno} - Turma: {aluno_data['Turma'].values[0]}")
        st.dataframe(aluno_data[colunas_a_exibir])
        
        turma_mean = turma_data[colunas_selecionadas].mean().reset_index()
        turma_mean.columns = ['Bimestre', 'Média da Turma']
        
        aluno_data_selecionadas = aluno_data[colunas_selecionadas].melt(var_name='Bimestre', value_name='Nota do Aluno')
        aluno_data_selecionadas['Nome'] = selected_aluno
        
        comparacao_df = pd.merge(aluno_data_selecionadas, turma_mean, on='Bimestre')

        if idade_aluno is not None:
            st.write(f"**Idade do Aluno:** {idade_aluno} anos")
        else:
            st.error("Coluna 'Idade -Cálculo média' não encontrada nos dados do aluno.")

        if colunas_selecionadas:
            try:
                if comparacao_df.empty:
                    st.error("Nenhum dado disponível para a comparação com a média da turma.")
                else:
                    fig = px.bar(comparacao_df, x='Bimestre', y=['Nota do Aluno', 'Média da Turma'], barmode='group', title=f'Comparação de Desempenho do Aluno ({selected_aluno}) com a Média da Turma ({selected_turma})', text_auto=True)
                    fig.update_layout(
                        title={
                            'text': f'Comparação de Desempenho do Aluno ({selected_aluno}) com a Média da Turma ({selected_turma})',
                            'x': 0.25
                        },
                        bargap=0.4,
                        bargroupgap=0.1,
                        xaxis=dict(
                            tickfont=dict(size=14),
                            title='Bimestre'
                        ),
                        yaxis=dict(
                            tickfont=dict(size=14),
                            title='Nota'
                        ),
                        font=dict(size=12)
                    )
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de comparação: {e}")

else:
    st.warning("Por favor, carregue um arquivo Excel.")
