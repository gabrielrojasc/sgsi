#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"/..
source scripts/utils.sh
assert_outside_container

DEVCONTAINER_SHARED_PATH=~/.config/magnet-django-devcontainer
ALIASES_PATH=$DEVCONTAINER_SHARED_PATH/zshcustom/50-aliases.zsh

if [[ -f $ALIASES_PATH ]]; then
  # Don't overwrite
  exit
fi

mkdir -p "$(dirname $ALIASES_PATH)"

# Copy but without the ##~ banner:
grep -Ev "^##~ " docker/zsh_dev/50-aliases.zsh > $ALIASES_PATH

color_print "$green" "Created aliases file"
