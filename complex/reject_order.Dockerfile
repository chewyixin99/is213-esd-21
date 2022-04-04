FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./amqp/amqp.reqs.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt -r amqp.reqs.txt
COPY ./reject_order.py ./invokes.py ./amqp/amqp_setup.py ./
CMD [ "python", "./reject_order.py" ]