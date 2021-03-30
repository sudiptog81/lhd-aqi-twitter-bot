#!/bin/bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
crontab -l > /tmp/jobs.txt
echo "@reboot bash $(pwd)/run.sh" >> /tmp/jobs.txt
echo "0 0,6,12,18 * * * bash $(pwd)/run-job.sh" >> /tmp/jobs.txt
crontab /tmp/jobs.txt
rm /tmp/jobs.txt
