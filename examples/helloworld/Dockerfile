FROM python:3.8.3-slim-buster as base

RUN apt-get -y update
RUN apt-get install -y sqlite3 libsqlite3-dev

WORKDIR /usr/src/app
RUN mkdir /db
ADD requirements.txt .
RUN pip install gunicorn
RUN pip install -r requirements.txt
COPY . .

RUN adduser --disabled-password --gecos '' default
RUN chmod +x ./examples/helloworld/api.py

USER default

FROM base as run
EXPOSE 5000
COPY ./examples/helloworld/api.py .
CMD [ "python" "./api.py" ]
