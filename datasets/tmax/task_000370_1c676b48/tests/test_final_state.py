# test_final_state.py
import csv
import os
import re
import subprocess
import pytest

def test_pipeline_output_and_cron():
    score = 0.0

    csv_path = '/home/user/cleaned_dataset.csv'
    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist."

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ['hour', 'user_id', 'event_clean', 'user_category', 'user_type'], \
            f"CSV headers are incorrect. Expected ['hour', 'user_id', 'event_clean', 'user_category', 'user_type'], got {reader.fieldnames}"
        rows = list(reader)

    counts = {'guest': 0, 'registered': 0, 'admin': 0}
    hour_ok = 0
    clean_ok = 0
    cat_ok = 0

    for r in rows:
        user_type = r.get('user_type', '')
        counts[user_type] = counts.get(user_type, 0) + 1

        hour = r.get('hour', '')
        if hour.isdigit() and 0 <= int(hour) <= 23:
            hour_ok += 1

        event_clean = r.get('event_clean', '')
        if event_clean == event_clean.lower().strip() and not re.search(r'[^\w\s]', event_clean):
            clean_ok += 1

        cat = r.get('user_category', '')
        if cat in ['premium', 'standard', 'spam', 'unknown']:
            cat_ok += 1

    if counts == {'guest': 100, 'registered': 100, 'admin': 100}:
        score += 0.3

    if hour_ok == 300: 
        score += 0.2
    if clean_ok == 300: 
        score += 0.2
    if cat_ok == 300: 
        score += 0.2

    try:
        crontab = subprocess.check_output(['crontab', '-l'], stderr=subprocess.DEVNULL).decode()
        if '*/5 * * * *' in crontab and '/home/user/pipeline.sh' in crontab:
            score += 0.1
    except subprocess.CalledProcessError:
        pass

    assert score >= 0.95, (
        f"Pipeline score {score:.2f} is below the 0.95 threshold. "
        f"Details: counts={counts}, hour_ok={hour_ok}/300, clean_ok={clean_ok}/300, cat_ok={cat_ok}/300"
    )