#!/bin/sh

exec gunicorn BookSwap_Backend.wsgi:application --bind 0.0.0.0:8000 "$@"