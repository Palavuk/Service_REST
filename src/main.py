from fastapi import FastAPI, Body, UploadFile, Response
from fastapi.responses import FileResponse
import pandas as pd
from os import mkdir
from os.path import isfile, isdir

from .datacontrol import find, write_to

app = FastAPI()

@app.post("/filter/case_sensitive")
def function_filter(data = Body()):
    
    result = []
    not_interested = []
    
    for i in range(len(data) - 1):   
        word = data[i].lower()
        if word in not_interested: continue

        if data[i] not in (data[:i] + data[(i+1):]):
            if word not in result: result.append(word)
        elif word in result: 
            result.remove(word)
        else: 
            not_interested.append(data[i].lower())
    
    return result


@app.post("/upload/{file_name}")
def file_work(file_name, response: Response, files: list[UploadFile]):
    
    wrong_files = []
    for file in files:
        if file.filename.split('.')[-1] not in ['json', 'csv']: wrong_files.append(file.filename)
    
    if bool(wrong_files): 
        response.status_code = 415
        return wrong_files

    frames = []
    for file in files:
        df = pd.read_csv(file.file, sep=';') if file.content_type == "text/csv" else pd.read_json(file.file)
        frames.append(df)

    df = pd.concat(frames, sort=False, axis=0)

    write_to(file_name, df)


@app.post("/load/{file_name}")
def get_file(file_name, response: Response):
    if find(file_name):
        return FileResponse(find(file_name))
    else:
        response.status_code = 404
        return file_name + '.csv'

