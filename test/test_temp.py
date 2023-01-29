import pytest
import pandas as pd
import sqlalchemy

import sys
import os
sys.path.append(os.getcwd())

from src.temp import find, engine, get_file_path, write_to

def test_find():
    assert find('not_existing_table') == False

def test_write_find():
    df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']], columns=['int_column', 'date_column'])
    write_to('only_for_test', df)
    assert find('only_for_test') == True
    engine.execute('DROP TABLE IF EXISTS only_for_test;')


def test_get_file_path():
    df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']], columns=['int_column', 'date_column'])
    write_to('only_for_test', df)
    assert get_file_path('only_for_test') == 'temp/only_for_test.csv'
    engine.execute('DROP TABLE IF EXISTS only_for_test;')

def test_write_to():
    engine.execute('DROP TABLE IF EXISTS only_for_test;')
    df = pd.DataFrame(data=[[0, '10/11/12'], [1, '12/11/10']], columns=['int_column', 'date_column'])
    write_to('only_for_test', df)
    result = pd.read_sql(f'SELECT * FROM only_for_test', con = engine)
    assert result.equals(df) == True
