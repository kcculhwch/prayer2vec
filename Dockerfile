FROM python:3
RUN apt update
RUN apt install -y build-essential libpoppler-cpp-dev pkg-config python-dev
RUN mkdir /app
WORKDIR /app
COPY build/requirements.txt ./
RUN pip install --no-cache-dir  -r requirements.txt
COPY build/scripts/ ./
RUN mkdir /corpus
RUN mkdir /models
COPY corpus/ /corpus
COPY models /models

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
