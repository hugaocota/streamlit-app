import streamlit as st
import pandas as pd
import os

# Definir o layout como "wide" para expandir o conteúdo
st.set_page_config(layout="wide")

# Caminho para o arquivo Excel dos textos
file_path_textos = r"Script/textos_script_venda.xlsx"

# Caminho para o arquivo Excel das máquinas
file_path_machines = '01 - CATALOGO.xls'

# Caminho para a logo da empresa
logo_path = r"Logo Rech/Logo Rech.jpg"

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

# Função para substituir as variáveis nos textos
def substituir_variaveis(texto, cliente_nome, vendedor_nome, maquina_cliente):
    return texto.format(cliente_nome=cliente_nome, vendedor_nome=vendedor_nome, maquina_cliente=maquina_cliente)

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

        if textos_dict:
            texto_saudacao = substituir_variaveis(textos_dict.get('saudacao', ''), cliente_nome, vendedor_nome, '')
            st.write(f"{saudacao}, {texto_saudacao}")

            texto_introducao = textos_dict.get('introducao', '')
            st.write(texto_introducao)

            texto_pergunta_ramo = textos_dict.get('pergunta_ramo', '')
            st.write(texto_pergunta_ramo)
        else:
            st.write("Não foi possível carregar os textos do script.")

        ramo_atuacao = st.text_input("Ramo de Atuação")

        st.write("Entendido! Agora, poderia me informar qual máquina você está utilizando atualmente?")
        maquina_cliente = st.selectbox("Selecione a Máquina:", abas, index=abas.index("KOM D50"))

        # Se uma máquina foi selecionada
        if maquina_cliente:
            try:
                df_maquina = pd.read_excel(xls, sheet_name=maquina_cliente)

                df_maquina = df_maquina.dropna(
                    how='all').loc[:, ~df_maquina.columns.str.contains('^Unnamed')]

                texto_pergunta_maquina = substituir_variaveis(textos_dict.get('pergunta_maquina', ''), '', '', maquina_cliente)
                st.write(texto_pergunta_maquina)

                # Botão para carregar a imagem da máquina
                if st.button("Mostrar Imagem da Máquina"):
                    imagem_url = buscar_imagem_maquina(maquina_cliente)
                    st.image(imagem_url, caption=f"Imagem da Máquina {maquina_cliente}", use_column_width=True)

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

                    # Botão para carregar a imagem da máquina
                    if st.button("Mostrar Imagem da Máquina"):
                        imagem_url = buscar_imagem_maquina(maquina_selecionada)
                        st.image(imagem_url, caption=f"Imagem da Máquina {maquina_selecionada}", use_column_width=True)

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

