FROM python:3.4.8-jessie
ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 8000

RUN useradd --uid 1000 --no-create-home --home-dir /app webdev

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
                                               libpq-dev postgresql-client gettext curl \
                                               libopenblas-dev libatlas3-base gfortran && \
    rm -rf /var/lib/apt/lists/*

# Using PIL or Pillow? You probably want to uncomment next line
# RUN apt-get update && apt-get install -y --no-install-recommends libjpeg8-dev

WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# First copy requirements.txt and peep so we can take advantage of
# docker caching.
COPY requirements.txt /app/requirements.txt
RUN pip install --require-hashes --no-cache-dir -r requirements.txt

COPY . /app
RUN DEBUG=False SECRET_KEY=foo ALLOWED_HOSTS=localhost, DATABASE_URL=sqlite:// ./manage.py collectstatic --noinput -c
RUN chown webdev:webdev -R .
USER webdev

# Using /bin/bash as the entrypoint works around some volume mount issues on Windows
# where volume-mounted files do not have execute bits set.
# https://github.com/docker/compose/issues/2301#issuecomment-154450785 has additional background.
ENTRYPOINT ["/bin/bash", "/app/bin/run"]

CMD ["web"]
