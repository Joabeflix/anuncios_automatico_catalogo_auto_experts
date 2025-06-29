import pandas as pd
import requests
import re

from utils.utils import (
    texto_no_console,
    tela_aviso,
    medir_tempo_execucao,
    selecionar_pasta
)
from utils.utils_acertar_nome import deixar_nome_ate_60_caracteres
from models_api.api_max import puxar_dados_produto_api, puxar_dados_veiculos_api
from models_api.gerar_token import TokenGerador
from globals import PADROES_SUBS_NOME_ANUNCIO
from models_excel.excel_utils import Exel


class Gerar_Anuncios:
    def __init__(
        self,
        planilha,
        funcao_atualizar_barra_geral,
        funcao_atualizar_barra_anuncio,
        local_salvar_imagens,
        baixar_img=True
    ):
        self.planilha = planilha
        self.baixar_img = baixar_img
        self.funcao_atualizar_barra_geral = funcao_atualizar_barra_geral
        self.funcao_atualizar_barra_anuncio = funcao_atualizar_barra_anuncio
        self.local_salvar_imagens = local_salvar_imagens

    def extrair_primeira_data(self, veiculo):
        match = re.search(r'\b(19|20)\d{2}-(19|20)\d{2}\b', veiculo)
        if match:
            return veiculo[:match.end()]
        return veiculo

    @medir_tempo_execucao
    def gerar_planilha(self):
        self.funcao_atualizar_barra_geral(0)

        planilha_funcoes = Exel(arquivo_excel=self.planilha)
        planilha_aberta = planilha_funcoes.abrir()
        coluna_codigo = planilha_aberta['Cod Produto']
        qtd_produtos = len(coluna_codigo)

        texto_no_console(f'Total de produtos para criar anúncio: {qtd_produtos}')

        qtd_feita = 1
        dados_puxar = [
            'nome', 'grupo_produto', 'aplicacao', 'marca',
            'part_number', 'ean', 'posicao', 'lado',
            'imagem_url', 'veiculos', 'ncm', 'garantia',
            'peso', 'altura_embalagem', 'largura_embalagem',
            'comprimento_embalagem', 'qtd_embalagem', 'similares'
        ]

        dados_inserir = {
            "nome_anuncio": [],
            "ean": [],
            "nome_ate_60": [],
            "descricao_completa_ecommerce": [],
            "descricao_completa": [],
            "descricao_simplificada": [],
            "similares_feito": [],
            "posicao": [],
            "lado": [],
            "ncm": [],
            "garantia": [],
            "peso": [],
            "altura_embalagem": [],
            "largura_embalagem": [],
            "comprimento_embalagem": [],
            "qtd_embalagem": []
        }

        for cod in coluna_codigo:
            texto_no_console(f'Gerando dados do código {cod}.')

            dados_anuncio_api = puxar_dados_produto_api(
                codigo_produto=cod,
                dados_necessarios=dados_puxar
            )

            if not dados_anuncio_api:
    
                for coluna in dados_inserir.keys():
                    dados_inserir[coluna] = "Sem dados"
                qtd_feita += 1
                continue

            @medir_tempo_execucao
            def gerar_aplicacao_veiculo():
                texto_no_console(f'Gerando aplicação do código {dados_anuncio_api["part_number"]}')
                lista_de_veiculos_crua = dados_anuncio_api['veiculos']

                lista_veiculos_api = puxar_dados_veiculos_api(
                    lista_veiculos=lista_de_veiculos_crua,
                    funcao_atualizar_barra_anuncio=self.funcao_atualizar_barra_anuncio
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
                        texto_no_console(f"Erro ao montar aplicação para veículo: {e}")

                lista_similares = []
                for item in dados_anuncio_api['similares']:
                    try:
                        lista_similares.append(f"{item['marca']['nome']}: {item['partNumber']}")
                    except Exception as e:
                        texto_no_console(f"Erro ao montar os similares: {e}")

                texto_no_console('Aplicação montada com sucesso!')
                texto_no_console('Tempo demorado para gerar a aplicação:')

                linhas_similares = (
                    f"\n\nCódigos similares:\n{'\n'.join(lista_similares)}"
                    if lista_similares else ''
                )

                dados_anuncio_api["descricao_completa"] = "\n".join(linhas_aplicacao)
                dados_anuncio_api["similares_feito"] = "\n".join(lista_similares)

                return f"{'\n'.join(linhas_aplicacao)}{linhas_similares}"

            _nome_anuncio = (
                f'{self.verificar_e_substituir_nome_padrao(dados_anuncio_api['grupo_produto'])} Compatível {self.extrair_primeira_data(dados_anuncio_api['aplicacao'])} '
                f'{dados_anuncio_api['posicao']} {dados_anuncio_api['lado']} {dados_anuncio_api['marca']} {dados_anuncio_api['part_number']}'
            ).title()

            nome_anuncio = " ".join(_nome_anuncio.replace('None', ' ').split()).title()
            nome_ate_60 = deixar_nome_ate_60_caracteres(nome_anuncio, dados_anuncio_api['part_number'], dados_anuncio_api['marca'])
            aplicacao_simplificada = (
                f"Produto: {dados_anuncio_api['nome']}\nMarca: {dados_anuncio_api['marca']}\n"
                f"Código Produto: {dados_anuncio_api['part_number']}\n\nCompatível com os veículos:\n{dados_anuncio_api['aplicacao']}"
            )
            aplicacao_completa = (f'{aplicacao_simplificada}\n\n\n\nAplicação detalhada:\n{gerar_aplicacao_veiculo()}')

            dados_anuncio_api["nome_anuncio"] = nome_anuncio
            dados_anuncio_api["nome_ate_60"] = nome_ate_60
            dados_anuncio_api["descricao_completa_ecommerce"] = aplicacao_completa
            dados_anuncio_api["descricao_simplificada"] = aplicacao_simplificada

            texto_no_console(f'Nome gerado: {nome_ate_60}')

            for coluna in dados_inserir.keys():
                dados_inserir[coluna].append(dados_anuncio_api[coluna])

            try:
                if self.baixar_img:
                    self.baixar_imagem(
                        url=dados_anuncio_api['imagem_url'],
                        nome_arquivo=dados_anuncio_api['part_number']
                    )
            except:
                pass

            texto_no_console(f'Feito: {qtd_feita}/{qtd_produtos}.')
            texto_no_console('-')

            if self.funcao_atualizar_barra_geral:
                progresso = int((qtd_feita / qtd_produtos) * 100)
                self.funcao_atualizar_barra_geral(progresso)

            qtd_feita += 1

        texto_no_console('Selecione uma pasta para salvar os anúncios.')

        local_salvar = selecionar_pasta(
            titulo='Local para salvar o arquivo Excel',
            msg='Pasta para salvar o Excel selecionada com sucesso.'
        )

        try:
            salvar_dados = planilha_funcoes.adicionar_colunas(
                planilha=planilha_aberta,
                dados_inserir=dados_inserir,
                nome_salvar=f'{local_salvar}/anun.xlsx'
            )
        except PermissionError as e:
            tela_aviso(
                'Planilha aberta.',
                'Provavelmente você está com uma planilha de outra geração aberta, feche a planilha antes de fechar esse informativo, para salvar. Caso contrário vai ter que rodar o programa novamente.',
                'erro'
            )
            salvar_dados = planilha_funcoes.adicionar_colunas(
                planilha=planilha_aberta,
                dados_inserir=dados_inserir,
                nome_salvar=f'{local_salvar}/anun.xlsx'
            )

        texto_no_console('Planilha de anúncios gerada com sucesso!')
        texto_no_console('Tempo demorado para gerar a planilha:')

    def baixar_imagem(self, url, nome_arquivo):
        texto_no_console(f'Baixando imagem {nome_arquivo}.')
        try:
            resposta = requests.get(url)
            if resposta.status_code == 200:
                with open(f'{self.local_salvar_imagens}/{nome_arquivo}.jpg', 'wb') as f:
                    f.write(resposta.content)
                texto_no_console(f"Imagem salva como: {nome_arquivo}.")
            else:
                texto_no_console(f"Erro ao baixar imagem. Código HTTP: {resposta.status_code}")
        except Exception as e:
            texto_no_console(f"Código: {nome_arquivo} --> provavelmente não tem imagem disponível na API.")

    def verificar_e_substituir_nome_padrao(self, nome_padrao):
        nome_padrao = str(nome_padrao).lower()
        return PADROES_SUBS_NOME_ANUNCIO.get(nome_padrao, nome_padrao)

if __name__ == "__main__":
    app = Gerar_Anuncios(
        planilha='plan.xlsx',
        funcao_atualizar_barra_geral=None,
        funcao_atualizar_barra_anuncio=None,
        local_salvar_imagens='imgs'
    )
    app.gerar_planilha()
