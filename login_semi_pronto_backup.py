import streamlit as st
import yaml
from funcoes import *


# Função para verificar as credenciais
def verificar_credenciais(username, senha):
    # Carregar credenciais do arquivo YAML
    with open('config.yaml') as file:
        credenciais = yaml.load(file, Loader=yaml.FullLoader)

    # Verificar se as credenciais são válidas
    usuarios = credenciais.get('usuarios', {})
    usuario = next((u for u in usuarios if u.get('username') == username), None)

    if usuario and usuario.get('senha') == senha:
        return True, usuario.get('email')

    return False, None

# Inicializar st.session_state
if 'username' not in st.session_state:
    st.session_state.username = None

# Página de login
def login():
    st.title('Login')
    username = st.text_input('Username:')
    senha = st.text_input('Senha:', type='password')
    
    if st.button('Login'):
        autenticado, email = verificar_credenciais(username, senha)
        if autenticado:            
            st.experimental_set_query_params(auth_status=True, username=username)
            st.session_state.username = username

            st.success(f" Credênciais validadas, seja Bem-Vindo(a) {username}")
            if st.button("Entrar"):
                pass
                pagina_principal()

        else:
            st.error('Credenciais inválidas')


# Roteamento entre páginas
auth_status = st.experimental_get_query_params().get('auth_status', [''])[0]
if  auth_status:
    pagina_principal()

else:
    login()