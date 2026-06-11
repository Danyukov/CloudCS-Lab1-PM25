FROM python:3.11-slim-bookworm
RUN groupadd --gid 1000 service && \
    useradd --uid 1000 --gid service --shell /bin/bash --create-home service
WORKDIR /home/service
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./src .
COPY models/pipeline.pkl /models/pipeline.pkl
USER service
ENTRYPOINT [ "uvicorn" , "main:app", "--host", "0.0.0.0", "--port", "8000"]