import uvicorn
import os

if __name__ == "__main__":
    os.environ.setdefault('LOG_DIR', 'logs')
    if not os.path.isdir('logs'): os.mkdir('logs')
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)