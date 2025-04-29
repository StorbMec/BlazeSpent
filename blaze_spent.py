import requests

def obter_transacoes(url, headers):
    pagina = 1
    total = 0.0
    
    while True:
        parametros = {'page': str(pagina)}
        
        try:
            resposta = requests.get(url, params=parametros, headers=headers)
            if resposta.status_code != 200:
                print(f"Erro ao acessar a API: {resposta.status_code}")
                break
                
            dados = resposta.json()
            
            for registro in dados.get('records', []):
                if registro.get('status') == 'complete':
                    valor_str = registro.get('amount', '0.0000')
                    try:
                        total += float(valor_str)
                    except:
                        print(f"Valor inválido ignorado: {valor_str}")
            
            total_paginas = dados.get('meta', {}).get('total_pages', 1)
            if pagina >= total_paginas:
                break
                
            pagina += 1
            
        except Exception as e:
            print(f"Erro durante a requisição: {str(e)}")
            break
            
    return total

def main():
    token = input("Cole seu Bearer Token aqui: ").strip()
    
    cabecalhos = {
        'authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pt-BR,pt;q=0.6',
        'device_id': '97814af4-733e-46a3-80ea-41f02bc0dce3',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'x-client-language': 'pt',
        'x-client-version': 'fd474d097',
    }
    
    print("\nCalculando...\n")
    
    total_depositado = obter_transacoes('https://blaze.bet.br/api/deposits', cabecalhos)
    total_sacado = obter_transacoes('https://blaze.bet.br/api/withdrawals', cabecalhos)
    
    saldo = total_sacado - total_depositado
    
    print(f"Total Depositado: R$ {total_depositado:.2f}")
    print(f"Total Sacado: R$ {total_sacado:.2f}")
    print(f"Saldo: R$ {saldo:.2f}")
    
    if saldo > 0:
        print("\nSituação: POSITIVO (Lucro)")
    elif saldo < 0:
        print("\nSituação: NEGATIVO (Prejuízo)")
    else:
        print("\nSituação: ZERADO")

if __name__ == "__main__":
    main()