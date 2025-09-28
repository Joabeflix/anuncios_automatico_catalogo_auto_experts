from models_api.api_max import puxar_dados_veiculos_api


if __name__ == "__main__":
    dict_veiculos = [
                  {
                     "id":"f5d7c131-3ada-45ac-8862-ed7bfa86b847",
                     "codigo":"C.FOR.0358",
                     "anoInicial":1979,
                     "anoFinal":1992,
                     "observacao":"",
                     "restricao":"",
                     "somente":""
                  },
                  {
                     "id":"f2fe2866-be5e-43b2-8849-cbceca6b726a",
                     "codigo":"C.FOR.0360",
                     "anoInicial":1979,
                     "anoFinal":1992,
                     "observacao":"",
                     "restricao":"",
                     "somente":""
                  },
                  {
                     "id":"cef98c16-fdfc-49d2-8f10-c6cb33e88d50",
                     "codigo":"C.FOR.0361",
                     "anoInicial":1979,
                     "anoFinal":1992,
                     "observacao":"",
                     "restricao":"",
                     "somente":""
                  },
                  {
                     "id":"9144c50c-bf34-4b50-b806-25cb22d476f9",
                     "codigo":"C.FOR.0359",
                     "anoInicial":1979,
                     "anoFinal":1992,
                     "observacao":"",
                     "restricao":"",
                     "somente":""
                  }
               ]
    
    print(puxar_dados_veiculos_api(dict_veiculos))



