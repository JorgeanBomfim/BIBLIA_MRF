import pandas as pd
import requests 
import streamlit as st
import json
from funcoes import *

api_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlR1ZSBKYW4gMDIgMjAyNCAxODo0OTozNyBHTVQrMDAwMC42NTgwODliNjA0NDIxNzAwMmI4ODRkNzYiLCJpYXQiOjE3MDQyMjEzNzd9.zycy2SPmHrf84lbalv7PCvIODKzEC0EkwMJrKjOkKHo"
def retono_versoes():
    ## consulta de livros, capitulos 
    url_versao = 'https://www.abibliadigital.com.br/api/versions'
    # Faça a requisição GET com o token no cabeçalho
    headers = {'Authorization': f'Bearer {api_token}'}
    response = requests.get(url_versao, headers=headers)

    # Verifique se a requisição foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Parseie a resposta JSON
        dados_versoes = response.json()

        dados_versoes = pd.DataFrame(dados_versoes)
        versoes_br = ['acf','nvi','ra']
        dados_versoes = dados_versoes.query(f"version in {versoes_br}")
    opcoes_de_versoes = dados_versoes['version'].unique()

    return opcoes_de_versoes

@st.cache_data
def retorno_livros():
    ## consulta de livros, capitulos 
    url_livros = 'https://www.abibliadigital.com.br/api/books'
    # Faça a requisição GET com o token no cabeçalho
    headers = {'Authorization': f'Bearer {api_token}'}
    response = requests.get(url_livros, headers=headers)

    # Verifique se a requisição foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Parseie a resposta JSON
        dados_livros = response.json()

        df_livros = pd.DataFrame(dados_livros)


        # Extrair valores de 'abbrev' para colunas separadas
        df_livros['abbrev_pt'] = df_livros['abbrev'].apply(lambda x: x['pt'])
        df_livros['abbrev_en'] = df_livros['abbrev'].apply(lambda x: x['en'])

        # Descartar a coluna 'abbrev'
        df_livros.drop(['abbrev','abbrev_en'], axis=1, inplace=True)
    else:
        print(f'Erro ao os livros. Código de status: {response.status_code}')

    ## Renomeando as colunas para um melhor entendimento de variáveis
    df_livros.rename(columns={'name':'livros','testament':'testamento',
                            'chapters':'capitulo','author':'autor'},inplace=True)
    
    return df_livros



### Consultando livro, e capitulo. Utilizando a credencial gerada através do login
@st.cache_data
def buscar_livro(versao_selecionada,abreviacao,capitulo_selecionado):

    # Construa a URL com os parâmetros
    url = f'https://www.abibliadigital.com.br/api/verses/{versao_selecionada}/{abreviacao}/{capitulo_selecionado}'

    # Faça a requisição GET com o token no cabeçalho
    headers = {'Authorization': f'Bearer {api_token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parseie a resposta JSON
        dados_versiculos = response.json()

        # Exiba os versículos
        livro_nome = dados_versiculos['book']['name']
        capitulo_numero = dados_versiculos['chapter']['number']
        
        versiculos = []
        for versiculo in dados_versiculos['verses']:
            versiculos.append(f"{versiculo['number']}. {versiculo['text']}")

        # Atribua a variável para uso posterior
        texto_versiculos = {
            'livro': livro_nome,
            'capitulo': capitulo_numero,
            'versiculos': versiculos
        }

        # Exiba ou retorne os versículos
        print(f"{livro_nome} {capitulo_numero}")
        for versiculo in versiculos:
            print(versiculo)
    else:
        # Em caso de erro
        mensagem_erro = f'Erro ao obter versículos. Código de status: {response.status_code}'
        print(mensagem_erro)
        texto_versiculos = None  # Ou qualquer outro valor que faça sentido em caso de erro

    return texto_versiculos 




def pesquisar_palavra(palavra_pesquisa):
    body_pesquisar_palavra = {
        "version": 'ra',
        "search": palavra_pesquisa
    }

    url_pesquisar_palavra = 'https://www.abibliadigital.com.br/api/verses/search'
    # Faça a requisição GET com o token no cabeçalho
    headers = {'Authorization': f'Bearer {api_token}'}
    response_palavra = requests.post(url_pesquisar_palavra, headers=headers, json=body_pesquisar_palavra)

    # Lista para armazenar as strings formatadas dos resultados
    resultados_formatados = []

    # Verifique se a requisição foi bem-sucedida (código de status 200)
    if response_palavra.status_code == 200:
        # Parseie a resposta JSON
        palavra_pesquisada = response_palavra.json()

        # Itera sobre cada versículo retornado
        for versiculo in palavra_pesquisada['verses']:
            # Obtém as informações do versículo
            livro_nome_palavra = versiculo['book']['name']
            capitulo_numero_palavra = versiculo['chapter']
            versiculo_numero = versiculo['number']
            versiculo_texto = versiculo['text']

            # Adiciona a string formatada à lista de resultados
            resultados_formatados.append(
                f"{livro_nome_palavra} {capitulo_numero_palavra}:{versiculo_numero}. {versiculo_texto}"
            )

    else:
        resultados_formatados = ""

    # Retorna a lista de resultados formatados como strings
    return resultados_formatados




def pagina_principal():



    def add_bg_from_url():
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("https://images.unsplash.com/photo-1572061486732-b528a9b293a3?q=80&w=1171&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
                background-attachment: fixed;
                background-size: cover
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    add_bg_from_url() 




    # Titulo da página
    col_1, titulo_page, col_3 = st.columns([1,2,1])

    with col_1:
        pass
    with titulo_page:
        st.title("Biblia Digital MRF")

    with col_3:
        pass



    # Barra de pesquisa
    col_1, barra_pesquisa, col_3 = st.columns(3)

    with col_1:
        pass
    with barra_pesquisa:
        palavra_pesquisa = st.text_input(label='Pesquisa por palavra')

        if st.button("Pesquisar"):
            if palavra_pesquisa == "":
                resultados_formatados = ""
            elif palavra_pesquisa != "":
                # Chama a função e obtém os resultados formatados
                resultados_formatados = pesquisar_palavra(palavra_pesquisa)

            # for resultado_formatado in resultados_formatados:
            #     st.write(resultado_formatado)
        else:
            resultados_formatados = ""

    for resultado_formatado in resultados_formatados:
        st.write(resultado_formatado)


    with col_3:
        pass



    # Versao, Livro, Versciculos
    col_1, versao, livro, capitulo, col_5 = st.columns(5)
    with col_1:
        pass



    with versao:
        opcoes_de_versoes = retono_versoes()
        versao_selecionada = st.selectbox("Versao", opcoes_de_versoes)

    with livro:
        df_livros = retorno_livros()
        opcoes_de_livros = df_livros['livros'].unique()
        livro_selecionado = st.selectbox("Livro",opcoes_de_livros)
            ### Seleção da abreviação do livro
        abreviacao = df_livros.query(f"livros == '{livro_selecionado}'").loc[:,['abbrev_pt']].iloc[0,0]


    with capitulo:
        opcoes_de_livros = df_livros['livros'].unique()
        qnt_de_capit_do_livro_selec = df_livros.query(f"livros == '{livro_selecionado}'").loc[:,'capitulo'].iloc[-1]
        opcoes_de_capitulos = list(range(1, qnt_de_capit_do_livro_selec + 1))
        capitulo_selecionado = st.selectbox(" Capitulo ", opcoes_de_capitulos)



    with col_5:
        pass


    # Retorno API
    containter = st.container()
    with containter:
        _, retorno_api = st.columns([0.1,1])
        with retorno_api:
            if st.button("Buscar"):
                # texto_versiculos = buscar_livro(versao_selecionada,abreviacao,capitulo_selecionado)
                dados_versiculos = buscar_livro(versao_selecionada, abreviacao, capitulo_selecionado)

                # Exibe os versículos no Streamlit
                st.write(f"{dados_versiculos['livro']} {dados_versiculos['capitulo']}")
                for versiculo in dados_versiculos['versiculos']:
                    st.write(versiculo)



