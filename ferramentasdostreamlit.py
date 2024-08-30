import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Carrega os dados do arquivo CSV
file_path = r"C:\Users\Hugo.raposo\OneDrive - AGRO COMPETENCE\Área de Trabalho\df_final.csv"
data = pd.read_csv(file_path)

# Adiciona os filtros interligados na barra lateral
colunas_filtro = ['UF', 'NOME DO MUNICIPIO', 'BAIRRO', 'CEP', 'DESCRICAO CNAE PRINCIPAL', 'PONTUACAO DE CONFIANCA']
filtro_selecionado = {}

for idx, coluna in enumerate(colunas_filtro):
    opcoes = sorted(data[coluna].dropna().unique())
    filtro_anterior = filtro_selecionado.get(colunas_filtro[idx - 1]) if idx > 0 else None

    if filtro_anterior:
        data_filtrado = data[data[colunas_filtro[idx - 1]].isin(filtro_anterior)]
        opcoes = sorted(data_filtrado[coluna].dropna().unique())

    filtro_selecionado[coluna] = st.sidebar.multiselect(f"Selecione os valores de '{coluna}'", opcoes)

# Aplica os filtros selecionados
data_filtrado = data

for coluna, valores in filtro_selecionado.items():
    if valores:
        data_filtrado = data_filtrado[data_filtrado[coluna].isin(valores)]

# Calcula os KPIs dos dados filtrados
total_municipios = data_filtrado['NOME DO MUNICIPIO'].nunique()
total_empresas = data_filtrado['RAZAO SOCIAL'].nunique()
total_cnaes = data_filtrado['DESCRICAO CNAE PRINCIPAL'].nunique()

# Exibe os KPIs como widgets na barra lateral
st.sidebar.write("KPIs")
st.sidebar.write(f"N° de Municípios: {total_municipios} de {data['NOME DO MUNICIPIO'].nunique()}")
st.sidebar.write(f"N° de Empresas: {total_empresas} de {data['RAZAO SOCIAL'].nunique()}")
st.sidebar.write(f"N° de CNAEs: {total_cnaes} de {data['DESCRICAO CNAE PRINCIPAL'].nunique()}")

# Adiciona o título e o subtítulo
st.title("Encontre aqui o prestador de serviços ideal para a sua necessidade:")
st.subheader("São mais de 180 mil prestadores no estado de Santa Catarina!")

# Exibe os dados filtrados na tabela principal
st.subheader("Tabela de Dados Filtrados")
colunas_visiveis = ['RAZAO SOCIAL','NOME FANTASIA','NOME DO MUNICIPIO', 'BAIRRO', 'TIPO DE LOGRADOURO', 'LOGRADOURO', 'NUMERO', 'COMPLEMENTO', 'CEP', 'DESCRICAO CNAE PRINCIPAL', 'DESCRICAO CNAE SECUNDARIA', 'DDD 1', 'TELEFONE 1', 'DDD 2', 'TELEFONE 2', 'CORREIO ELETRONICO', 'PONTUACAO DE CONFIANCA']
st.write(data_filtrado[colunas_visiveis])

# Verifica se pelo menos um município foi selecionado no filtro 'NOME DO MUNICIPIO'
if filtro_selecionado['NOME DO MUNICIPIO']:
    # Exibe o mapa de Santa Catarina
    st.subheader("Mapa de Santa Catarina")
    m = folium.Map(location=[-27.595378, -48.548556], zoom_start=7)

    # Adiciona marcadores para cada ponto no mapa
    for index, row in data_filtrado.iterrows():
        latitude = row['LATITUDE']
        longitude = row['LONGITUDE']
        if not pd.isnull(latitude) and not pd.isnull(longitude):
            folium.Marker([latitude, longitude], popup=row['NOME DO MUNICIPIO']).add_to(m)

    folium_static(m)
else:
    st.info("Por favor, selecione pelo menos um município no filtro 'NOME DO MUNICIPIO' para exibir o mapa.")
