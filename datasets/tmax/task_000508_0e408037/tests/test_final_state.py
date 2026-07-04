# test_final_state.py

import os
import pytest

def test_sanitized_traffic_f1_score():
    raw_path = '/app/traffic.raw'
    sanitized_path = '/home/user/sanitized_traffic.raw'

    assert os.path.isfile(raw_path), f"Raw traffic file missing: {raw_path}"
    assert os.path.isfile(sanitized_path), f"Sanitized traffic file missing: {sanitized_path}"

    with open(raw_path, 'r', encoding='utf-8', errors='replace') as f:
        raw = f.read()
    with open(sanitized_path, 'r', encoding='utf-8', errors='replace') as f:
        sanitized = f.read()

    token = "X9fK_master_2024"
    original_count = raw.count(token)
    remnant_count = sanitized.count(token)
    redacted_count = sanitized.count("[REDACTED]")

    if original_count == 0:
        f1_score = 0.0
    elif remnant_count > 0:
        f1_score = 0.0
    elif redacted_count != original_count:
        f1_score = redacted_count / original_count
    else:
        f1_score = 1.0

    assert f1_score >= 0.99, f"Redaction F1-Score {f1_score} is below threshold 0.99. remnant_count={remnant_count}, redacted_count={redacted_count}, original_count={original_count}"

def test_alerts_log_created_and_format():
    alerts_path = '/home/user/alerts.log'
    assert os.path.isfile(alerts_path), f"Alerts log file missing: {alerts_path}"

    with open(alerts_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # Check that it contains the expected unauthorized format
    assert "UNAUTHORIZED: " in content, f"Alerts log missing expected 'UNAUTHORIZED: ' string format. Content: {content[:100]}..."

def test_picohttpparser_fixed():
    pico_c_path = '/app/picohttpparser-2.1/picohttpparser.c'
    assert os.path.isfile(pico_c_path), f"picohttpparser.c missing: {pico_c_path}"

    with open(pico_c_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    assert "<string.h>" in content, "The typo '<sting.h>' was not fixed to '<string.h>' in picohttpparser.c"