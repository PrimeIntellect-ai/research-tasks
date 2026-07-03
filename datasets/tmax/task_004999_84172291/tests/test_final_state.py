# test_final_state.py
import os
import sys
import importlib.util

def test_incident_verdict_log():
    log_path = "/home/user/voice_sec/incident_verdict.log"
    assert os.path.isfile(log_path), f"Expected log file not found at {log_path}"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content == "VERDICT: EVIL", f"Expected 'VERDICT: EVIL' in {log_path}, got '{content}'"

def test_sanitizer_against_corpora():
    sys.path.insert(0, "/home/user/voice_sec")
    try:
        import sanitizer
    except ImportError:
        assert False, "Could not import sanitizer.py from /home/user/voice_sec"

    assert hasattr(sanitizer, 'is_safe_input'), "sanitizer.py is missing the 'is_safe_input' function"

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"

    failed_clean = []
    for filename in os.listdir(clean_dir):
        if not filename.endswith('.txt'):
            continue
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
        if not sanitizer.is_safe_input(content):
            failed_clean.append(filename)

    failed_evil = []
    for filename in os.listdir(evil_dir):
        if not filename.endswith('.txt'):
            continue
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
        if sanitizer.is_safe_input(content):
            failed_evil.append(filename)

    total_clean = len([f for f in os.listdir(clean_dir) if f.endswith('.txt')])
    total_evil = len([f for f in os.listdir(evil_dir) if f.endswith('.txt')])

    error_msgs = []
    if failed_clean:
        error_msgs.append(f"{len(failed_clean)} of {total_clean} clean modified/rejected. Offending files: {', '.join(failed_clean)}")
    if failed_evil:
        error_msgs.append(f"{len(failed_evil)} of {total_evil} evil bypassed/accepted. Offending files: {', '.join(failed_evil)}")

    assert not error_msgs, " | ".join(error_msgs)