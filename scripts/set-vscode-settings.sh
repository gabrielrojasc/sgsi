#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"/..
source scripts/utils.sh

# Now that the image is built, set virtual_env in .env:
env_file='.env'

# VIRTUAL_ENV must be unset for poetry to generate the path itself
virtual_env=$(echo "docker-compose run --rm -T django env --unset=VIRTUAL_ENV poetry env info --path" | newgrp docker)
perl -pi -e "s|{{virtual_env}}|$virtual_env|g" $env_file

mkdir -p .vscode
if [[ ! -f .vscode/settings.json ]]; then
  echo \
"{
  \"python.defaultInterpreterPath\": \"$virtual_env/bin/python\",
}" > .vscode/settings.json
fi
if [[ ! -f .vscode/launch.json ]]; then
  echo \
  "{
    \"version\": \"0.2.0\",
    \"configurations\": [
        {
            \"name\": \"Server\",
            \"type\": \"python\",
            \"request\": \"launch\",
            \"program\": \"\${workspaceFolder}/manage.py\",
            \"args\": [
                \"runserver_plus\", \"8002\"
            ],
            \"django\": true,
            \"justMyCode\": true
        },
        {
            \"name\": \"Shell\",
            \"type\": \"python\",
            \"request\": \"launch\",
            \"program\": \"\${workspaceFolder}/manage.py\",
            \"args\": [
                \"shell_plus\",
            ],
            \"django\": true,
            \"justMyCode\": true
        }
    ]
}" > .vscode/launch.json
fi