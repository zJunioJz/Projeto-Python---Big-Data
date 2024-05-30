import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar layout da página
st.set_page_config(page_title="Home", page_icon="", layout="wide")

# Tabs para Medidas fisiológicas e Medidas antropométricas
tab1, tab2 = st.tabs(["Medidas fisiológicas", "Medidas antropométricas"])

# Código para Medidas fisiológicas
with tab1:
    st.success("**Medidas fisiológicas**")

    # Carregar dados do Excel
    tabela_fisio = pd.read_excel('Dados.xlsx', sheet_name='Medidas fisiológicas', nrows=350)
    tabela_fisio = tabela_fisio[['Turma','Nome','FC rep','PA rep','FCmáx polar','FCmáx teste','Teste FC','FCmáx prev.','FC Polar leve','FC Polar mod.','FC Polar méd.','FC Polar forte','FC Polar máx','FCteste leve','FCteste mod.','FCteste méd.','FCteste forte','FCteste máx','FCprev leve','FCprev mod.','FCprev méd.','FCprev forte','FCprev máx']]

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
    colunas_disponiveis_fisio = ['FC rep','PA rep','FCmáx polar','FCmáx teste','Teste FC','FCmáx prev.','FC Polar leve','FC Polar mod.','FC Polar méd.','FC Polar forte','FC Polar máx','FCteste leve','FCteste mod.','FCteste méd.','FCteste forte','FCteste máx','FCprev leve','FCprev mod.','FCprev méd.','FCprev forte','FCprev máx']
    colunas_selecionadas_fisio = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis_fisio, default=colunas_disponiveis_fisio)

    st.write("### Todos os Dados")
    st.dataframe(tabela_fisio[colunas_selecionadas_fisio])

    # Mostrar os dados do aluno selecionado com as colunas selecionadas
    st.write("### Dados do Aluno Selecionado")
    st.dataframe(aluno_data_fisio[['Nome'] + colunas_selecionadas_fisio])

    # Visualização com Plotly para o aluno selecionado, com colunas específicas
    colunas_grafico_fisio = ['FC rep', 'PA rep', 'FCmáx polar', 'FCmáx teste', 'Teste FC']
    if colunas_grafico_fisio:
        fig_fisio = px.bar(aluno_data_fisio, x='Nome', y=colunas_grafico_fisio, barmode='group', title='Dados Fisiológicos do Aluno')
        st.plotly_chart(fig_fisio, use_container_width=True)

# Código para Medidas antropométricas
with tab2:
    st.success("**Medidas antropométricas**")

    # Carregar dados do Excel
    tabela_antropo = pd.read_excel('Dados.xlsx', sheet_name='Medidas antropométricas', nrows=350)
    tabela_antropo = tabela_antropo[['Nome', 'IMC', 'Peso', 'Estatura']]
    
    # Converter colunas para tipo numérico
    for col in tabela_antropo.columns[1:]:
        tabela_antropo[col] = pd.to_numeric(tabela_antropo[col], errors='coerce')

    # Carregar estilo CSS
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Selecionar aluno
    selected_aluno_antropo = st.selectbox('Selecione o aluno', tabela_antropo['Nome'].unique())

    # Filtrar dados do aluno selecionado
    aluno_data_antropo = tabela_antropo[tabela_antropo['Nome'] == selected_aluno_antropo]

    # Selecionar colunas para exibir
    colunas_disponiveis_antropo = ['IMC', 'Peso', 'Estatura']
    colunas_selecionadas_antropo = st.multiselect("Selecione as colunas para exibir", colunas_disponiveis_antropo, default=colunas_disponiveis_antropo)

    # Mostrar todos os dados na tabela completa
    st.write("### Todos os Dados")
    st.dataframe(tabela_antropo)

    # Mostrar os dados do aluno selecionado com as colunas selecionadas
    st.write("### Dados do Aluno Selecionado")
    st.dataframe(aluno_data_antropo[['Nome'] + colunas_selecionadas_antropo])

    # Visualização com Plotly para o aluno selecionado, se houver colunas selecionadas
    if colunas_selecionadas_antropo:
        fig_antropo = px.bar(aluno_data_antropo, x='Nome', y=colunas_selecionadas_antropo, barmode='group', title='Dados Antropométricos do Aluno')
        st.plotly_chart(fig_antropo, use_container_width=True)
