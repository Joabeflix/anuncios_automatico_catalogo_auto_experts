import re
from typing import TypedDict
from globals import PADROES_SUBS_NOME_ANUNCIO
import re
from globals import PADROES_SUBS_ATE_60
from tipos.tipos import CriarNomeAnuncioTipo, RetornoNomeAnuncioTipo, CriarDescricaoTipo, RetornoDescricaoTipo
from models_api.api_max import puxar_dados_veiculos_api

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
    return {"nome_anuncio": nome, "nome_ate_60_caracteres": nome_ate_60}

def f_similares(dict_similares: dict) -> str | None:
    lista_similares = []
    for item in dict_similares:
        try:
            lista_similares.append(f"{item['marca']['nome']}: {item['partNumber']}")
        except Exception as e:
            print(f"Erro ao gerar similares: {e}")
    if lista_similares:
        print(f"debug: similares = {lista_similares}")
        return "\n".join(lista_similares)


def f_descricoes(dados_produto: CriarDescricaoTipo, funcao_atualizar_barra_anuncio) -> RetornoDescricaoTipo:
    lista_de_veiculos_crua = dados_produto["veiculos"]
    lista_veiculos_api = puxar_dados_veiculos_api(
        lista_veiculos=lista_de_veiculos_crua,
        funcao_atualizar_barra_anuncio=funcao_atualizar_barra_anuncio
    )
    linhas_aplicacao = []
    for veiculo, ano_aplicacao in zip(lista_veiculos_api, lista_de_veiculos_crua):
        try:
            marca = veiculo.get('marca', '')
            nome = veiculo.get('nome', '')
            modelo = veiculo.get('modelo', '')
            motorizacao = veiculo.get('motorizacao', {})
            motor_nome = motorizacao.get('nome', '')
            cilindrada = motorizacao.get('cilindrada', '')
            configuracao = motorizacao.get('configuracao', '')
            potencia = motorizacao.get('potenciaCv', '')
            anos = f"{ano_aplicacao.get('anoInicial', '')}-{ano_aplicacao.get('anoFinal', '')}"
            linha = f"{marca} {nome} {modelo} {anos} - Motor: {motor_nome} {cilindrada}cc {configuracao} {potencia}cv"
            if linha.strip() in linhas_aplicacao:
                continue
            linhas_aplicacao.append(linha.strip())
        except Exception as e:
            print(f"Erro ao montar aplicação para veículo: {e}")

    similares = f_similares(dados_produto['similares'])

    aplicacao_completa_inicio = (
        f"Produto: {dados_produto["nome"]}\nMarca: {dados_produto["marca"]}\n"
        f"Código Produto: {dados_produto['part_number']}\n\nCompatível com os veículos:\n"
    )
    descricao_completa_ecommerce = f'{aplicacao_completa_inicio}{"\n".join(linhas_aplicacao)}'
    if similares:
        descricao_completa_ecommerce += f'\n\n Códigos Similares:\n{similares}'
        return {"descricao_completa_ecommerce": descricao_completa_ecommerce, "aplicacao": f'{"\n".join(linhas_aplicacao)}'}
    return {"descricao_completa_ecommerce": descricao_completa_ecommerce, "aplicacao": f'{"\n".join(linhas_aplicacao)}'}
