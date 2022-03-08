#!/bin/sh
# this script is used to boot a Docker container
source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Deploy command failed, retrying in 5 secs...
    sleep 5
done
# flask translate compile
pybabel compile -d app/translations
# exec gunicorn -b :5000 --access-logfile - --error-logfile - pc_donation:app
exec gunicorn -b :5000 --access-logfile /home/pc_donation/logs/access.log --error-logfile /home/pc_donation/logs/error.log pc_donation:app
# exec nginx -g "daemon off;"
# export DOLLAR='$'
# exec envsubst < nginx.conf.template > /etc/nginx/project.conf
