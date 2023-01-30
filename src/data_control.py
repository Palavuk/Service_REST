import os
import pandas as pd

data_path = 'data/' if os.environ.get('DATA_DIR') is None else os.environ.get('DATA_DIR')

def get_file_path(file_name):
    return data_path + file_name + '.csv'

def find(file_name):
    return bool(os.path.isfile(data_path + file_name + '.csv'))

def write_to(file_name, data):
    path = get_file_path(file_name)

    if find(file_name):
        origin = pd.read_csv(path, sep=';')
        data = pd.concat([origin, data], sort=False, axis=0)
    else:
        f = open(path, 'w+')
        f.close()
    
    data.to_csv(path, sep=';', index=False)

def get_data(file_name):
    path = get_file_path(file_name)
    return pd.read_csv(path, sep=';')

def remove_file(file_name):
    os.remove(get_file_path(file_name))