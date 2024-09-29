FROM python:3.12.5

RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/America/Bogota /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN mkdir /app
WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0","--port=8001", "--workers", "4"]
