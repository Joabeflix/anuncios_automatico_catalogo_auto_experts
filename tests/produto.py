from models_api.api_max import puxar_dados_produto_api


if __name__ == "__main__":
    cod_produto = 'C-5688'
    # dados_necessarios = ['nome', 'marca', 'aplicacao', 'peso']
    dados_necessarios = ['json_completo']

    print(puxar_dados_produto_api(cod_produto, dados_necessarios))


