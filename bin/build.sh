#!/usr/bin/env bash
# -*- coding: utf-8 -*-

# exit on error
set -o errexit

python -m pip install --upgrade pip

pip install -r ../requirements.txt
