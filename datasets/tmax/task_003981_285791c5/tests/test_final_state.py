# test_final_state.py

import os
import json
import configparser
import re

def test_config_updated():
    config_path = '/home/user/microservices/config.ini'
    assert os.path.isfile(config_path), f"The config file {config_path} is missing."

    config = configparser.ConfigParser()
    config.read(config_path)

    assert 'Emitter' in config, "[Emitter] section missing in config.ini"
    assert config['Emitter'].get('processor_port') == '8002', "The processor_port in config.ini was not updated to 8002."

def test_apply_fixes_script_exists():
    script_path = '/home/user/apply_fixes.py'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

def test_first_transaction_extracted():
    log_path = '/home/user/microservices/logs/aggregator.log'
    txt_path = '/home/user/first_transaction.txt'

    assert os.path.isfile(log_path), f"The log file {log_path} is missing. Did the services run?"
    assert os.path.isfile(txt_path), f"The output file {txt_path} is missing."

    # Extract expected UUID from the first log line
    expected_uuid = None
    with open(log_path, 'r') as f:
        for line in f:
            if '[INFO] - SUCCESS - Transaction ID:' in line:
                match = re.search(r'Transaction ID: ([a-f0-9\-]+) -', line)
                if match:
                    expected_uuid = match.group(1)
                    break

    assert expected_uuid is not None, "Could not find a successful transaction in aggregator.log."

    with open(txt_path, 'r') as f:
        actual_uuid = f.read().strip()

    assert actual_uuid == expected_uuid, f"The UUID in {txt_path} ({actual_uuid}) does not match the first transaction in the log ({expected_uuid})."

def test_monitor_script_exists():
    script_path = '/home/user/monitor.py'
    assert os.path.isfile(script_path), f"The script {script_path} is missing."

def test_monitor_result():
    result_path = '/home/user/monitor_result.json'
    assert os.path.isfile(result_path), f"The result file {result_path} is missing."

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {result_path} does not contain valid JSON."

    assert data.get("status") == "success", f"Expected status 'success' in {result_path}, got {data.get('status')}."
    assert data.get("count") == 5, f"Expected count 5 in {result_path}, got {data.get('count')}."