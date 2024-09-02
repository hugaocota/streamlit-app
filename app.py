import streamlit as st
import pandas as pd
import requests

# Definir o layout como "wide" para expandir o conteúdo
st.set_page_config(layout="wide")

# Caminhos para os arquivos no GitHub
file_path = "https://github.com/hugaocota/streamlit-app/raw/main/Script/textos_script_venda.xlsx"
logo_path = "https://github.com/hugaocota/streamlit-app/raw/main/Logo%20Rech/Logo%20Rech.jpg"
file_path_maquinas = "https://github.com/hugaocota/streamlit-app/raw/main/Imagens/01%20-%20CATALOGO.xls"

# Função para carregar os textos do Excel
def carregar_textos(file_path):
    try:
        st.write(f"Carregando arquivo de textos do caminho: {file_path}")
        textos_df = pd.read_excel(file_path)
        st.write(f"Colunas encontradas no arquivo: {textos_df.columns}")
        
        if 'Parte' not in textos_df.columns or 'Texto' not in textos_df.columns:
            st.error("As colunas 'Parte' e 'Texto' não foram encontradas no arquivo Excel.")
            return None
        else:
            return textos_df.set_index('Parte')['Texto'].to_dict()
    except Exception as e:
        st.error(f"Erro ao carregar os textos do script: {e}")
        return None

# Carregar os textos do script
textos_dict = carregar_textos(file_path)

# Verificar se a logo foi carregada corretamente e exibi-la na parte superior direita
try:
    st.image(logo_path, width=150, use_column_width=False)
except Exception as e:
    st.error(f"Erro ao carregar a logo: {e}")

# Verificar se o arquivo de máquinas existe e carregar as máquinas
try:
    st.write(f"Carregando arquivo de máquinas do caminho: {file_path_maquinas}")
    xls = pd.ExcelFile(file_path_maquinas)
    abas = xls.sheet_names  # Lista com os nomes das abas

    # Remover a primeira aba da lista, se não for necessária
    if abas:
        abas = abas[1:]

except Exception as e:
    st.error(f"Erro ao ler o arquivo Excel: {e}")

# Menu lateral com opções principais
st.sidebar.title("Menu")
menu_option = st.sidebar.radio("Selecione uma opção:", ["Script de Venda", "Máquinas", "Marcas"])

# Opção 1: Script de Venda
if menu_option == "Script de Venda":
    st.title("Simulação de Interação de Venda")

    # Apresentação do vendedor
    st.subheader("Apresentação do Vendedor")
    vendedor_nome = st.text_input("Seu Nome")
    saudacao = st.radio("Escolha uma saudação:", ["Bom dia", "Boa tarde", "Boa noite"])

    # Saudação e pergunta inicial
    cliente_nome = st.text_input("Nome do Cliente")
    cliente_empresa = st.text_input("Empresa do Cliente")

    if textos_dict:
        st.write(f"{saudacao}, {cliente_nome}. Meu nome é {vendedor_nome}, {textos_dict.get('apresentacao', 'Texto padrão de apresentação')}")

    st.write("Gostaria de começar perguntando sobre o seu ramo de atuação. Qual é o segmento em que você trabalha?")
    ramo_atuacao = st.text_input("Ramo de Atuação")

    st.write("Entendido! Agora, poderia me informar qual máquina você está utilizando atualmente?")
    maquina_cliente = st.selectbox("Selecione a Máquina:", abas)

    # Se uma máquina foi selecionada
    if maquina_cliente:
        try:
            # Carregar os dados da aba selecionada
            df_maquina = pd.read_excel(xls, sheet_name=maquina_cliente)

            # Remover colunas "Unnamed" e linhas que são completamente vazias
            df_maquina = df_maquina.dropna(how='all').loc[:, ~df_maquina.columns.str.contains('^Unnamed')]

            st.write(f"Ótimo! Trabalhar com {maquina_cliente} é sempre uma escolha sólida. Agora, vamos ver como podemos ajudar a manter sua máquina em perfeitas condições.")

            # Campo de seleção dinâmica para a coluna "DESCRIÇÃO/ KOMATSU D50"
            coluna_nome = "DESCRIÇÃO/ KOMATSU D50"
            if coluna_nome in df_maquina.columns:
                itens_lista = df_maquina[coluna_nome].dropna().unique().tolist()
                item_pesquisado = st.selectbox("Pesquise o item desejado:", [""] + itens_lista)

                if item_pesquisado:
                    itens_filtrados = df_maquina[df_maquina[coluna_nome] == item_pesquisado]
                    if not itens_filtrados.empty:
                        st.write(f"Você selecionou o item '{item_pesquisado}'. Este é um excelente produto que pode contribuir muito para o desempenho da sua máquina.")

                        # Sugerir itens do mesmo kit
                        if 'KIT' in df_maquina.columns:
                            kit_do_item = itens_filtrados['KIT'].values[0]
                            itens_do_mesmo_kit = df_maquina[df_maquina['KIT'] == kit_do_item]
                            if not itens_do_mesmo_kit.empty:
                                st.write("Aqui estão outros itens que fazem parte do mesmo kit e
