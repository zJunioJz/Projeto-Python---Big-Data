import pandas as pd
import streamlit as st
import plotly.express as px

tabela = pd.read_excel('Dados.xlsx', sheet_name='Medidas antropométricas', nrows=350)
tabela = tabela[['Nome', 'IMC', 'Peso', 'Estatura']]
tabela['IMC'] = pd.to_numeric(tabela['IMC'], errors='coerce').fillna(0)
tabela['Peso'] = pd.to_numeric(tabela['Peso'], errors='coerce').fillna(0)
tabela['Estatura'] = pd.to_numeric(tabela['Estatura'], errors='coerce').fillna(0)

tabela2 = pd.read_excel('Dados.xlsx', sheet_name='Dados Cadastrais', nrows=351)
tabela2 = tabela2[['Nome', 'Sexo', 'Turma', 'Idade -Cálculo média']]

st.title('Dados Antropométricos')

selected_aluno = st.selectbox('Selecione o aluno', tabela['Nome'].unique())

filtered_data = tabela[tabela['Nome'] == selected_aluno]

st.subheader(f'IMC, Peso e Estatura de {selected_aluno}')
bar_fig = px.bar(filtered_data, x='Nome', y=['IMC', 'Peso', 'Estatura'],
                 barmode='group', title=f'IMC, Peso e Estatura de {selected_aluno}')
bar_fig.update_layout(
    plot_bgcolor='white',
    xaxis_title='Nome',
    yaxis_title='Valores',
    legend_title_text='Métricas',
    bargap=0.2, 
    bargroupgap=0.1 
)
st.plotly_chart(bar_fig)


st.subheader('Relação entre Estatura e Peso')
scatter_fig = px.scatter(tabela, x='Estatura', y='Peso', color='IMC', hover_name='Nome',
                         title='Relação entre Estatura e Peso', labels={'Estatura': 'Estatura (cm)', 'Peso': 'Peso (kg)'})
scatter_fig.update_layout(
    plot_bgcolor='white',
    xaxis_title='Estatura (cm)',
    yaxis_title='Peso (kg)'
)
st.plotly_chart(scatter_fig)


st.subheader('Distribuição do IMC dos Alunos')
histogram_fig = px.histogram(tabela, x='IMC', nbins=30, title='Distribuição do IMC dos Alunos')
histogram_fig.update_layout(
    plot_bgcolor='white',
    xaxis_title='IMC',
    yaxis_title='Frequência',
    bargap=0.1 
)
st.plotly_chart(histogram_fig)

st.subheader('Distribuição de Sexo')
color_discrete_map = {'M': 'Blue', 'F': 'pink'}
histogram_fig = px.histogram(tabela2, x='Turma',nbins=30,color='Sexo',title='Distribuição do sexo por turma',
                              color_discrete_map=color_discrete_map)
histogram_fig.update_layout(
    plot_bgcolor='white',
    xaxis_title='Sexo',
    yaxis_title='Frequência',
    bargap=0.1 
)
st.plotly_chart(histogram_fig)

st.subheader('Média da Idade Total das Turmas')
cores = {'11': 'green','12':'yellow','13': 'blue'}
fig = px.pie(tabela2,names='Idade -Cálculo média',title="Distribuição das Idades",color_discrete_map=cores)
fig.update_layout(
    plot_bgcolor='white',
    xaxis_title='Idade',
    yaxis_title='Frequência',
    bargap=0.1 
)
st.plotly_chart(fig)



#python -m streamlit run test.py