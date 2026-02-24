from typing import TypedDict
"""
Abaixo temos os tipos que usamos para criar
os dados de anuncios, que fazemos separadamente
ex: nome anuncio, aplicacao e etc... tudo isso
montamos fora do arquivo core principal, por isso
deixo tudo 100% tipado, e abaixo temos os tipos

""" 








class CriarNomeAnuncioTipo(TypedDict):
    grupo_produto: str
    aplicacao: str
    posicao: str
    lado: str
    marca: str
    part_number: str

class RetornoNomeAnuncioTipo(TypedDict):
    nome_anuncio: str
    nome_ate_60_caracteres: str

class CriarDescricaoTipo(TypedDict):
    nome: str
    marca: str
    part_number: str
    veiculos: dict
    similares: dict

class RetornoDescricaoTipo(TypedDict):
    descricao_completa_ecommerce: str
    aplicacao: str


class RetornoCriarDescricaoTipo(TypedDict):
    ...

