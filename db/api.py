import pathlib
import sqlite3
import pandas as pd

DB_FILE = 'gy91.db'

def get_gy91_data(start, end):
    """
    Query wind data rows between two ranges
    :params start: start row id
    :params end: end row id
    :returns: pandas dataframe object
    """

    conn = sqlite3.connect(str(DB_FILE))
    statement = f'SELECT gX, gY, gZ FROM Gyroscope WHERE rowid > "{start}" AND rowid <= "{end}";'
    df = pd.read_sql_query(statement, conn)
    return df

def get_gy91_data_by_id(id):
    """
    Query a row from the Wind Table
    :params id: a row id
    :returns: pandas dataframe object
    """
    conn = sqlite3.connect(str(DB_FILE))
    statement = f'SELECVT * FROM Gyroscope WHERE rowid = "{id}";'
    df = pd.read_sql_query(statement, conn)
    return df

