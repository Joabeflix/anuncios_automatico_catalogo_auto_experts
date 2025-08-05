import pandas as pd
from datetime import datetime

class Exel:
    def __init__(self, arquivo_excel: str) -> None:
        self.arquivo_excel=arquivo_excel

    def abrir(self, nome_aba: str='') -> pd.DataFrame:
        if nome_aba:
            return pd.read_excel(self.arquivo_excel, sheet_name=nome_aba)
        return pd.read_excel(self.arquivo_excel)

    def salvar(self, planilha: pd.DataFrame, nome_salvar: str) -> None:
        data_hora = datetime.now().strftime('%d_%m_%y_%H_%M')
        planilha.to_excel(f'{nome_salvar}_{data_hora}.xlsx', index=False)
    
    def adicionar_colunas(self, planilha: pd.DataFrame, nome_salvar: str, dados_inserir: dict={}) -> None:
        if dados_inserir:
            for coluna in dados_inserir.keys():
                planilha[coluna] = dados_inserir.get(coluna)

            self.salvar(planilha=planilha, nome_salvar=nome_salvar)
                
    
if __name__ == "__main__":
    local_arquivo = r'models_excel\teste.xlsx'
    planilha_funcoes = Exel(arquivo_excel=local_arquivo)
    planilha = planilha_funcoes.abrir()

    dados_inserir = {
        "COLUNA x": [
            1, 2, 3, 4
        ],
        "COLUNA_Y": [
            "JOABE", "ALVES", "LUZ", "LINDO"
        ]
    }

    # planilha_funcoes.adicionar_colunas(planilha=planilha, dados_inserir=dados_inserir)

