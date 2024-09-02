import streamlit as st
import pandas as pd
<<<<<<< HEAD
import os
=======
import requests
>>>>>>> f9f955b7d75f94ee5cf21f2c06cef28dbf5194bc

# Definir o layout como "wide" para expandir o conteúdo
st.set_page_config(layout="wide")

<<<<<<< HEAD
# Caminho para o arquivo Excel dos textos
file_path_textos = r"C:\Users\Hugo.raposo\AGRO COMPETENCE\F.PARTS - Gestao\00 GESTÃO\Oportunidade de Vendas\Script\textos_script_venda.xlsx"

# Caminho para o arquivo Excel das máquinas
file_path_machines = '01 - CATALOGO.xls'

# Caminho para a logo da empresa
logo_path = r"C:\Users\Hugo.raposo\AGRO COMPETENCE\F.PARTS - Gestao\00 GESTÃO\Oportunidade de Vendas\Logo Rech\Logo Rech.jpg"

# Função para carregar textos do script a partir do Excel
def carregar_textos(file_path):
    try:
        df = pd.read_excel(file_path)
        if 'parte' in df.columns and 'texto' in df.columns:
            textos_dict = dict(zip(df['parte'], df['texto']))
            return textos_dict
        else:
            st.error("As colunas 'parte' e 'texto' não foram encontradas no arquivo Excel.")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar os textos do script: {e}")
        return None

# Carregar os textos
textos_dict = carregar_textos(file_path_textos)

# Exibir a logo da empresa no canto superior direito
if os.path.exists(logo_path):
    st.image(logo_path, width=150, use_column_width=False, clamp=True)

# Verificação do arquivo Excel das máquinas
if not os.path.exists(file_path_machines):
    st.error("O arquivo Excel não foi encontrado.")
else:
    try:
        xls = pd.ExcelFile(file_path_machines)
        abas = xls.sheet_names

        if abas:
            abas = abas[1:]
=======
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
>>>>>>> f9f955b7d75f94ee5cf21f2c06cef28dbf5194bc

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

<<<<<<< HEAD
        if textos_dict:
            st.write(f"{saudacao}, {cliente_nome}. Meu nome é {vendedor_nome}, {textos_dict.get('apresentacao', 'Texto padrão de apresentação')}")

        st.write("Gostaria de começar perguntando sobre o seu ramo de atuação. Qual é o segmento em que você trabalha?")
        ramo_atuacao = st.text_input("Ramo de Atuação")

        st.write("Entendido! Agora, poderia me informar qual máquina você está utilizando atualmente?")
        maquina_cliente = st.selectbox("Selecione a Máquina:", abas)

        # Se uma máquina foi selecionada
        if maquina_cliente:
            try:
                df_maquina = pd.read_excel(xls, sheet_name=maquina_cliente)

                df_maquina = df_maquina.dropna(
                    how='all').loc[:, ~df_maquina.columns.str.contains('^Unnamed')]

                st.write(f"Ótimo! Trabalhar com {maquina_cliente} é sempre uma escolha sólida. Agora, vamos ver como podemos ajudar a manter sua máquina em perfeitas condições.")

                coluna_nome = "DESCRIÇÃO/ KOMATSU D50"
                if coluna_nome in df_maquina.columns:
                    itens_lista = df_maquina[coluna_nome].dropna(
                    ).unique().tolist()
                    item_pesquisado = st.selectbox(
                        "Pesquise o item desejado:", [""] + itens_lista)

                    if item_pesquisado:
                        itens_filtrados = df_maquina[df_maquina[coluna_nome]
                                                     == item_pesquisado]
                        if not itens_filtrados.empty:
                            st.write(f"Você selecionou o item '{item_pesquisado}'. Este é um excelente produto que pode contribuir muito para o desempenho da sua máquina.")

                            if 'KIT' in df_maquina.columns:
                                kit_do_item = itens_filtrados['KIT'].values[0]
                                itens_do_mesmo_kit = df_maquina[df_maquina['KIT']
                                                                == kit_do_item]
                                if not itens_do_mesmo_kit.empty:
                                    st.write("Aqui estão outros itens que fazem parte do mesmo kit e que podem ser interessantes para você:")
                                    st.dataframe(itens_do_mesmo_kit,
                                                 use_container_width=True)
                                    st.write("Oferecer um pacote completo desses itens pode garantir que sua máquina funcione perfeitamente por mais tempo. Podemos prosseguir com um orçamento?")
                        else:
                            st.write("Nenhum item encontrado com esse nome.")
                else:
                    st.warning(f"A coluna '{coluna_nome}' não foi encontrada na tabela da máquina selecionada.")

            except Exception as e:
                st.error(f"Erro ao carregar os dados da máquina: {e}")

    # Opção 2: Máquinas
    elif menu_option == "Máquinas":
        st.title("Máquinas")

        if abas:
            maquinas_filtradas = abas
            maquina_selecionada = st.selectbox(
                "Selecione a Máquina:", maquinas_filtradas)

            if maquina_selecionada:
                try:
                    df_maquina = pd.read_excel(
                        xls, sheet_name=maquina_selecionada)

                    df_maquina = df_maquina.dropna(
                        how='all').loc[:, ~df_maquina.columns.str.contains('^Unnamed')]

                    st.title(f"Dados da Máquina: {maquina_selecionada}")
                    st.dataframe(df_maquina, use_container_width=True)

                except Exception as e:
                    st.error(f"Erro ao carregar os dados da máquina: {e}")

    # Opção 3: Marcas
    elif menu_option == "Marcas":
        st.title("Marcas")
        marcas = ["Marca A", "Marca B", "Marca C"]
        marca_selecionada = st.selectbox("Selecione a Marca:", marcas)
        if marca_selecionada:
            st.write(f"Informações detalhadas sobre a {marca_selecionada}.")
            st.write("""
            **Histórico:**  
            A [Marca Selecionada] é uma das líderes no mercado, conhecida pela sua qualidade e inovação.

            **Produtos Principais:**  
            - Produto 1
            - Produto 2
            - Produto 3

            **Diferenciais:**  
            - Alta durabilidade
            - Suporte técnico especializado
            - Rede de distribuição abrangente
            """)
=======
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
>>>>>>> f9f955b7d75f94ee5cf21f2c06cef28dbf5194bc
