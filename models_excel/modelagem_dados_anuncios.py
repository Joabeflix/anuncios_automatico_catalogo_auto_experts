import re
from typing import TypedDict
from globals import PADROES_SUBS_NOME_ANUNCIO
import re
from globals import PADROES_SUBS_ATE_60
from tipos.tipos import CriarNomeAnuncioTipo, RetornoNomeAnuncioTipo

def deixar_nome_ate_60_caracteres(nome_produto: str, codigo_produto: str, marca: str) -> str:

    palavras_para_substituir = PADROES_SUBS_ATE_60

    def acertar_nomes(x: str) -> str:
        return str(x).upper().replace("  ", " ")
    
    def verificar_tamanho(nome: str) -> bool:
        return True if len(nome) < 61 else False
    
    def retorno_final(x: str) -> str:
        return x.title().rstrip().replace("///", "").replace("//", "").replace("   ", " ").replace("  ", " ")
    
    nome_produto = acertar_nomes(nome_produto)
    codigo_produto = acertar_nomes(codigo_produto)
    marca = acertar_nomes(marca)
    
    nome_novo = nome_produto.replace("  ", " ")

    if verificar_tamanho(nome_novo):
        return retorno_final(nome_novo)
    
    nome_novo = nome_novo.replace(codigo_produto, "")
    nome_novo = nome_novo.replace("  ", " ")

    if verificar_tamanho(nome_novo):
        return retorno_final(nome_novo)
    
    nome_novo = nome_novo.replace(marca, "")
    nome_novo = nome_novo.replace("  ", " ")

    if verificar_tamanho(nome_novo):
        return retorno_final(nome_novo)
    
    for palavra in palavras_para_substituir:
        if palavra not in nome_novo:
            continue
        if verificar_tamanho(nome_novo):
            return retorno_final(nome_novo)
        nome_novo = nome_novo.replace(palavra, palavras_para_substituir.get(palavra))

    if verificar_tamanho(nome_novo):
        return retorno_final(nome_novo)
    

    def remover_conteudo_parenteses(texto: str) -> str:
        """
        Função para remover dados que temos entre parentezes dos nomes... ex: 
        "Amortecedor De Suspensão Compatível Puma 7900 (Serie 10 / X10) 1981-2005 Diant / Tras"
        vira:
        "Amortecedor De Suspensão Compatível Puma 7900 981-2005 Diant / Tras"
        """
        return re.sub(r"\([^)]*\)", "", texto)

    nome_novo = remover_conteudo_parenteses(nome_novo)

    return retorno_final(nome_novo)






# Aux
def verificar_e_substituir_nome_padrao(nome_padrao: str) -> str:
    nome_padrao = str(nome_padrao).lower()
    return PADROES_SUBS_NOME_ANUNCIO.get(nome_padrao, nome_padrao)
def extrair_primeira_data(veiculo: str) -> str:
    "Uso essa função exatamente para pagar o primeiro nome de um"
    "Veículo que tem no nome e usamos para concatenar no nome anuncio"
    match = re.search(r'\b(19|20)\d{2}-(19|20)\d{2}\b', veiculo)
    if match:
        return veiculo[:match.end()]
    return veiculo





def f_nome_anuncio(dados_produto: CriarNomeAnuncioTipo) -> RetornoNomeAnuncioTipo:
    grupo_produto = verificar_e_substituir_nome_padrao(dados_produto["grupo_produto"])
    aplicacao = extrair_primeira_data(dados_produto["aplicacao"])
    posicao = dados_produto["posicao"]
    lado = dados_produto["lado"]
    marca = dados_produto["marca"]
    part_number = dados_produto["part_number"]
    nome = f'{grupo_produto} Compatível {aplicacao} {posicao} {lado} {marca} {part_number}'.title()
    nome = " ".join(nome.replace('None', ' ').split()).title()
    nome_ate_60 = deixar_nome_ate_60_caracteres(nome_produto=nome, codigo_produto=part_number, marca=marca)

    retorno = {"nome_anuncio": nome, "nome_ate_60_caracteres": nome_ate_60}
    print(retorno)
    return {"nome_anuncio": nome, "nome_ate_60_caracteres": nome_ate_60}