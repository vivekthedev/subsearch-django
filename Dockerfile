FROM  python:3.10.4-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /cc

RUN apt-get update && apt-get install -y libglew-dev libglfw3-dev cmake gcc libssl-dev libcurl4-openssl-dev python-dev tesseract-ocr libtesseract-dev libleptonica-dev clang libclang-dev curl tar dnsutils


RUN curl -LO https://github.com/CCExtractor/ccextractor/archive/refs/tags/v0.87.tar.gz
RUN mkdir ccextractor
RUN tar -xzf v0.87.tar.gz -C ccextractor --strip-components=1

RUN apt-get install -y autoconf pkg-config
WORKDIR /cc/ccextractor/linux
RUN ./build -debug -without-rust

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .
