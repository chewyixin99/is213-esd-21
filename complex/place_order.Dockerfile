## Build image:
# docker build -t koguwee/place_order:esd -f ./place_order.Dockerfile .
# Note: build from this folder

## Run image:
# docker run --name place_order -p 5100:5100 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/esd <dockerid>/place_order:esd

FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./amqp/amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY ./place_order.py ./invokes.py ./amqp/amqp_setup.py ./
CMD [ "python", "./place_order.py" ]