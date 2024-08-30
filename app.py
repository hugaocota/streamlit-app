import streamlit as st
import pandas as pd
import os
import requests

# Definir o layout como "wide" para expandir o conteúdo
st.set_page_config(layout="wide")

# Caminho para o arquivo Excel
file_path = '01 - CATALOGO.xls'

# Função para buscar imagem da máquina no Unsplash
def buscar_imagem_unsplash(maquina):
    access_key = "J8RWiEJ0nMNT1zvfLDTrzXdrVDSyiX8iVY5a770DXAQ"
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": f"Máquina {maquina}",
        "client_id": access_key,
        "per_page": 1  # Retornar apenas uma imagem
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if data["results"]:
        return data["results"][0]["urls"]["regular"]
    else:
        return None

# Verificar se o arquivo existe
if not os.path.exists(file_path):
    st.error("O arquivo Excel não foi encontrado.")
else:
    # Ler todas as abas da planilha em um dicionário
    try:
        xls = pd.ExcelFile(file_path)
        abas = xls.sheet_names  # Lista com os nomes das abas

        # Remover a primeira aba da lista, se não for necessária
        if abas:
            abas = abas[1:]

    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")

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

        st.write(f"{saudacao}, {cliente_nome}. Meu nome é {vendedor_nome}, da empresa [Nome da Empresa]. É um prazer falar com você! Estamos sempre prontos para ajudar nossos clientes com as melhores soluções em peças e serviços.")

        st.write(
            "Gostaria de começar perguntando sobre o seu ramo de atuação. Qual é o segmento em que você trabalha?")
        ramo_atuacao = st.text_input("Ramo de Atuação")

        st.write(
            "Entendido! Agora, poderia me informar qual máquina você está utilizando atualmente?")
        maquina_cliente = st.selectbox("Selecione a Máquina:", abas)

        # Se uma máquina foi selecionada
        if maquina_cliente:
            try:
                # Carregar os dados da aba selecionada
                df_maquina = pd.read_excel(xls, sheet_name=maquina_cliente)

                # Remover colunas "Unnamed" e linhas que são completamente vazias
                df_maquina = df_maquina.dropna(
                    how='all').loc[:, ~df_maquina.columns.str.contains('^Unnamed')]

                st.write(f"Ótimo! Trabalhar com {maquina_cliente} é sempre uma escolha sólida. Agora, vamos ver como podemos ajudar a manter sua máquina em perfeitas condições.")

                # Campo de seleção dinâmica para a coluna "DESCRIÇÃO/ KOMATSU D50"
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

                            # Sugerir itens do mesmo kit
                            if 'KIT' in df_maquina.columns:
                                kit_do_item = itens_filtrados['KIT'].values[0]
                                itens_do_mesmo_kit = df_maquina[df_maquina['KIT']
                                                                == kit_do_item]
                                if not itens_do_mesmo_kit.empty:
                                    st.write(
                                        "Aqui estão outros itens que fazem parte do mesmo kit e que podem ser interessantes para você:")
                                    st.dataframe(itens_do_mesmo_kit,
                                                 use_container_width=True)
                                    st.write(
                                        "Oferecer um pacote completo desses itens pode garantir que sua máquina funcione perfeitamente por mais tempo. Podemos prosseguir com um orçamento?")
                        else:
                            st.write("Nenhum item encontrado com esse nome.")
                else:
                    st.warning(f"A coluna '{coluna_nome}' não foi encontrada na tabela da máquina selecionada.")

                # Botão para buscar imagem da máquina
                if st.button("Buscar Imagem da Máquina"):
                    imagem_url = buscar_imagem_unsplash(maquina_cliente)
                    if imagem_url:
                        st.image(imagem_url, caption=f"Imagem da Máquina {maquina_cliente}")
                    else:
                        st.write("Nenhuma imagem encontrada para esta máquina.")

            except Exception as e:
                st.error(f"Erro ao carregar os dados da máquina: {e}")

    # Opção 2: Máquinas
    elif menu_option == "Máquinas":
        st.title("Máquinas")

        # Remover a primeira aba do filtro, se for o menu que não tem serventia
        if abas:
            maquinas_filtradas = abas
            maquina_selecionada = st.selectbox(
                "Selecione a Máquina:", maquinas_filtradas)

            if maquina_selecionada:
                try:
                    # Carregar os dados da aba selecionada
                    df_maquina = pd.read_excel(
                        xls, sheet_name=maquina_selecionada)

                    # Remover colunas "Unnamed" e linhas que são completamente vazias
                    df_maquina = df_maquina.dropna(
                        how='all').loc[:, ~df_maquina.columns.str.contains('^Unnamed')]

                    # Exibir os dados filtrados
                    st.title(f"Dados da Máquina: {maquina_selecionada}")
                    st.dataframe(df_maquina, use_container_width=True)

                    # Botão para buscar imagem da máquina
                    if st.button("Buscar Imagem da Máquina"):
                        imagem_url = buscar_imagem_unsplash(
                            maquina_selecionada)
                        if imagem_url:
                            st.image(imagem_url, caption=f"Imagem da Máquina {maquina_selecionada}")
                        else:
                            st.write(
                                "Nenhuma imagem encontrada para esta máquina.")

                except Exception as e:
                    st.error(f"Erro ao carregar os dados da máquina: {e}")

    # Opção 3: Marcas
    elif menu_option == "Marcas":
        st.title("Marcas")
        marcas = ["Marca A", "Marca B", "Marca C"]  # Exemplo de marcas
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

