import os
import pandas as pd

data_path = 'data/' if os.environ.get('DATA_DIR') is None else os.environ.get('DATA_DIR')

def get_file_path(file_name):
    return data_path + file_name + '.csv'

def find(file_name):
    return bool(os.path.isfile(data_path + file_name + '.csv'))

def write_to(filename, data):
    path = get_file_path(filename)

    if find(filename):
        origin = pd.read_csv(path, sep=';')
        data = pd.concat([origin, data], sort=False, axis=0)
    else:
        f = open(path, 'w+')
        f.close()
    
    data.to_csv(path, sep=';', index=False)
