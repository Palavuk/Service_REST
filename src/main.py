from fastapi import FastAPI, Body, UploadFile, Response
from fastapi.responses import FileResponse
import pandas as pd
import logging
import os

from .datacontrol import find, write_to

app = FastAPI()

logger = logging.getLogger("uvicorn.access")
err_logger = logging.getLogger("uvicorn.error")

@app.on_event('startup')
def startup_event():

    logger.setLevel('DEBUG')
    err_logger.setLevel('ERROR')

    log_dir = os.environ.get("LOG_DIR")
    if log_dir:
        f = open(f'{log_dir}/access.log', 'w+')
        f.close()
        handler = logging.FileHandler(f'{log_dir}/access.log')
        f = open(f'{log_dir}/error.log', 'w+')
        f.close()
        err_handler = logging.FileHandler(f'{log_dir}/error.log')
    else: 
        handler = logging.StreamHandler()
        err_handler = logging.StreamHandler()
    
    handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    err_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
    
    logger.addHandler(handler)
    err_logger.addHandler(err_handler)


@app.post("/filter/case_sensitive")
def function_filter(data = Body()):
    logger.info("POST /filter/case_sensitive")
    
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
    logger.info(f"POST /upload/{file_name}")
    
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
    logger.info(f"POST /load/{file_name}")

    if find(file_name):
        return FileResponse(find(file_name))
    else:
        response.status_code = 404
        return file_name + '.csv'

