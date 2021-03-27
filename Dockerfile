FROM python:3

# DONT CHANGE BELOW
RUN mkdir /corpus
RUN mkdir /models
RUN mkdir /normalized
RUN mkdir /outputs
# DONT CHANGE ABOVE


RUN apt update
RUN apt install -y build-essential libpoppler-cpp-dev pkg-config python-dev
RUN mkdir /app
WORKDIR /app
COPY build/requirements.txt ./
RUN pip install --no-cache-dir  -r requirements.txt
COPY build/scripts/ ./

ENTRYPOINT ["/bin/bash", "entrypoint.sh"]
