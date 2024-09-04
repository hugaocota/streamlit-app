import streamlit as st
import pandas as pd
import os
import base64

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

# Função para carregar a imagem da máquina
def carregar_imagem_maquina(maquina):
    imagem_path = f"Imagens/{maquina}/{maquina}.jpg"
    if os.path.exists(imagem_path):
        st.image(imagem_path, caption=f"Imagem da Máquina {maquina}", use_column_width=True)
    else:
        st.warning(f"Imagem para {maquina} não encontrada.")

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
            abas = abas[1:]  # Ignora a primeira aba, se necessário
            if "KOM D50" in abas:
                default_machine = "KOM D50"
            else:
                default_machine = abas[0]  # Seleciona a primeira aba como padrão se "KOM D50" não existir

    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")

    # Menu lateral com opções principais
    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio("Selecione uma opção:", [
                                   "Script de Venda", "Máquinas", "Marcas", "Venda mais", "Segmentos"])

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
            # Substituir os placeholders nos textos do script
            texto_saudacao = textos_dict.get('saudacao', 'Texto padrão de saudação')
            texto_saudacao = texto_saudacao.replace("{cliente_nome}", cliente_nome).replace("{vendedor_nome}", vendedor_nome)

            texto_introducao = textos_dict.get('introducao', 'Texto padrão de introdução')
            texto_ramo = textos_dict.get('pergunta_ramo', 'Texto padrão de pergunta sobre ramo')
            texto_maquina = textos_dict.get('pergunta_maquina', 'Texto padrão de pergunta sobre máquina')

            # Exibir os textos no script
            st.write(texto_saudacao)
            st.write(texto_introducao)
            
            ramo_atuacao = st.text_input("Ramo de Atuação")
            st.write(texto_ramo)

            maquina_cliente = st.selectbox("Selecione a Máquina:", abas, index=abas.index(default_machine))
            st.write(texto_maquina)

            # Botão para carregar a imagem da máquina
            if st.button("Mostrar Imagem da Máquina"):
                carregar_imagem_maquina(maquina_cliente)

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

                            # Sugerir itens do mesmo kit
                            if 'KIT' in df_maquina.columns:
                                kit_do_item = itens_filtrados['KIT'].values[0]
                                itens_do_mesmo_kit = df_maquina[df_maquina['KIT']
                                                                == kit_do_item]
                                if not itens_do_mesmo_kit.empty:
                                    st.write("Aqui estão outros itens que fazem parte do mesmo kit e que podem ser interessantes para você:")
                                    st.dataframe(itens_do_mesmo_kit, use_container_width=True)
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

                    # Botão para carregar a imagem da máquina
                    if st.button("Mostrar Imagem da Máquina"):
                        carregar_imagem_maquina(maquina_selecionada)

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

    # Opção 4: Venda mais (vídeos do YouTube)
    elif menu_option == "Venda mais":
        st.title("Venda Mais - Dicas e Estratégias")

        st.video("https://www.youtube.com/watch?v=PZ1uaXoINmk")
        st.video("https://www.youtube.com/watch?v=i9bfGMhryYY")
        st.video("https://www.youtube.com/watch?v=8LqBTCXBNzE")
        st.video("https://www.youtube.com/watch?v=TOp6oYruEg4")
        st.video("https://www.youtube.com/watch?v=Kh2m6prJHEU")
        st.video("https://www.youtube.com/watch?v=kaoGiCkVUHI")

    # Opção 5: Segmentos
    elif menu_option == "Segmentos":
        st.title("Segmentos - Material Rodante")

        # Botão para mostrar ou ocultar o PDF
       
