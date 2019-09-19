#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
source $DIR/venv/bin/activate
export PATH="$PATH:$DIR/ghr/ghr_v0.13.0_linux_386/"
