#!/bin/bash

poetry build && podman build --rm -t cvcreator --network host .
