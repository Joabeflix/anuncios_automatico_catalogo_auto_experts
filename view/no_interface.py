from tkinter.filedialog import askopenfilename
from utils.utils import texto_no_console, tela_aviso, selecionar_pasta
import sys
from models_excel.core import Gerar_Anuncios
import threading

class ConsoleInterface:
    def __init__(self) -> None:
        self.local_salvar_imagens_t = rf'C:\Users\joab.alves\Downloads'
        pass

    def executar(self) -> None:
        ...

    def selecionar_arquivos_excel(self) -> str | None:
        arquivo = askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
        if arquivo:
            texto_no_console(f'Arquivo selecionado com sucesso: {arquivo}\n')
            return arquivo
        else:   
            texto_no_console('Nenhum arquivo selecionado.\n')

    def principal(self) -> None:
        texto_no_console('Programa iniciado com sucesso!')
        texto_no_console('Pressione [S] para selecionar o Excel para gerar os anúncios')
        valor = input('[S]: ')
        if valor == 'S':
            local_excel = self.selecionar_arquivos_excel()
            if local_excel:
                app = Gerar_Anuncios(planilha=local_excel,baixar_img=True, local_salvar_imagens=self.local_salvar_imagens_t, funcao_atualizar_barra_anuncio=None, funcao_atualizar_barra_geral=None, label_qtd_feita=None)
                app.gerar_planilha()
                tela_aviso('Planilha finalizada', 'A planilha foi gerada com sucesso.', 'informacao')

if __name__ == "__main__":
    app = ConsoleInterface()
    app.principal()


