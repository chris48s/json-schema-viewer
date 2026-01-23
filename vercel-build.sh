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
    python3.12 -m venv .venv
    source .venv/bin/activate
    printf 'installing pipenv..'
    pip install --upgrade pip pipenv

    printf '\ninstalling..\n'
    pipenv sync

    printf '\nbuilding..\n'
    pipenv run build
    echo '..done'
fi
