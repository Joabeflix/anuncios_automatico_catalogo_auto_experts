import re
import requests
import ttkbootstrap as ttk # type: ignore
from models_excel.excel_utils import Exel
from globals import PADROES_SUBS_NOME_ANUNCIO
from utils.utils_acertar_nome import deixar_nome_ate_60_caracteres
from models_api.api_max import puxar_dados_produto_api, puxar_dados_veiculos_api
from utils.utils import texto_no_console, tela_aviso, medir_tempo_execucao, selecionar_pasta
from models_api.retornos_api_class import DadosProdutoApi
from models_excel.modelagem_dados_anuncios import f_nome_anuncio, f_similares, f_descricoes
from tipos.tipos import RetornoNomeAnuncioTipo
print("USANDO CORE V2")
#####################################################################################################################
class Gerar_Anuncios:
    def __init__(
        self,
        planilha: str,
        funcao_atualizar_barra_geral,
        funcao_atualizar_barra_anuncio,
        local_salvar_imagens: str | None,
        label_qtd_feita: ttk.Label | None,
        baixar_img: bool = True
    ) -> None:
        self.planilha = planilha
        self.baixar_img = baixar_img
        self.funcao_atualizar_barra_geral = funcao_atualizar_barra_geral
        self.funcao_atualizar_barra_anuncio = funcao_atualizar_barra_anuncio
        self.local_salvar_imagens = local_salvar_imagens
        self.label_qtd_feita=label_qtd_feita

    def extrair_primeira_data(self, veiculo: str) -> str:
        "Uso essa função exatamente para pagar o primeiro nome de um"
        "Veículo que tem no nome e usamos para concatenar no nome anuncio"
        match = re.search(r'\b(19|20)\d{2}-(19|20)\d{2}\b', veiculo)
        if match:
            return veiculo[:match.end()]
        return veiculo

    @medir_tempo_execucao
    def gerar_planilha(self) -> None:
        if self.funcao_atualizar_barra_geral:
            self.funcao_atualizar_barra_geral(0)

        planilha_funcoes = Exel(arquivo_excel=self.planilha)
        planilha_aberta = planilha_funcoes.abrir()
        coluna_codigo = planilha_aberta['Cod Produto']
        qtd_produtos = len(coluna_codigo)

        texto_no_console(f'Total de produtos para criar anúncio: {qtd_produtos}')

        qtd_feita = 1

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

            # dados_anuncio_api = puxar_dados_produto_api(
            #     codigo_produto=cod,
            #     dados_necessarios=dados_puxar
            # )
            dados_anuncio_api = DadosProdutoApi(cod)

            if not dados_anuncio_api:
                for coluna in dados_inserir.keys():
                    dados_inserir[coluna].append("sem dados / código errado")
                qtd_feita += 1
                continue

            nome_anuncio_: RetornoNomeAnuncioTipo = f_nome_anuncio(dados_produto={
                'aplicacao': dados_anuncio_api.aplicacao,
                'grupo_produto': dados_anuncio_api.grupo_produto,
                'lado': dados_anuncio_api.lado,
                'marca': dados_anuncio_api.marca,
                'part_number': dados_anuncio_api.part_number,
                'posicao': dados_anuncio_api.posicao
            })
            nome_anuncio = nome_anuncio_['nome_anuncio']
            nome_ate_60 = nome_anuncio_['nome_ate_60_caracteres']

            descricoes = f_descricoes(dados_produto={
                'nome': dados_anuncio_api.nome,
                'marca': dados_anuncio_api.marca,
                'part_number': dados_anuncio_api.part_number,
                'similares': dados_anuncio_api.similares,
                'veiculos': dados_anuncio_api.veiculos
                }, funcao_atualizar_barra_anuncio=self.funcao_atualizar_barra_anuncio)



            dados_anuncio_api.dados_gerais["nome_anuncio"] = nome_anuncio
            dados_anuncio_api.dados_gerais["nome_ate_60"] = nome_ate_60
            dados_anuncio_api.dados_gerais["descricao_completa_ecommerce"] = descricoes['descricao_completa_ecommerce']
            dados_anuncio_api.dados_gerais["descricao_simplificada"] = dados_anuncio_api.aplicacao
            dados_anuncio_api.dados_gerais["similares_feito"] = f_similares(dados_anuncio_api.similares)
            dados_anuncio_api.dados_gerais["descricao_completa"] = descricoes['aplicacao']
            texto_no_console(f'Nome gerado: {nome_ate_60}')
            for coluna in dados_inserir.keys():

                # Eu adicionei até dados que['part_number'] criamos nos dados de retorno gerais acima...
                # fazendo isso aqui abaixo vamos inserir.
                # ou seja, minha ideia foi montar tudo acima, e adicionar os dados no próprio retorno
                # para no fim eu adicionar tudo de uma vez em dados_inserir
                dados = dados_anuncio_api.dados_gerais[coluna]
                dados_inserir[coluna].append(dados)

            try:
                if self.baixar_img:
                    self.baixar_imagem(
                        url=dados_anuncio_api.imagem_url,
                        nome_arquivo=dados_anuncio_api.part_number
                    )
            except:
                pass

            # texto_no_console(f'Feito: {qtd_feita}/{qtd_produtos}.')
            texto_no_console('-')

            if self.funcao_atualizar_barra_geral:
                progresso = int((qtd_feita / qtd_produtos) * 100)
                self.funcao_atualizar_barra_geral(progresso)
            if self.label_qtd_feita:
                self.label_qtd_feita.config(text=f"{qtd_feita}/{qtd_produtos}")

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
                nome_salvar=f'{local_salvar}/planilha_anúncios'
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
                nome_salvar=f'{local_salvar}/planilha_anúncios'
            )

        texto_no_console('Planilha de anúncios gerada com sucesso!')
        texto_no_console('Tempo demorado para gerar a planilha:')

    def baixar_imagem(self, url: str, nome_arquivo: str) -> None:
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

    # def verificar_e_substituir_nome_padrao(self, nome_padrao: str) -> str:
    #     nome_padrao = str(nome_padrao).lower()
    #     return PADROES_SUBS_NOME_ANUNCIO.get(nome_padrao, nome_padrao)

