import os
import json
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import OperationalError


class Controller():

    def __init__(self, sql_con=None) -> None:
        if sql_con is not None:
            self.engine = sql_con
            return
        if os.environ.get('DATA_DIR') is not None:
            self.data_path = os.environ.get('DATA_DIR')
            self.filesystem = True
        else:
            with open('src/db_connect.json', 'r', encoding='utf-8') as settings:
                try:
                    self.engine = create_engine(URL.create(**(json.load(settings)['DATABASE'])))
                    self.engine.connect()
                    self.filesystem = False
                except OperationalError:
                    self.data_path = 'data/'
                    self.filesystem = True

    def get_file_path(self, file_name):
        if self.filesystem:
            return self.data_path + file_name + '.csv'
        else:
            if not os.path.isdir('temp'):
                os.mkdir('temp')
            path = f'temp/{file_name}.csv'
            df = pd.read_sql(f'SELECT * FROM {file_name}', con = self.engine)
            Path(path).touch(exist_ok=True)
            df.to_csv(path, sep=';', index=False)
            return path

    def find(self, file_name):
        if self.filesystem:
            return bool(os.path.isfile(self.data_path + file_name + '.csv'))
        else:
            insp = inspect(self.engine)
            return insp.has_table(file_name)

    def write_to(self, file_name, data):
        if self.filesystem:
            path = self.get_file_path(file_name)

            if self.find(file_name):
                origin = pd.read_csv(path, sep=';')
                data = pd.concat([origin, data], sort=False, axis=0)
            else:
                Path(path).touch(exist_ok=True)

            data.to_csv(path, sep=';', index=False)
        else:
            if self.find(file_name):
                origin = pd.read_sql(f'SELECT * FROM {file_name}', con = self.engine)
                data = pd.concat([origin, data], sort=False, axis=0)
            data.to_sql(file_name, con=self.engine, if_exists='replace', index=False)

    def remove_file(self, file_name):
        if self.filesystem:
            os.remove(self.get_file_path(file_name))
        else:
            self.engine.execute(f'DROP TABLE IF EXISTS {file_name};')
    
    def get_data(self, file_name):
        if self.filesystem:
            return pd.read_csv(self.get_file_path(file_name), sep=';')
        else:
            return pd.read_sql(f'SELECT * FROM {file_name}', con = self.engine)