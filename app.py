from view.interface import MinhaInterface
from models_api.gerar_token import TokenGerador

if __name__ == "__main__":
    # Se não existir token, ao ler e ver que não existe token ele ja gera um    
    app = MinhaInterface()
    app.iniciar()


