# Builder image
FROM python:3-slim-stretch AS builder

WORKDIR /app
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"

RUN apt-get update && \
    apt-get install -y --no-install-recommends gettext build-essential && \
    rm -rf /var/lib/apt/lists/*

RUN python -m venv /venv

RUN pip install --no-cache-dir pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy


# Final image
FROM python:3-slim-stretch

WORKDIR /app
CMD ["python", "app.py"]
ENV LANG=C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/venv/bin:$PATH"

COPY --from=builder /venv /venv

COPY app.py nginx.conf.sigil ./
