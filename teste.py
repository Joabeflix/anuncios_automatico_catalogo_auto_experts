import os

# Junta partes do caminho de forma compatível
caminho = os.path.join("pasta", "subpasta", "arquivo.txt")

print(caminho)
# No Windows → pasta\subpasta\arquivo.txt
# No Linux   → pasta/subpasta/arquivo.txt

