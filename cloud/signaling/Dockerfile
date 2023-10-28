# Set up signaling server at localhost:9999
FROM python:3.8
RUN apt update && apt install netcat-openbsd -y
EXPOSE 9999
RUN mkdir /signaling
WORKDIR /signaling/
COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt
COPY ./ .
CMD python -u server.py
