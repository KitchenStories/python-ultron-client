#!/bin/bash

export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export WORKON_HOME=/home/gitlab_ci_multi_runner/.virtualenvs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
mkvirtualenv ultron-client-env || true
source /home/gitlab_ci_multi_runner/.virtualenvs/ultron-client-env/bin/activate
pip install -r requirements/dev.txt
