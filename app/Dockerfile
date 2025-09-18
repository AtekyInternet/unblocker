FROM python:3.10-alpine AS build

WORKDIR /app

#Copy project from container
COPY ./ /app

RUN apk add alpine-sdk libffi-dev python3-dev

#Copy archives with packets of instalation of the python
COPY requirements.txt /tmp/requirements.txt

#Install packets of the python
RUN pip3 install -r /tmp/requirements.txt --no-cache-dir

RUN apk del alpine-sdk libffi-dev python3-dev

RUN rm -rf /root/.cache/pip &&\
    apk --purge del apk-tools

FROM python:3.10-alpine
#.
WORKDIR /app

COPY --from=build /app /app
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

EXPOSE 8888

CMD ["python3", "/app"]
