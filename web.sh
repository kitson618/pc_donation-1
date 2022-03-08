#!/bin/sh
# this script is used to boot a Docker container
source venv/bin/activate

# exec nginx -g "daemon off;"
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
