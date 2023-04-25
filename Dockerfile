FROM python:3.9-slim
WORKDIR /app
ADD . .
RUN ./install.sh
RUN apt update -y && apt install p7zip-full -y
WORKDIR /