#!/bin/bash

# Install all requirements to prject development

updated=""

main() {
    check_dependencies
    exit_if_error
}

function check_dependencies() {
    check_pkg python2.7
    check_pkg python2.7-dev
    check_pkg sloccount
    check_pkg graphviz
    check_pkg graphviz-dev
    check_pkg build-essential
    check_pip
    check_module virtualenv
    check_module Fabric
    check_nodejs
    exit_if_error
}

function check_module() {
    up=`pip list 2>/dev/null | grep $1`
    if [ "$up" = "" ] ; then
        sudo pip install $1
    else
        echo "$1 updated"
    fi
    exit_if_error
}

function check_modules_update() {
    up=`pip list --outdated 2>/dev/null`
    if [ "$up" = "" ] ; then
        echo "site-packages updated"
    else
        pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | sudo xargs -n1 pip install -U
    fi
    exit_if_error
}

function check_pip() {
    if hash pip 2>/dev/null; then
        echo "pip installed"
    else
        wget https://bootstrap.pypa.io/get-pip.py -O - | sudo python2 -
    fi
    exit_if_error
}

function check_pkg() {
    pkg=`dpkg-query -W --showformat='${Status}\n' $1 2>/dev/null`
    echo $pkg
    if [ "$pkg" != "install ok installed" ] ; then
        do_apt_get_update
        sudo apt-get install -y $1
    else
        echo "$1 installed"
    fi
    exit_if_error
}

function check_nodejs() {
    pkg=`dpkg-query -W --showformat='${Status}\n' nodejs 2>/dev/null`
    if [ "$pkg" != "install ok installed" ] ; then
        sudo curl -sL https://deb.nodesource.com/setup_0.12 | sudo -E bash -
        do_apt_get_update
        sudo apt-get install -y nodejs
    else
        echo "nodejs installed"
    fi
    exit_if_error
}

function exit_if_error() {
    err=$?
    if [ "$err" -ne "0" ]; then
        echo "Exit on error $err";
        exit 1;
    fi
}

function do_apt_get_update() {
    if [ "$updated" = "" ] ; then
        sudo apt-get update
        updated="true"
    fi
}
main "$@"
