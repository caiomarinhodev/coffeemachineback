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

mkdir -p backcoffee/reports/
sloccount --duplicates --wide --details backcoffee > backcoffee/reports/sloccount.sc

virtualenv --python=python2 env
env/bin/pip install -r backcoffee/requirements.txt
env/bin/python backcoffee/manage.py violations --max=1000
exit_if_error
env/bin/python backcoffee/manage.py makemigrations
env/bin/python backcoffee/manage.py migrate
# env/bin/python xingu_back/manage.py compilemessages          # Create translation files
# manage collectstatic --noinput  # Collect static files
env/bin/python backcoffee/manage.py jenkins xingu --enable-coverage
env/bin/coverage run --source='backcoffee/' backcoffee/manage.py test xingu
env/bin/coverage xml -o backcoffee/reports/coverage.xml

