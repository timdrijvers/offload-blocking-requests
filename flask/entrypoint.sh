#!/bin/bash
export POLLER_IP=`getent hosts apipoller | awk '{ print $1 }'`
uwsgi --ini app.ini
#uwsgi --ini app.ini --gevent=10 --gevent-early-monkey-patch
