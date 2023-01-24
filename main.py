from fastapi import FastAPI, Body
import pandas as pd

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