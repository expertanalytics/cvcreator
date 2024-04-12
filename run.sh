#!/bin/bash
podman run -it --rm -v $1:/mnt cvcreator:latest .venv/bin/cvcreate --projects ':' /mnt/content.toml mnt/$2
