import pandas as pd
import shutil

import sys
import os
sys.path.append(os.getcwd())
os.environ.setdefault('SQLALCHEMY_SILENCE_UBER_WARNING', '1')

from src.data_control import find, get_file_path, write_to, remove_file, get_data

def test_find():
    assert find('not_existing_table') == False


def test_write_find():
    df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']], columns=['int_column', 'date_column'])
    write_to('only_for_test', df)
    assert find('only_for_test') == True


def test_rewove_file():
    df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']], columns=['int_column', 'date_column'])
    write_to('only_for_test', df)
    assert find('only_for_test') == True
    remove_file('only_for_test')
    assert find('only_for_test') == False


def test_get_data():
    df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']], columns=['int_column', 'date_column'])
    write_to('only_for_test', df)
    result = get_data('only_for_test')
    assert result.equals(df) == True


def test_get_file_path():
    if os.path.isdir('temp'): shutil.rmtree('temp', ignore_errors=True)
    df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']], columns=['int_column', 'date_column'])
    write_to('only_for_test', df)
    assert get_file_path('only_for_test') == 'data/only_for_test.csv'
    remove_file('only_for_test')
