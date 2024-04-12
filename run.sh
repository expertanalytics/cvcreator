#!/bin/bash

podman run -it --rm -v $1:/mnt cvcreator:latest .venv/bin/cvcreate -p ':' /mnt/content.toml mnt/$2
