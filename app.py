from funcoes import *


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


