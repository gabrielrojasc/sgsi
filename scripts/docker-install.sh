#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"/..
source scripts/utils.sh
assert_outside_container


if [[ "$OSTYPE" == darwin* ]]; then
  color_print $yellow "Warning: On macOS systems, install Docker Desktop manually. At least engine version 20.10 is required."
  exit
fi

title_print "Installing Docker..."

docker_version_new_enough() (
  # We currently use "COPY --chmod=" as a safeguard,
  # which requires 20.10 (https://github.com/moby/buildkit/pull/1492#issuecomment-758105476)
  # Also 20.10 is the only currently supported version  https://endoflife.date/docker-engine
  LOWEST_VERSION=20.10

  docker_version_majmin=$(docker --version |
    grep -Po '.*?\K\d+\.\d+')  # Extracts 12.34 from "asdsad 12.34.56 asdsad"

  # https://github.com/docker/docker-install/blob/0c9037543e67d311c57fe5ec9626052e0f37bb3f/install.sh#L96
  calver_compare() (
    set +x

    yy_a="$(echo "$1" | cut -d'.' -f1)"
    yy_b="$(echo "$2" | cut -d'.' -f1)"
    if [ "$yy_a" -lt "$yy_b" ]; then
      return 1
    fi
    if [ "$yy_a" -gt "$yy_b" ]; then
      return 0
    fi
    mm_a="$(echo "$1" | cut -d'.' -f2)"
    mm_b="$(echo "$2" | cut -d'.' -f2)"
    if [ "${mm_a#0}" -lt "${mm_b#0}" ]; then
      return 1
    fi

    return 0
  )

  eval calver_compare "$docker_version_majmin" $LOWEST_VERSION
)

# Check if docker is already installed
if command -v docker >/dev/null && docker_version_new_enough; then
  color_print $green "Skipped! $(docker --version) found."
else
  # Download and install.
  # The script says it can be used to update  (https://github.com/docker/docker-install/blob/c2de0811708b6d9015ed1a2c80f02c9b70c8ce7b/install.sh#L377)
  # and that it installs Compose              (https://github.com/docker/docker-install/blob/c2de0811708b6d9015ed1a2c80f02c9b70c8ce7b/install.sh#L19)
  sudo apt-get install -y curl jq
  curl -fsSL https://get.docker.com -o get-docker.sh
  chmod +x get-docker.sh
  sudo ./get-docker.sh
  rm get-docker.sh

  color_print $green "Docker installation completed."
fi

# Check if we are allowed to manage docker as a non-root
if ! groups | grep -qw docker; then
  sudo groupadd docker &>/dev/null || true
  sudo usermod -aG docker "$USER"
  echo "Please reboot your computer to use Docker without sudo." >> quickstart-messages.log
fi


if ! has_compose_plugin; then
  color_print $yellow "Modern docker version is present, but compose plugin is not?"
  # Hope this fixes it:
  sudo apt-get install -y docker-compose-plugin
  if ! has_compose_plugin; then
    color_print $red 'This is unexpected. docker-compose-plugin should have been installed,
but "docker compose" is not working.'
    exit 1
  fi
fi


enable_buildkit() {
  if ! [ -s /etc/docker/daemon.json ]; then
    # Default state (no file (or empty)), so create it:
    echo '{
    "features": {
      "buildkit": true
    }
  }' | sudo tee /etc/docker/daemon.json >/dev/null

    sudo systemctl restart docker.service

    color_print $green "BuildKit has been enabled."

  elif grep -q '"buildkit":\s*true' /etc/docker/daemon.json; then
    color_print $green "BuildKit already enabled."
    # Note: it's possible that even though the file contains buildkit:true,
    # a restart of the daemon is pending.

  else
    # force enable buildkit with jq
    color_print "$yellow" "BuildKit appears not to be enabled. Enabling it."
    new_file=$(mktemp)
    jq '.features.buildkit = true' /etc/docker/daemon.json > "$new_file"
    sudo sh -c 'mv "'"$new_file"'" /etc/docker/daemon.json; chown 0:0 /etc/docker/daemon.json; chmod 644 /etc/docker/daemon.json'
    color_print "$yellow" "Restarting docker daemon"
    sudo systemctl restart docker.service
  fi
}

# Enable BuildKit
if [[ "$(< /proc/sys/kernel/osrelease)" == "*Microsoft" ]]; then
  color_print $yellow 'Warning: On WSL, BuildKit must be configured manually using Docker Desktop GUI.
Make sure your daemon configuration contains the
following:
"features": {
  "buildkit": true
}"'
  exit
else
  enable_buildkit
fi
