# Script para popular o banco de dados com leituras de exemplo

import random
from datetime import datetime, timedelta
from database import init_db, inserir_leitura

# Garante que o banco e a tabela existem
init_db()

base_time = datetime.now() - timedelta(hours=30)

print('Inserindo 30 leituras de exemplo...')
for i in range(30):
    temp = round(random.uniform(18.0, 32.0), 1)
    umid = round(random.uniform(40.0, 85.0), 1)
    pressao = round(random.uniform(1008.0, 1020.0), 1)

    inserir_leitura(
        temperatura=temp,
        umidade=umid,
        pressao=pressao,
        localizacao='Inteli'
    )
    print(f'  [{i+1:02d}] temp={temp} °C  umid={umid} %  pressao={pressao} hPa')

print('\nBanco populado com sucesso!')