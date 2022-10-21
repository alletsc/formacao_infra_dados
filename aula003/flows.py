from prefect import Flow, Parameter

from tasks import (
    download_data,
    parse_data,
    save_report,
    format_phone_number,
    total_users,
    total_users_country

)

with Flow("Users report") as flow:

    # Parâmetros
    n_users = Parameter("n_users", default=10)

    # Tasks
    data = download_data(n_users)
    dataframe = parse_data(data)
    save_report(dataframe)
    format_phone_number(dataframe, "phone")
    format_phone_number(dataframe, "cell")
    total_users(dataframe)
    total_users_country(dataframe)



