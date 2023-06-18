FROM python:3.9.16-slim-buster
WORKDIR /opt/webapp

COPY ./car_racing_server.py .
EXPOSE 5555
CMD python car_racing_server.py