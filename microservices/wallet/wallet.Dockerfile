## Build image:
# docker build -t <dockerid>/wallet:esd -f ./wallet.Dockerfile .
# Note: build from this folder

## Run image:
# docker run --name wallet -p 5005:5005 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/esd <dockerid>/wallet:esd

FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./wallet.py ./
CMD [ "python", "./wallet.py" ]