#!/bin/bash

if [[ "$1" == "-test" ]]; then
    pytest
elif [[ "$1" == "-install" ]]; then
    python3 -m pip install requirements.txt
else
    python3 -m src.ac_editor
fi
