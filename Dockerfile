#####################################
# Base image python + node + poetry
#####################################
FROM python:3.9.9-slim-bullseye AS python-node-base

WORKDIR /usr/src/app

# Install prerequisites
RUN apt-get update && apt-get install -y gcc curl libpq-dev gettext \
  && rm -rf /var/lib/apt/lists/*

# Install Node
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
  && apt-get install -y nodejs \
  && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

#####################################
# Add python+node dependencies
#####################################
FROM python-node-base AS project-dependencies
# Install python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# Install javascript dependencies
# COPY package.json package-lock.json ./
# RUN npm ci

#####################################
# Production image
#####################################
# Place Production image above development, so docker-compose on servers stop building after this one.
FROM project-dependencies AS production

# COPY assets webpack.*.js ./
# RUN npm run build

# Copy rest of the project
COPY . .

RUN poetry run django-admin compilemessages

# TODO: django-cron

CMD ["docker/django/prod_entrypoint.sh"]

#####################################
# Development image
#####################################
FROM project-dependencies AS development

# No need to copy the project, it's in a volume and prevents rebuilds.

RUN \
  # PostgreSQL client is required to pg_restore from Django container into Postgres container
  curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor > /usr/share/keyrings/postgresql.gpg \
  && echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
  && apt-get update && apt-get install -y git htop jq zsh postgresql-client-14 \
  && sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
  && rm -rf /var/lib/apt/lists/* \
  && ln -s /usr/src/app/ansible/ansible-ssh /usr/local/bin/ \
  && pip3 install yq

# Install Poetry dev-dependencies:
RUN poetry install

# Prevent development container shutdown:
CMD ["/bin/sh", "-c", "\"while sleep 1000; do :; done\""]