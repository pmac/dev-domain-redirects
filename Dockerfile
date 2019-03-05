FROM python:3-slim-stretch

WORKDIR /app
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
CMD ["python", "app.py"]

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY ./static ./static
COPY ./templates ./templates
COPY app.py cnames.toml nginx.conf.sigil ./
