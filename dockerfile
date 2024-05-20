FROM python:3.11-slim

COPY ./ ./app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000
COPY ./docker-entrypoint.sh /usr/local/bin
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/bin/bash", "/usr/local/bin/docker-entrypoint.sh"]
