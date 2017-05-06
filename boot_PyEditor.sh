#!/usr/bin/env bash

DESTINATION=$(pwd)/PyEditor_env

(
    set -e
    set -x

    python3 --version

    python3 -Im venv --without-pip ${DESTINATION}

    ls -la ${DESTINATION}/bin
)
(
    source ${DESTINATION}/bin/activate
    set -x
    python -m ensurepip
)
if [ "$?" == "0" ]; then
    echo "pip installed, ok"
else
    echo "ensurepip doesn't exist, use get-pip.py"
    (
        set -e
        source ${DESTINATION}/bin/activate
        set -x
        cd ${DESTINATION}/bin
        wget https://bootstrap.pypa.io/get-pip.py
        ${DESTINATION}/bin/python get-pip.py
    )
fi
(
    set -e
    source ${DESTINATION}/bin/activate
    set -x
    pip install --upgrade pip

    pip install -e git+git@github.com:PyEditor/PyEditor.git#egg=pyeditor
)
