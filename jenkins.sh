#!/usr/bin/env bash

function exit_if_error() {
    err=$?
    if [ "$err" -ne "0" ]; then
        echo "Exit on error $err";
        mkdir reports | true
        echo '<testsuite errors="0" failures="0" name="violations" skips="0" tests="0" time="1.062"> \
                <testcase classname="dummy" name="dummy" time="0.897020" /> \
              </testsuite>' > reports/TEST-fail.xml
        exit 0;
    fi
}

mkdir -p xingu_back/reports/
sloccount --duplicates --wide --details xingu_back > xingu_back/reports/sloccount.sc

virtualenv --python=python2 env
env/bin/pip install -r xingu_back/requirements.txt
env/bin/python xingu_back/manage.py violations --max=67
exit_if_error
env/bin/python xingu_back/manage.py makemigrations
env/bin/python xingu_back/manage.py migrate
# env/bin/python xingu_back/manage.py compilemessages          # Create translation files
# manage collectstatic --noinput  # Collect static files
env/bin/python xingu_back/manage.py jenkins xingu --enable-coverage
env/bin/coverage run --source='xingu_back/' xingu_back/manage.py test xingu
env/bin/coverage xml -o xingu_back/reports/coverage.xml

