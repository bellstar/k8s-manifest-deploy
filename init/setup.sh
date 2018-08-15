#!/bin/bash
set -e

PACKAGE="python-pip python-dev python-virtualenv python-requests python-argcomplete jq tree mosh"

sudo apt update && \
  sudo apt install -y $PACKAGE
