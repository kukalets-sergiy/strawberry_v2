FROM python:3.8.5
ENV PYTHONUNBUFFERED=1

# Додайте необхідні системні пакети для встановлення mysqlclient
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev build-essential

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/



