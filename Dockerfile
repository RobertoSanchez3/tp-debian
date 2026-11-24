FROM python:3.12-slim

LABEL maintainer="Administrateur système"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances nécessaires à python-ldap

RUN apt-get update && apt-get install -y \
    gcc \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copie du code Django

COPY app/ .

# Création du répertoire de données

RUN mkdir -p /data /app/staticfiles

# Compte applicatif non privilégié

RUN useradd --system --uid 10001 django \
    && chown -R django:django /app /data

USER django

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "config:application"]
