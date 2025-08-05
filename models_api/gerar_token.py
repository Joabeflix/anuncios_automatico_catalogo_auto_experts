import requests
from utils.utils import *
from globals import CLIENTKEY, CLIENTSECRET

class TokenGerador:
    def __init__(self) -> None:
        pass

    CLIENT_KEY=CLIENTKEY
    CLIENT_SECRET=CLIENTSECRET
 
    def _gerar_token(self) -> str | None:
        token_url = 'https://api.intelliauto.com.br/v1/login'
        token_payload = {
            'clientKey': CLIENTKEY,
            'clientSecret': CLIENTSECRET
        }
        texto_no_console(f'Dados enviados para gerar o novo Token: {token_payload}')
        token_response = requests.post(token_url, json=token_payload)
        if token_response.status_code == 200:
            token = token_response.json().get('accessToken')
            texto_no_console(f'Novo Token gerado: {token}')
            print(type(token))
            return token
        return None

    def definir_novo_token(self) -> str | None:
        token = self._gerar_token()
        if token:
            alterar_valor_json(rf'configs\configuracoes.json', 'token', token)
        return token
    
    """
    def ler_token(self):

    #    Essa é a única função que 

        try:
            with open(r"configs\token.txt", "r", encoding="utf-8") as arquivo:
                access_token = arquivo.read()
                return access_token
            
        except FileNotFoundError:
            self.definir_novo_token()
            self.ler_token()

    """
if __name__ == "__main__":
    app = TokenGerador()
    app.definir_novo_token()