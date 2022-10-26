from io import StringIO

import pandas as pd
from prefect import task
import requests

import re

from utils import log


@task
def download_data(n_users: int) -> str:
    """
    Baixa dados da API https://randomuser.me e retorna um texto em formato CSV.

    Args:
        n_users (int): número de usuários a serem baixados.

    Returns:
        str: texto em formato CSV.
    """
    response = requests.get(
        "https://randomuser.me/api/?results={}&format=csv".format(n_users)
    )
    log("Dados baixados com sucesso!")
    return response.text


@task
def parse_data(data: str) -> pd.DataFrame:
    """
    Transforma os dados em formato CSV em um DataFrame do Pandas, para facilitar sua manipulação.

    Args:
        data (str): texto em formato CSV.

    Returns:
        pd.DataFrame: DataFrame do Pandas.
    """
    df = pd.read_csv(StringIO(data))
    log("Dados convertidos em DataFrame com sucesso!")
    return df


@task
def save_report(dataframe: pd.DataFrame) -> None:
    """
    Salva o DataFrame em um arquivo CSV.

    Args:
        dataframe (pd.DataFrame): DataFrame do Pandas.
    """
    dataframe.to_csv("report.csv", index=False)
    log("Dados salvos em report.csv com sucesso!")


@task
def format_phone_number(df, column_name):
    """
    Formata o número de telefone

     Args:
        dataframe (pd.DataFrame): DataFrame do Pandas, column 
    """
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


@task
# funcao para exibir total de user por genero
def total_users(df):
    """Exibe o total de usuários por gênero
    
     Args:
        dataframe (pd.DataFrame): DataFrame do Pandas.
    """
    df_gender = df_gender = df.gender.value_counts().rename_axis(
        'Gênero').to_frame('Quantidade').reset_index()
    df_gender["%"] = round(df_gender.Quantidade /
                           df_gender.Quantidade.sum() * 100, 0)

    log(f"Total de usuários por gênero: {df_gender}")


@task
def total_users_country(df):
    """Exibe o total de usuários por país
    
     Args:
        dataframe (pd.DataFrame): DataFrame do Pandas.
    """
    df_country = df.nat.value_counts().rename_axis(
        'País').to_frame('Quantidade').reset_index()
    df_country["%"] = round(df_country.Quantidade /
                            df_country.Quantidade.sum() * 100, 0)
    # add row com total de usuarios
    df_country = df_country.append({'País': 'Total', 'Quantidade': df_country.Quantidade.sum(
    ), '%': df_country['%'].sum()}, ignore_index=True)

    log(f"Total de usuários por país: {df_country}")

@task
def total_users_country(df):
    """" % users country
    
     Args:
        dataframe (pd.DataFrame): DataFrame do Pandas.
    """
    df_country = df.nat.value_counts().rename_axis('País').to_frame('Quantidade').reset_index()
    df_country["%"] = round( df_country.Quantidade / df_country.Quantidade.sum() * 100, 0 )
    # add row com total de usuarios
    df_country = df_country.append({'País': 'Total', 'Quantidade': df_country.Quantidade.sum(), '%': df_country['%'].sum()}, ignore_index=True)

    log(df_country)
    
