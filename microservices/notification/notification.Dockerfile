FROM python:3-slim
WORKDIR /usr/src/app
COPY ../complex/amqp/amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r amqp.reqs.txt
COPY ./notification.py ../complex/amqp/amqp_setup.py ./
CMD [ "python", "./notification.py" ]