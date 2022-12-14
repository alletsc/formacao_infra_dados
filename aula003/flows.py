from prefect import Flow, Parameter

from tasks import (
    download_data,
    gerar_df,
    salvar_df_transformado,
    format_phone_number,
    total_users,
    total_users_country
)

with Flow("Users report") as flow:
    # Parâmetros
    n_users = Parameter("n_users", default=10)
    
    # Tasks
    data = download_data(n_users)
    dataframe = gerar_df(data)
    salvar_df_transformado(dataframe)
    format_phone_number(dataframe, "phone")
    format_phone_number(dataframe, "cell")
    total_users(dataframe)
    total_users_country(dataframe)
    