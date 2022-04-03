## Build image:
# docker build -t <dockerid>/escrow:esd -f ./escrow.Dockerfile .
# Note: build from this folder

## Run image:
# docker run --name escrow -p 5006:5006 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/esd <dockerid>/escrow:esd

FROM python:3-slim
WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./escrow.py ./
CMD [ "python", "./escrow.py" ]