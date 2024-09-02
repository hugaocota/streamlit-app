import streamlit as st
import pandas as pd

# URL base do GitHub
base_url = "https://raw.githubusercontent.com/hugaocota/streamlit-app/main/"

# Caminhos dos arquivos no GitHub
file_path_maquinas = base_url + "Imagens/01%20-%20CATALOGO.xls"
file_path_logo = base_url + "Logo%20Rech/Logo%20Rech.jpg"
file_path_script = base_url + "Script/textos_script_venda.xlsx"

# Função para carregar o Excel das máquinas
def carregar_excel_maquinas(file_url):
    try:
        df = pd.read_excel(file_url, None)  # Carrega todas as abas como um dicionário
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")
        return None

# Função para carregar o script de vendas
def carregar_script(file_url):
    try:
        df = pd.read_excel(file_url)
        if 'Parte' not in df.columns or 'Texto' not in df.columns:
            st.error("As colunas 'Parte' e 'Texto' não foram encontradas no arquivo Excel.")
            return None
        textos_dict = df.set_index('Parte')['Texto'].to_dict()
        return textos_dict
    except Exception as e:
        st.error(f"Erro ao carregar os textos do script: {e}")
        return None

# Carregar o logo da Rech
st.image(file_path_logo, width=200)

# Carregar os dados
maquinas_dict = carregar_excel_maquinas(file_path_maquinas)
textos_dict = carregar_script(file_path_script)

# Verificar se os dados foram carregados com sucesso
if maquinas_dict and textos_dict:
    st.sidebar.title("Menu")
    menu_option = st.sidebar.radio("Selecione uma opção:", [
                                   "Script de Venda", "Máquinas", "Marcas"])

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

        st.write(f"{saudacao}, {cliente_nome}. Meu nome é {vendedor_nome}, {textos_dict.get('apresentacao', 'Texto padrão de apresentação')}")

        st.write(textos_dict.get('ramo_atuacao', "Gostaria de começar perguntando sobre o seu ramo de atuação. Qual é o segmento em que você trabalha?"))
        ramo_atuacao = st.text_input("Ramo de Atuação")

        st.write(textos_dict.get('maquina_cliente', "Entendido! Agora, poderia me informar qual máquina você está utilizando atualmente?"))
        maquina_cliente = st.selectbox("Selecione a Máquina:", list(maquinas_dict.keys()))

        # Se uma máquina foi selecionada
        if maquina_cliente:
            try:
                # Carregar os dados da aba selecionada
                df_maquina = maquinas_dict[maquina_cliente]

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
                                    st.write("Aqui estão outros itens que fazem parte do mesmo kit e que podem ser interessantes para você:")
                                    st.dataframe(itens_do_mesmo_kit, use_container_width=True)
                                    st.write("Oferecer um pacote completo desses itens pode garantir que sua máquina funcione perfeitamente por mais tempo. Podemos prosseguir com um orçamento?")
                        else:
                            st.write("Nenhum item encontrado com esse nome.")
                else:
                    st.warning(f"A coluna '{coluna_nome}' não foi encontrada na tabela da máquina selecionada.")

                # Botão para buscar imagem da máquina
                imagem_url = f"{base_url}Imagens/{maquina_cliente}/{maquina_cliente}.jpg"
                st.image(imagem_url, caption=f"Imagem da Máquina {maquina_cliente}")
            except Exception as e:
                st.error(f"Erro ao carregar os dados da máquina: {e}")

    # Opção 2: Máquinas
    elif menu_option == "Máquinas":
        st.title("Máquinas")

        # Seleção de máquina
        if maquinas_dict:
            maquina_selecionada = st.selectbox("Selecione a Máquina:", list(maquinas_dict.keys()))

            if maquina_selecionada:
                try:
                    # Carregar os dados da aba selecionada
                    df_maquina = maquinas_dict[maquina_selecionada]

                    # Remover colunas "Unnamed" e linhas que são completamente vazias
                    df_maquina = df_maquina.dropna(how='all').loc[:, ~df_maquina.columns.str.contains('^Unnamed')]

                    # Exibir os dados filtrados
                    st.title(f"Dados da Máquina: {maquina_selecionada}")
                    st.dataframe(df_maquina, use_container_width=True)

                    # Mostrar a imagem da máquina
                    imagem_url = f"{base_url}Imagens/{maquina_selecionada}/{maquina_selecionada}.jpg"
                    st.image(imagem_url, caption=f"Imagem da Máquina {maquina_selecionada}")

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
