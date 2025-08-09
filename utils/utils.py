import os
import time
import json
import numpy as np
from typing import Any
from tkinter import messagebox
from tkinter.filedialog import askdirectory

def texto_no_console(obj: str | list) -> None:
    separadores = ['_', '*', '-', '#']
    if obj in separadores:
        print(obj * 130)
        return None
    if isinstance(obj, list):
        for t in obj:
            if t == '\n':
                print('\n')
                continue
            print(f'>>> {t}{'\n'}')
        return None
    print(f'>>> {obj}{'\n'}')

def alterar_valor_json(caminho_json: str, chave: str, novo_valor: str | float) -> None:
    with open(file=caminho_json, mode='r', encoding='utf8') as arquivo:
        dados = json.load(arquivo)
    dados[chave] = novo_valor
    with open(file=caminho_json, mode='w', encoding='utf8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

def retorno_dados_json(caminho_json: str, chaves: list[str] | str, se_nao_encontrar: str | float | None = None) -> list[str] | str | float | None:
    """
    Lê um arquivo JSON e retorna o valor da chave fornecida.

    Parâmetros:
        caminho_arquivo (str): Caminho para o arquivo JSON.
        chave (str): Chave a ser buscada.
        padrao: Valor padrão caso a chave não seja encontrada.

    Retorna:
        Valor correspondente à chave, ou valor padrão se não encontrado.
    """
    try:
        if isinstance(chaves, list):
            with open(caminho_json, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return [dados.get(x, se_nao_encontrar) for x in chaves]


        with open(caminho_json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            texto_no_console('Lendo o arquivo json')
        return dados.get(chaves, se_nao_encontrar)
    
    except FileNotFoundError:
        print(f"Arquivo '{caminho_json}' não encontrado.")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar o arquivo JSON: '{caminho_json}'")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    return se_nao_encontrar

def tela_aviso(titulo: str, mensagem: str, tipo: str) -> None:

    tipos = {
        "informacao": messagebox.showinfo,
        "erro": messagebox.showerror
    }
    if tipo in tipos.keys():
        tipos[tipo](title=titulo, message=mensagem)
    else:
        texto_no_console([
            f'Tipo de tela não cadastrado na função: {tipo}', 
            f'Tipos cadastrados: {list(tipos.keys())}'])

def converter_int64_para_int(obj: Any) -> Any:
    """ Se não for int64 ele retorna o valor original."""
    if isinstance(obj, np.integer):
        return int(obj)
    return obj

def limpar_prompt() -> None:
    os.system('cls')

def medir_tempo_execucao(funcao):
    def wrapper(*args, **kwargs):

        inicio = time.perf_counter()
        resultado = funcao(*args, **kwargs)
        fim = time.perf_counter()
        _tempo_demorado = f"{fim - inicio:.0f}"
        tempo_demorado_total = int(_tempo_demorado)

        if tempo_demorado_total < 60:
            texto_no_console(f"Tempo: {tempo_demorado_total} segundos.")
            return resultado
        
        minutos = tempo_demorado_total // 60
        segundos = tempo_demorado_total % 60

        texto_no_console(f"Tempo: {minutos} minutos e {segundos} segundos.")
        return resultado
    return wrapper


def selecionar_pasta(titulo: str, msg: str| None=None) -> str:
    pasta = askdirectory(title=titulo)
    if pasta:
        texto_no_console(f"{msg}")
        return pasta
    tela_aviso('Erro', 'Você precisa selecionar um local para salvar!', 'erro')
    return selecionar_pasta(titulo=titulo, msg=msg)

if __name__ == "__main__":
    tela = tela_aviso(titulo='Teste', mensagem='Oi, está mensagem é de teste. Rs!', tipo='erro')
