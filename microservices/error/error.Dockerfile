# Note: build from "microservice" folder (files relative)

FROM python:3-slim
WORKDIR /usr/src/app
COPY ./amqp/amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r amqp.reqs.txt
COPY ./error.py ./amqp/amqp_setup.py ./
CMD [ "python", "./error.py" ]