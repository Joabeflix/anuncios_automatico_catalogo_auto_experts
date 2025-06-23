import json


with open(rf'configs\configuracoes.json', 'r', encoding='utf-8') as f:
    dados_config = json.load(f)

with open(rf'configs\mapeamentos_substituicoes_ate_60.json', 'r', encoding='utf-8') as f:
    PADROES_SUBS_ATE_60 = json.load(f)

with open(rf'configs\padroes_substituicoes_nome_anuncio.json', 'r', encoding='utf-8') as f:
    PADROES_SUBS_NOME_ANUNCIO = json.load(f)

CLIENTKEY=dados_config['clientkey']
CLIENTSECRET=dados_config['clientsecret']
TOKEN=dados_config['token']
TEMA=dados_config['tema']







