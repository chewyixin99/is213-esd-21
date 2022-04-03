## Build image:
# docker build -t koguwee/hawker:1.0 -f ./hawker/hawker.Dockerfile .
# Note: build from "microservice" folder

## Run image:
# docker run -p 5002:5002 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/esd <dockerid>/hawker:1.0

FROM python:3-slim
WORKDIR /usr/src/app
COPY ./dependencies/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./hawker/hawker.py ./
CMD [ "python", "./hawker.py" ]