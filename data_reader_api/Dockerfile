FROM python:3.6

LABEL maintainer="artur.karoly@irob.uni-obuda.hu"

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev && \
    python3 -m pip install --upgrade pip


COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT [ "python3" ]

CMD [ "./app.py" ]