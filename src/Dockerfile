FROM python:3.11
LABEL maintainer="lit.nk.98@gmail.com"

WORKDIR /usr/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./src

RUN mkdir data 
#ENV DATA_DIR = '${pwd}/data'

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0"]