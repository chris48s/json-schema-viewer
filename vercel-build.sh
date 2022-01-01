#!/bin/bash

set -euo pipefail

echo 'looking for pipenv..'
command -v pipenv || { echo 'pipenv not found, installing..' && pip install pipenv; }

printf '\ninstalling..\n'
pipenv install

printf '\nbuilding..\n'
pipenv run build
echo '..done'
