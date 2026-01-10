import json
import os


# 'configs\mapeamentos_substituicoes_ate_60.json'
with open(os.path.join("configs", "mapeamentos_substituicoes_ate_60.json"), 'r', encoding='utf-8') as f:
    PADROES_SUBS_ATE_60 = json.load(f)

# 'configs\padroes_substituicoes_nome_anuncio.json',
with open(os.path.join("configs", "padroes_substituicoes_nome_anuncio.json"), 'r', encoding='utf-8') as f:
    PADROES_SUBS_NOME_ANUNCIO = json.load(f)

# 'configs\mapeamento_falta_atributo.json'
with open(os.path.join("configs", "mapeamento_falta_atributo.json"), 'r', encoding='utf-8') as f:
    MAPEAMENTO_FALTA_ATRIBUTO = json.load(f)

# configs\configuracoes.json'
with open(os.path.join("configs", "configuracoes.json"), 'r', encoding='utf-8') as f:
    dados_config = json.load(f)

CLIENTKEY=dados_config['clientkey']
CLIENTSECRET=dados_config['clientsecret']
TOKEN=dados_config['token']
TEMA=dados_config['tema']

