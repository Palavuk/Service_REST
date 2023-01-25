import os
import pandas as pd

if not os.path.isdir('data'):
    os.mkdir('data')

data_path = 'data/' if os.environ.get('DATA_DIR') == None else os.environ.get('DATA_DIR')

def find(file_name):
    if os.path.isfile(data_path + file_name + '.csv'):
        return data_path + file_name + '.csv'
    else:
        return False

def write_to(filename, data):
    path = find(filename)
    if path:
        origin = pd.read_csv(path, sep=';')
        data = pd.concat([origin, data], sort=False, axis=0)
    else:
        path = data_path + filename + '.csv'
        f = open(path, 'w+')
        f.close()
    
    data.to_csv(path, sep=';', index=False)
