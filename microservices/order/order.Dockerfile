## Build image:
# docker build -t <dockerid>/order:esd -f ./order.Dockerfile .
# Note: build from this folder

## Run image:
# docker run --name order -p 5004:5004 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/esd <dockerid>/order:esd

FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./order.py ./
CMD [ "python", "./order.py" ]