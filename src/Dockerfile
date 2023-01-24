FROM python:3.11
LABEL maintainer="lit.nk.98@gmail.com"

WORKDIR /usr/app

RUN pip install fastapi && pip install python-multipart && pip install pandas && pip install "uvicorn[standard]" && mkdir data
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]