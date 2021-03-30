# AQI Automation Twitter Bot

## Cronjob

Create `.env` with the template as in `.env.sample` first. Replace `delhi, us embassy` with your city in `job.py` line 38.

```bash
chmod +x install.sh
./install.sh
```

Note: if you receive errors regarding user has no crontab, generate one by executing `crontab -e` once and inserting an empty line.

## Watch Tweets as a Stream

Create `.env` with the template as in `.env.sample` first.

```bash
git clone <repo>
cd <repo>
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3 index.py
```
