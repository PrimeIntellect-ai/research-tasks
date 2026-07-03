# test_final_state.py
import os
import csv
import stat
import pytest
import numpy as np
from scipy.io import wavfile

def test_directories_exist():
    dirs = ['src', 'bin', 'logs', 'www', 'tls', 'config']
    for d in dirs:
        path = f"/home/user/{d}"
        assert os.path.isdir(path), f"Directory {path} does not exist."

def test_sensor_config():
    conf_path = "/home/user/config/sensor.conf"
    assert os.path.isfile(conf_path), f"Config file {conf_path} does not exist."
    with open(conf_path, 'r') as f:
        content = f.read()
    assert "THRESHOLD=12000" in content, "THRESHOLD=12000 not found in sensor.conf"
    assert "MIN_DURATION_S=0.05" in content, "MIN_DURATION_S=0.05 not found in sensor.conf"
    assert "LOGFILE=/home/user/logs/sensor.log" in content, "LOGFILE not found in sensor.conf"

def test_logrotate_config():
    conf_path = "/home/user/config/logrotate.conf"
    assert os.path.isfile(conf_path), f"Logrotate config {conf_path} does not exist."
    with open(conf_path, 'r') as f:
        content = f.read()
    assert "/home/user/logs/sensor.log" in content, "Target log file not found in logrotate.conf"
    assert "daily" in content, "daily rotation not found in logrotate.conf"
    assert "rotate 7" in content, "rotate 7 not found in logrotate.conf"
    assert "compress" in content, "compress not found in logrotate.conf"

def test_deploy_script():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deploy script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deploy script {script_path} is not executable."
    with open(script_path, 'r') as f:
        content = f.read()
    assert "gcc" in content, "gcc not found in deploy.sh"
    assert "-O3" in content, "-O3 optimization flag not found in deploy.sh"

def test_tls_certs():
    cert_path = "/home/user/tls/cert.pem"
    key_path = "/home/user/tls/key.pem"
    assert os.path.isfile(cert_path), f"TLS cert {cert_path} does not exist."
    assert os.path.isfile(key_path), f"TLS key {key_path} does not exist."

def test_start_server_script():
    script_path = "/home/user/start_server.sh"
    assert os.path.isfile(script_path), f"Start server script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Start server script {script_path} is not executable."
    with open(script_path, 'r') as f:
        content = f.read()
    assert "8443" in content, "Port 8443 not found in start_server.sh"

def test_c_processor_exists():
    src_path = "/home/user/src/processor.c"
    bin_path = "/home/user/bin/processor"
    assert os.path.isfile(src_path), f"C source {src_path} does not exist."
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} does not exist."
    st = os.stat(bin_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Binary {bin_path} is not executable."

def get_truth_events(wav_path, threshold=12000, min_duration_s=0.05):
    rate, data = wavfile.read(wav_path)
    min_samples = int(min_duration_s * rate)

    is_over = np.abs(data) >= threshold

    events = []
    in_event = False
    event_start = 0
    consecutive_over = 0
    consecutive_under = 0

    for i, over in enumerate(is_over):
        if over:
            consecutive_over += 1
            consecutive_under = 0
            if not in_event and consecutive_over >= min_samples:
                in_event = True
                event_start = i - min_samples + 1
        else:
            consecutive_under += 1
            consecutive_over = 0
            if in_event and consecutive_under >= min_samples:
                in_event = False
                event_end = i - min_samples
                events.append((event_start / rate, (event_end - event_start + 1) / rate))

    if in_event:
        event_end = len(is_over) - 1
        events.append((event_start / rate, (event_end - event_start + 1) / rate))

    return events

def test_events_csv_f1_score():
    csv_path = "/home/user/www/events.csv"
    wav_path = "/app/machine_audio.wav"

    assert os.path.isfile(csv_path), f"Events CSV {csv_path} does not exist."
    assert os.path.isfile(wav_path), f"Audio file {wav_path} does not exist."

    truth_events = get_truth_events(wav_path)

    agent_events = []
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                agent_events.append((float(row['start_time']), float(row['duration'])))
    except Exception as e:
        pytest.fail(f"Failed to parse {csv_path}: {e}")

    if not agent_events and not truth_events:
        f1 = 1.0
    elif not agent_events or not truth_events:
        f1 = 0.0
    else:
        matches = 0
        for t_start, t_dur in truth_events:
            for a_start, a_dur in agent_events:
                if abs(t_start - a_start) <= 0.05 and abs(t_dur - a_dur) <= 0.05:
                    matches += 1
                    break

        precision = matches / len(agent_events) if len(agent_events) > 0 else 0
        recall = matches / len(truth_events) if len(truth_events) > 0 else 0

        if precision + recall == 0:
            f1 = 0.0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

    assert f1 >= 0.95, f"F1 score {f1:.4f} is below the threshold of 0.95. Agent found {len(agent_events)} events, expected {len(truth_events)}."