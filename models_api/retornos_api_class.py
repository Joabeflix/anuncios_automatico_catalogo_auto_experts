from models_api.api_max import puxar_dados_produto_api

class DadosProduto:
    def __init__(self, codigo_produto) -> None:
        dados_puxar = [
            'nome', 'grupo_produto', 'aplicacao', 'marca',
            'part_number', 'ean', 'posicao', 'lado',
            'imagem_url', 'veiculos', 'ncm', 'garantia',
            'peso', 'altura_embalagem', 'largura_embalagem',
            'comprimento_embalagem', 'qtd_embalagem', 'similares'
        ]
        self.dados_api = puxar_dados_produto_api(codigo_produto, dados_necessarios=dados_puxar)

    @property
    def dados_gerais(self) -> dict:
        return self.dados_api
    @property
    def nome(self) -> str:
        return self.dados_api['nome']
    @property
    def grupo_produto(self) -> str:
        return self.dados_api['grupo_produto']
    @property
    def aplicacao(self) -> str:
        return self.dados_api['aplicacao']
    @property
    def marca(self) -> str:
        return self.dados_api['marca']
    @property
    def part_number(self) -> str:
        return self.dados_api['part_number']
    @property
    def ean(self) -> str:
        return self.dados_api['ean']
    @property
    def posicao(self) -> str:
        return self.dados_api['posicao']
    @property
    def lado(self) -> str:
        return self.dados_api['lado']
    @property
    def imagem_url(self) -> str:
        return self.dados_api['imagem_url']
    @property
    def veiculos(self) -> dict:
        return self.dados_api['veiculos']
    @property
    def ncm(self) -> str:
        return self.dados_api['ncm']
    @property
    def garantia(self) -> str:
        return self.dados_api['garantia']
    @property
    def peso(self) -> str:
        return self.dados_api['peso']
    @property
    def altura_embalagem(self) -> str:
        return self.dados_api['altura_embalagem']
    @property
    def largura_embalagem(self) -> str:
        return self.dados_api['largura_embalagem']
    @property
    def comprimento_embalagem(self) -> str:
        return self.dados_api['comprimento_embalagem']
    @property
    def qtd_embalagem(self) -> str:
        return self.dados_api['qtd_embalagem']
    @property
    def similares(self) -> dict:
        return self.dados_api['similares']
    

if __name__ == '__main__':
    app = DadosProduto('C-3377')
    print(app.aplicacao)    
    print(app.peso)
    app.dados_gerais['teste'] = "joabeflix"
    print(app.dados_gerais)





