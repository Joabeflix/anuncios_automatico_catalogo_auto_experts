import json
from dotenv import load_dotenv
import os
load_dotenv()

with open(rf'configs\mapeamentos_substituicoes_ate_60.json', 'r', encoding='utf-8') as f:
    PADROES_SUBS_ATE_60 = json.load(f)

with open(rf'configs\padroes_substituicoes_nome_anuncio.json', 'r', encoding='utf-8') as f:
    PADROES_SUBS_NOME_ANUNCIO = json.load(f)

with open(rf'configs\mapeamento_falta_atributo.json', 'r', encoding='utf-8') as f:
    MAPEAMENTO_FALTA_ATRIBUTO = json.load(f)

with open(rf'configs\token.json', 'r', encoding='utf-8') as f:
    token = json.load(f)

class ConfigKeys:
    CLIENTKEY='CLIENTKEY'
    CLIENTSECRET='CLIENTSECRET'
    TEMA='TEMA'

CLIENTKEY=os.environ[ConfigKeys.CLIENTKEY]
CLIENTSECRET=os.environ[ConfigKeys.CLIENTSECRET]
TEMA=os.environ[ConfigKeys.TEMA]
TOKEN=token['token']


# CLIENTKEY=dados_config['clientkey']
# CLIENTSECRET=dados_config['clientsecret']
# TOKEN=dados_config['token']
# TEMA=dados_config['tema']



