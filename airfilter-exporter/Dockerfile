FROM python:3.7-slim-stretch

EXPOSE 9600/tcp

COPY app ./app
COPY pwm ./pwm
COPY sds011 ./sds011
COPY ccs811 ./ccs811
COPY airfilter_exporter.py .
COPY requirements.txt .

RUN apt-get update && apt-get upgrade -y && \
    apt-get purge -y libsqlite3-0 openssl && \
    apt-get autoremove -y && apt-get clean -y
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
CMD ["./airfilter_exporter.py"]
