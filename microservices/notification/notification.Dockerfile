# Note: build from this folder 

FROM python:3-slim
WORKDIR /usr/src/app
COPY ./amqp/amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r amqp.reqs.txt
COPY ./notification.py ./amqp/amqp_setup.py ./
CMD [ "python", "./notification.py" ]