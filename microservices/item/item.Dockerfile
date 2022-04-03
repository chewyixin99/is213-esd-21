## Build image:
# docker build -t <dockerid>/item:esd -f ./item.Dockerfile .
# Note: build from this folder

## Run image:
# docker run --name item -p 5003:5003 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/esd <dockerid>/item:esd

FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./item.py ./
CMD [ "python", "./item.py" ]