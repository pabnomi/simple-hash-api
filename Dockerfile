FROM python:3.8 as compile-image

RUN apt-get update && apt-get install -y

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip && pip install pip-tools
#COPY ./requirements.txt .
#RUN pip install -r requirements.txt

# build stage

FROM python:3.8 as runtime-image

COPY --from=compile-image /opt/venv /opt/venv
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/

RUN addgroup --system user && adduser --system --no-create-home --group user
RUN chown -R user:user /usr/src/app && chmod -R 755 /usr/src/app

USER user

## add app
COPY ./app.py /usr/src/app

## set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"

CMD python ./app/app.py