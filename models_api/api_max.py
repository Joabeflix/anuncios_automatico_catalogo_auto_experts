import json
import requests
from utils.utils import texto_no_console, tela_aviso
from models_api.gerar_token import TokenGerador
from models_api.mapeamentos_retorno_api import mapeamento_usar
import time
from globals import MAPEAMENTO_FALTA_ATRIBUTO

class APICliente:
    BASE_URL = 'https://api.intelliauto.com.br/v1'

    def __init__(self, access_token):
        self.access_token = access_token

    def obter_dados_api(self, obj, url_path):
        url = f'{self.BASE_URL}/{url_path}/{obj}'
        headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }

        try:
            response = requests.get(url, headers=headers)
        except requests.RequestException as e:
            texto_no_console(f"Erro de conexão com API: {e}")
            return None

        if response.status_code == 401:
            texto_no_console("Erro 401: Token inválido ou expirado.")
            tela_aviso('Erro Token', 'Provavelmente o seu token de acesso é inválido ou está expirado... Vamos gerar um novo token.', 'erro')
            gerar_token = TokenGerador().definir_novo_token()
            tela_aviso('Resolvido', f'Geramos o novo token "{gerar_token}"\n\nReinicie o programa para carregar as novas configurações. \n\nSe mesmo assim o erro persistir, consultar o Joabe para validar melhor o erro.', 'informacao')
            return None

        if response.status_code == 200:
            return response

        texto_no_console(f"Erro ao acessar API: Código {response.status_code}")
        return None


class FiltroJSON:
    @staticmethod
    def filtrar_dados(data, filtro_json, item_filtro=None):
        try:
            resultado = eval(f"data{filtro_json}")
        except Exception as e:
            texto_no_console(f"{MAPEAMENTO_FALTA_ATRIBUTO.get(filtro_json, "")}")
            return ""

        if item_filtro:
            try:
                filtrados = [dado for dado in resultado if dado.get("item") == item_filtro]
                return filtrados[0].get('descricao', '')
            except (IndexError, KeyError):
                return ''

        return resultado


def puxar_dados_produto_api(access_token, codigo_produto, dados_necessarios=None):
    if dados_necessarios is None:
        dados_necessarios = []

    api_cliente = APICliente(access_token)
    filtro = FiltroJSON()

    url_path = 'produtos/partnumber'
    response = api_cliente.obter_dados_api(codigo_produto, url_path)
    if response:
        if not response:
            return {}

        try:
            dados = response.json()
        except json.JSONDecodeError:
            texto_no_console("Resposta inválida da API.")
            return {}

        if not dados.get('data'):
            # Tentativa de nova requisição
            response = api_cliente.obter_dados_api(codigo_produto, url_path)
            if not response:
                return {}
            dados = response.json()

        if not dados.get('data'):
            return {}

        retorno = {}
        for chave in dados_necessarios:
            mapeamento = mapeamento_usar(chave)
            valor = filtro.filtrar_dados(dados, mapeamento['caminho'], mapeamento.get('chave_secundaria'))
            retorno[chave] = valor

        return retorno
    return None


def puxar_dados_veiculos_api(access_token, lista_veiculos, funcao_atualizar_barra_anuncio):

    api_cliente = APICliente(access_token)
    url_path = 'veiculos/codigo'
    veiculos_completos = []

    caminho_json = rf'configs\veiculos_cache.json'

    with open(caminho_json, 'r', encoding='utf-8') as f:
        cache_veiculos = json.load(f)

    total = len(lista_veiculos)
    feito = 0

    for item in lista_veiculos:
        if funcao_atualizar_barra_anuncio:
            progresso = int((feito / total) * 100)
            funcao_atualizar_barra_anuncio(progresso)
        codigo = item.get('codigo')
        if not codigo:
            continue


        # Aqui estamos verificando se ja não adicionamos o carro no cache, pois se tiver
        # não vamos precisar fazer a requisição e assim vamos gerar o relatorio mais rapido
        # de acordo que vamos adicionando informações nele
        if codigo in cache_veiculos:
            texto_no_console('[debug] CACHE')
            veiculos_completos.append(cache_veiculos[codigo])
            feito += 1
            continue

        response = api_cliente.obter_dados_api(codigo, url_path)
        texto_no_console('[debug] API')
        time.sleep(0.2)
        if not response:
            continue

        try:
            dados = response.json()
        except json.JSONDecodeError:
            texto_no_console(f"Erro ao decodificar resposta da API para o código {codigo}.")
            continue

        if not dados:
            continue

        try:
            veiculo = {
                "id": dados.get("id"),
                "codigo": dados.get("codigo"),
                "classificacao": dados.get("classificacao"),
                "marca": dados.get("marca"),
                "nome": dados.get("nome"),
                "modelo": dados.get("modelo"),
                "inicioProducao": dados.get("inicioProducao"),
                "finalProducao": dados.get("finalProducao"),
                "mercado": dados.get("mercado", {}).get("nome", ""),
                "motorizacao": {
                    "nome": dados.get("motorizacao", {}).get("nome"),
                    "cilindrada": dados.get("motorizacao", {}).get("cilindrada"),
                    "configuracao": dados.get("motorizacao", {}).get("configuracao"),
                    "potenciaCv": dados.get("motorizacao", {}).get("potenciaCv"),
                },
                "dataAtualizacao": dados.get("dataAtualizacao")
            }

            veiculos_completos.append(veiculo)
            cache_veiculos[codigo] = veiculo

            feito += 1

        except Exception as e:
            texto_no_console(f"Erro ao processar veículo {codigo}: {e}")
            continue

    with open(caminho_json, 'w', encoding='utf-8') as f:
        json.dump(cache_veiculos, f, ensure_ascii=False, indent=2)

    return veiculos_completos





if __name__ == "__main__":
    access_token = TokenGerador().retorno_token()
    dados_gerais = puxar_dados_produto_api(access_token=access_token, codigo_produto='HG 41111', dados_necessarios=['similares'])
    print(dados_gerais)