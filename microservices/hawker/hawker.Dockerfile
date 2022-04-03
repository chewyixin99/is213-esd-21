## Build image:
# docker build -t koguwee/hawker:esd -f ./hawker.Dockerfile .
# Note: build from this folder

## Run image:
# docker run --name hawker -p 5002:5002 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/esd <dockerid>/hawker:esd

FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./hawker.py ./
CMD [ "python", "./hawker.py" ]