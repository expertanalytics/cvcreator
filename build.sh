#!/bin/bash

python -m build --wheel . && podman build --rm -t cvcreator --network host .
