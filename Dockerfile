FROM python:3.6-slim as base

RUN apt-get -y update
RUN apt-get install -y sqlite3 libsqlite3-dev

WORKDIR /usr/src/app
RUN mkdir /db
ADD requirements.txt .
RUN pip install gunicorn
RUN pip install -r requirements.txt
COPY . .

RUN adduser --disabled-password --gecos '' default
RUN chmod +x boot.sh
USER default

FROM base as run
EXPOSE 5001
RUN /usr/bin/sqlite3 /db/test.db
ENV PYTHONPATH=.:hallmonitor
CMD ["./boot.sh"]
