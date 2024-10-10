FROM python:3.12

RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/Bogota /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

WORKDIR /app

COPY ./requirements.txt .
COPY ./scripts ./scripts
COPY ./patient_docs ./patient_docs
COPY ./alembic.ini .
COPY ./app/ ./app

RUN pip3 install -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8001"]
