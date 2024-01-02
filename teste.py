import requests


def obter_token_de_autenticacao():
    url_autenticacao = 'https://www.abibliadigital.com.br/api/users/token'

    # Dados de autenticação
    dados_autenticacao = {
        "email": "Jorgeanteste@email.com",
        "password": "12345678"
    }

    # Faça a requisição POST para obter o token
    response = requests.put(url_autenticacao, json=dados_autenticacao)

    # Verifique se a requisição foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        # Parseie a resposta JSON e retorne o token
        resultado_json = response.json()
        token = resultado_json.get('token')
        return token
    else:
        # Exiba uma mensagem de erro caso a requisição não tenha sido bem-sucedida
        print(f'Erro ao obter token. Código de status: {response.status_code}')
        return None

# Exemplo de uso
token_autenticacao = obter_token_de_autenticacao()
api_token = token_autenticacao
# Verifique se o token foi obtido com sucesso
if token_autenticacao:
    print(f'Token de autenticação: {token_autenticacao}')
    print(token_autenticacao)
else:
    print('Falha na autenticação.')
