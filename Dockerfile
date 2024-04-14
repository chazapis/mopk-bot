FROM python:3.12.3 AS gpio-build

RUN pip wheel --wheel-dir=/tmp RPi.GPIO==0.7.1

FROM python:3.12.3-slim

RUN apt-get update && \
    apt-get install -y vim-tiny && \
    apt-get clean \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY . /app
WORKDIR /app

COPY --from=gpio-build /tmp/*.whl /tmp/
RUN pip install /tmp/*.whl && \
    pip install -r requirements.txt

ENV DISCORD_TOKEN=
ENV DISCORD_GUILD=
ENV DISCORD_CHANNEL=

CMD python bot.py
