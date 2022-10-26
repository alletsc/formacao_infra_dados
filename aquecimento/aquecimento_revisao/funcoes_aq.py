import pandas as pd
import requests
import json
import csv
import re
import warnings

API_URL = "https://randomuser.me/api/"


def get_data(API_URL):
    response = requests.get(API_URL)
    value = json.loads(response.text)  # carrega o json
    # normaliza os dados
    df = pd.json_normalize(value['results'], sep=';')
    df.to_csv('dados_api.csv', index=False, sep=';', encoding='utf-8')


def format_phone_number(df, column_name):
    if column_name in df.columns:
        def get_number(number):
            """ remover caracteres não numericos"""
            return re.sub(r'[^0-9]', '', number)
        df[column_name] = df[column_name].apply(get_number)

        def format_number(number):
            """ formata o numero de telefone"""
            return f'{number[:2]} {number[2:]}'
        df[column_name] = df[column_name].apply(format_number)
        return df.head()
    else:
        print(f"Coluna {column_name} não encontrada em {df}.")
        return df.head()
