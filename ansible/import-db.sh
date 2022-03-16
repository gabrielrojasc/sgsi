#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"
source ../scripts/utils.sh

if (( $# == 0 )); then
  echo "Please specify target server"
  exit 1
fi
limit=$1

readonly LOCAL_DUMPS_PATH=../db_dumps

if (( $# == 1 )); then
  color_print "$cyan" "Creating a new backup..."

  # Horrible way of showing nice output and getting the db_dump with the same command.
  # It's extracted from:
  #
  #   TASK [backup-db : set dump_name]
  #   ok: [playg] => {
  #       "ansible_facts": {
  #           "dump_name": "playg-2022-02-14_22-49-05.dump"
  #       },

  dump_name=$(\
    ANSIBLE_FORCE_COLOR=True ansible-playbook -v --limit "$limit" playbooks/backup-db.yml \
      | tee /dev/tty \
      | grep -Po '"dump_name": "\K.+\.dump(?=")')

else
  dump_name=$2
fi

local_dump_path="$LOCAL_DUMPS_PATH/$dump_name"

if [ ! -f "$local_dump_path" ]; then
  color_print "$cyan" "Downloading $dump_name ..."

  # Ansible is not a good solution for downloading large files.
  # The `fetch` module always hashes the file on remote, even with "validate_checksum: no", and shows no progress.
  # Next alternative is `scp`, but it's uncomfortable to build parameters with `ansible-ssh`...
  # So use ssh as scp, showing progress with `pv`.

  remote_dump_path="$(yq -r .project_name group_vars/all.yml)/db_dumps/$dump_name"

  ansible-ssh "$limit" "pv -f $remote_dump_path" > $LOCAL_DUMPS_PATH/__tmp__.dump
  # Download to temp file to avoid storing a partial file with the same name,
  # and not downloading again if previous download is interrupted
  mv $LOCAL_DUMPS_PATH/__tmp__.dump "$local_dump_path"
fi

color_print "$cyan" "Restoring $dump_name ..."

drop_status=0
drop_output=$(dropdb "$PGDATABASE") || drop_status=$?
# Fail if dropdb failed, except in case of "does not exist"
if [[ $drop_status != 0 && "$drop_output" != *" does not exist" ]]; then
  echo "$drop_output"
  exit $drop_status
fi

createdb "$PGDATABASE"
pg_restore --dbname="$PGDATABASE" --no-owner --no-acl --jobs="$(nproc)" "$local_dump_path"

color_print "$green" "Done"

# TODO: run "../manage.py migrate --check >/dev/null" and check for unapplied migrations,
# and for extra migrations.