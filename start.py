import uvicorn

if __name__ == "__main__":
    uvicorn_log_config = uvicorn.config.LOGGING_CONFIG
    del uvicorn_log_config["loggers"] # delete default uvicorn logs for displayed only our custom logs
    uvicorn.run("src.main:app", log_config=uvicorn_log_config, host="0.0.0.0", port=8000, reload=True)