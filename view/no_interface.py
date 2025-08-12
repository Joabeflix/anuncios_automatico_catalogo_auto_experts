import os
from models_excel.core import Gerar_Anuncios
from tkinter.filedialog import askopenfilename
from utils.utils import texto_no_console, tela_aviso, selecionar_pasta
import sys
from models_excel.core import Gerar_Anuncios
import threading
import os

class ConsoleInterface:
    def __init__(self) -> None:
        texto_no_console('Programa iniciado com sucesso!')
        self.local_salvar_imagens_t = rf'C:\Users\joab.alves\Downloads'
        self.baixar_imagens_opcao=True
        pass

    def selecionar_arquivos_excel(self) -> str | None:
        arquivo = askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
        if arquivo:
            texto_no_console(f'Arquivo selecionado com sucesso: {arquivo}\n')
            return arquivo
        else:   
            texto_no_console('Nenhum arquivo selecionado.\n')

    def executar(self) -> None:
        texto_no_console('Opções: [S] -> Selecionar Excel\n[C] -> Abrir Configurações')
        texto_no_console('Pressione [S] para selecionar o Excel para gerar os anúncios')
        texto_no_console('Pressione [Q] para ativar/desativar baixar imagens.')

        inp_opcao = input('///: ')

        opcoes = {
            "s": self.gerar_anuncios,
            'inv': self.opcao_invalida 
        }

        executar = opcoes.get(inp_opcao, 'inv')

    def opcao_invalida(self) -> None:
        os.system('cls')
        texto_no_console('Você selecionou uma opção inválida!')
        self.executar()

    def gerar_anuncios(self) -> None:

        local_excel = self.selecionar_arquivos_excel()
        if local_excel:
            app = Gerar_Anuncios(planilha=local_excel,baixar_img=True, local_salvar_imagens=self.local_salvar_imagens_t, funcao_atualizar_barra_anuncio=None, funcao_atualizar_barra_geral=None, label_qtd_feita=None)
            app.gerar_planilha()
            tela_aviso('Planilha finalizada', 'A planilha foi gerada com sucesso.', 'informacao')

        # Executando a interface no consol,e novamente...
        self.executar()

if __name__ == "__main__":
    app = ConsoleInterface()
    app.executar()
