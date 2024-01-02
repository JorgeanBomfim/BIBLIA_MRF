import streamlit as st
import yaml
from funcoes import *


# Função para verificar as credenciais
def verificar_credenciais(username, senha):
    # Carregar credenciais do arquivo YAML
    with open('config.yaml') as file:
        credenciais = yaml.load(file, Loader=yaml.FullLoader)

    # Verificar se o usuário e senha são válidos
    for usuario in credenciais.get('usuarios', []):
        if usuario['username'] == username and usuario['senha'] == senha:
            return True, usuario['email']
    
    return False, None

# Página de login
def login():
    st.title('Login')
    username = st.text_input('Username:')
    senha = st.text_input('Senha:', type='password')
    
    if st.button('Login'):
        autenticado = verificar_credenciais(username, senha)
        if autenticado:            
            # Atualiza os parâmetros da URL para /pagina_principal
            st.experimental_set_query_params(auth_status=True, username=username)


        else:
            st.error('Credenciais inválidas')





# Roteamento entre páginas
auth_status = st.experimental_get_query_params().get('auth_status', [''])[0]
if  auth_status:
    pagina_principal()

else:
    login()