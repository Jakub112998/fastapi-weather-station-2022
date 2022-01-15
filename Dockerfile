FROM python:3.9-slim

RUN mkdir app/
COPY .env /app/.env
COPY main.py /app/main.py

COPY ./app ./app/app
COPY ./requirements.txt /app/requirements.txt
COPY ./entrypoint.sh ./app/entrypoint.sh
COPY ./app/encrypted ./app/app/encrypted

WORKDIR /app

RUN chmod +x entrypoint.sh

RUN pip install -r requirements.txt
RUN pip install fastapi uvicorn
RUN pip install fastapi gunicorn

CMD [ "./entrypoint.sh" ]