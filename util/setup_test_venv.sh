#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
mkdir -p $DIR/venv
mkdir -p $DIR/ghr/
virtualenv --system-site-packages -p python3 $DIR/venv
cd /tmp
wget https://github.com/tcnksm/ghr/releases/download/v0.13.0/ghr_v0.13.0_linux_386.tar.gz
tar -zxvf ghr_v0.13.0_linux_386.tar.gz -C $DIR/ghr/
cd $DIR
export PATH=$PATH:$DIR/ghr/ghr_v0.13.0_linux_386/
source $DIR/venv/bin/activate
