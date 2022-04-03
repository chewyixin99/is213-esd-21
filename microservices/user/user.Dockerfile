## Build image:
# docker build -t <dockerid>/user:esd -f ./user.Dockerfile .
# Note: build from this folder

## Run image:
# docker run --name user -p 5001:5001 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/esd <dockerid>/user:esd

FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./user.py ./
CMD [ "python", "./user.py" ]