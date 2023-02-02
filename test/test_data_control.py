import pandas as pd
import shutil

import sys
import os
sys.path.append(os.getcwd())
os.environ.setdefault('SQLALCHEMY_SILENCE_UBER_WARNING', '1')

from src.data_control import Controller

con = Controller()

def test_find():
    assert con.find('not_existing_table') == False


def test_write_find():
    df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']], columns=['int_column', 'date_column'])
    con.write_to('only_for_test', df)
    assert con.find('only_for_test') == True


def test_rewove_file():
    df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']], columns=['int_column', 'date_column'])
    con.write_to('only_for_test', df)
    assert con.find('only_for_test') == True
    con.remove_file('only_for_test')
    assert con.find('only_for_test') == False


def test_get_data():
    df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']], columns=['int_column', 'date_column'])
    con.write_to('only_for_test', df)
    result = con.get_data('only_for_test')
    assert result.equals(df) == True


def test_get_file_path():
    if os.path.isdir('temp'): shutil.rmtree('temp', ignore_errors=True)
    df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']], columns=['int_column', 'date_column'])
    con.write_to('only_for_test', df)

    assert con.get_file_path('only_for_test') == f'{con.data_path}only_for_test.csv'
    con.remove_file('only_for_test')
