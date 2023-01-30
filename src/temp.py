from sqlalchemy import create_engine, Column, Integer, String, DateTime, inspect
from sqlalchemy.engine.url import URL
import os
import pandas as pd
from sqlalchemy.orm import sessionmaker

DATABASE = {
    'drivername': 'postgresql+psycopg2', 
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': 'gfhjkm',
    'database': 'postgres'
}

engine = create_engine(URL.create(**DATABASE))

engine.connect()
    
#Session = sessionmaker(bind = engine)
#session = Session()

def get_file_path(file_name):
    if not os.path.isdir('temp'):
        os.mkdir('temp')
    df = pd.read_sql(f'SELECT * FROM {file_name}', con = engine)
    with open(f'temp/{file_name}.csv', 'w+') as f:
        f.close()
    df.to_csv(f'temp/{file_name}.csv', sep=';', index=False)
    return f'temp/{file_name}.csv'

def find(file_name):
    insp = inspect(engine)
    return insp.has_table(file_name)

def write_to(filename, data):
    if find(filename):
        origin = pd.read_sql(f'SELECT * FROM {filename}', con = engine)
        data = pd.concat([origin, data], sort=False, axis=0)
    data.to_sql(filename, con=engine, if_exists='replace', index=False)

def remove_file(file_name):
    engine.execute(f'DROP TABLE IF EXISTS {file_name};')

def get_data(file_name):
    return pd.read_sql(f'SELECT * FROM only_for_test', con = engine)