#!/bin/sh
set -e
nginx -c "$(pwd)/nginx.conf" -g 'daemon off;' &
python3 server.py &
wait
