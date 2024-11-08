#!/bin/bash

set -eo pipefail

if [ "$LOCAL" = "true" ]; then
    # local dev
    printf '\ninstalling..\n'
    pipenv sync

    printf '\nbuilding..\n'
    pipenv run build
    echo '..done'
else
    # building on vercel
    echo 'looking for pipenv..'
    command -v pipenv || { echo 'pipenv not found, installing..' && pip3.12 install pipenv; }

    printf '\ninstalling..\n'
    python3.12 -m pipenv sync

    printf '\nbuilding..\n'
    python3.12 -m pipenv run build
    echo '..done'
fi
