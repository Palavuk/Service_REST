from fastapi.testclient import TestClient
import pandas as pd
from io import BytesIO

import sys
import os
sys.path.append(os.getcwd()) # for access to /src folder

from src.main import app
from src.datacontrol import find, data_path

client = TestClient(app)

def test_function_filter_OK():
    response = client.post(
        "/filter/case_sensitive",
        headers={"X-Token": "coneofsilence"},
        content='["Мама", "МАМА", "Мама", "папа", "ПАПА", "ДЯдя", "брАт", "Дядя", "Дядя"]'
    )
    print(response)
    assert response.status_code == 200
    assert response.json() == [ "папа", "брат" ]

def test_function_filter_fail():
    response = client.post(
        "/filter/case_sensitive",
        headers={"X-Token": "coneofsilence"}
    )
    print(response)
    assert response.status_code == 422

'''def test_file_work_OK():
    with open(sys.path[0] + '/test_files/test.csv', 'rb') as f:
        files = {'file': f.read()}
        #files = {'test.csv': open(sys.path[0] + '/test_files/test.csv', 'rb')}
        response = client.post(
            "/upload/test1",
            files=files
        )
        assert response.status_code == 200
'''

def test_get_file_OK():

    test_file = find('only_for_test')

    if not test_file:
        test_file = data_path + 'only_for_test.csv'
        file = open(test_file, 'w+')
        file.write('a;b')
        file.write('0;1')
        file.close()

    response = client.post(
        'load/only_for_test'
    )
    assert response.status_code == 200
    df = pd.read_csv(test_file, sep=';')
    res = pd.read_csv(BytesIO(response.content), sep=';')
    assert df.equals(res)

def test_get_file_404():
    response = client.post(
        'load/somefile'
    )
    
    assert response.status_code == 404
    assert response.json() == "somefile.csv"
