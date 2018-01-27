FROM ubuntu:latest
RUN apt-get update -y; apt-get install -y python-pip python-dev build-essential
COPY *.* /app/
WORKDIR /app
VOLUME /config
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
