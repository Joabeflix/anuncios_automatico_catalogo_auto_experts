import re
from globals import PADROES_SUBS_ATE_60


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



