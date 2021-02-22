import os
from sqlalchemy import create_engine


def auth_azure():

    connection_string = "mssql+pyodbc://{}:{}@{}:1433/{}?driver={}".format(
        os.environ.get("ls_sql_database_user"),
        os.environ.get("ls_sql_database_password"),
        os.environ.get("ls_sql_server_name"),
        os.environ.get("ls_sql_database_name"),
        "ODBC Driver 17 for SQL Server",
    )

    con = create_engine(connection_string).connect()

    return con
