FROM python:3.7-slim-buster
MAINTAINER Dani El-Ayyass <dayyass@yandex.ru>

WORKDIR /workdir
COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

CMD ["bash"]
