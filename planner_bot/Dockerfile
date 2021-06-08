FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN apt-get update && apt-get install -y netcat
COPY pip-requirements.txt /code/
RUN pip3 install --upgrade pip && \
    pip3 install -r pip-requirements.txt
COPY . /code/