FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*


# Install app dependencies
RUN pip install mysqlclient
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000
#RUN python manage.py migrate
#RUN python manage.py makemigrations
