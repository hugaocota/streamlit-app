import streamlit as st
import pandas as pd
import requests

# Definir o layout como "wide" para expandir o conteúdo
st.set_page_config(layout="wide")

# URLs dos arquivos no GitHub
logo_url = "https://github.com/hugaocota/streamlit-app/blob/main/Logo%20Rech/Logo%20Rech.jpg?raw=true"
excel_url = "https://github.com/hugaocota/streamlit-app/blob/main/Script/textos_script_venda.xlsx?raw=true"

# Função para carregar o Excel a partir de uma URL
def carregar_excel(url):
    df = pd.read_excel(url)
    return df

# Função para carregar a imagem a partir de uma URL
def carregar_imagem(url):
    return url

# Carregar logo
st.image(carregar_imagem(logo_url), width=150)

# Carregar textos do script
try:
    df_textos = carregar_excel(excel_url)
    textos_dict = pd.Series(df_textos.Texto.values,index=df_textos.Parte).to_dict()
except Exception as e:
    st.error(f"Erro ao carregar os textos do script: {e}")
    textos_dict = {}

# Função para buscar imagem da máquina
def buscar_imagem_maquina(maquina_nome):
    imagem_url = f"https://github.com/hugaocota/streamlit-app/blob/main/Imagens/{maquina_nome}/{maquina_nome}.jpg?raw=true"
    return imagem_url

# Menu lateral com opções principais
st.sidebar.title("Menu")
menu_option = st.sidebar.radio("Selecione uma opção:", [
                               "Script de Venda", "Máquinas", "Marcas"])

# Opção 1: Script de Venda
if menu_option == "Script de Venda":
    st.title("Simulação de Interação de Venda")

    # Apresentação do vendedor
    st.subheader("Apresentação do Vendedor")
    vendedor_nome = st.text_input("Seu Nome")
    saudacao = st.radio("Escolha uma saudação:", [
                        "Bom dia", "Boa tarde", "Boa noite"])

    # Saudação e pergunta inicial
    cliente_nome = st.text_input("Nome do Cliente")
    cliente_empresa = st.text_input("Empresa do Cliente")

    st.write(f"{saudacao}, {cliente_nome}. Meu nome é {vendedor_nome}, {textos_dict.get('apresentacao', 'Texto padrão de apresentação')}")

    st.write("Gostaria de começar perguntando sobre o seu ramo de atuação. Qual é o segmento em que você trabalha?")
    ramo_atuacao = st.text_input("Ramo de Atuação")

    st.write("Entendido! Agora, poderia me informar qual máquina você está utilizando atualmente?")
    maquina_cliente = st.text_input("Nome da Máquina")

    # Se uma máquina foi selecionada
    if maquina_cliente:
        try:
            # Carregar a imagem da máquina
            imagem_url = buscar_imagem_maquina(maquina_cliente)
            if imagem_url:
                st.image(imagem_url, caption=f"Imagem da Máquina {maquina_cliente}")
            else:
                st.write("Nenhuma imagem encontrada para esta máquina.")
        except Exception as e:
            st.error(f"Erro ao carregar a imagem da máquina: {e}")

# Opção 2: Máquinas
elif menu_option == "Máquinas":
    st.title("Máquinas")
    st.write("Informações sobre máquinas estarão disponíveis aqui.")

# Opção 3: Marcas
elif menu_option == "Marcas":
    st.title("Marcas")
    st.write("Informações sobre marcas estarão disponíveis aqui.")
