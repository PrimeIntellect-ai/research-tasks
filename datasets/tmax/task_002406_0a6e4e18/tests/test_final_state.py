# test_final_state.py

import os
import csv
import json
import re
import xml.etree.ElementTree as ET
import configparser
import stat

def get_expected_data():
    configs_dir = '/home/user/configs'
    expected_rows = []

    for filename in os.listdir(configs_dir):
        filepath = os.path.join(configs_dir, filename)
        if not os.path.isfile(filepath):
            continue

        fmt = filename.split('.')[-1]
        port = None
        memory_str = None

        if fmt == 'json':
            with open(filepath, 'r') as f:
                data = json.load(f)
                port = data['app']['port']
                memory_str = data['app']['memory']
        elif fmt == 'xml':
            tree = ET.parse(filepath)
            root = tree.getroot()
            app = root.find('app')
            port = int(app.find('port').text)
            memory_str = app.find('memory').text
        elif fmt == 'ini':
            config = configparser.ConfigParser()
            config.read(filepath)
            port = int(config['app']['port'])
            memory_str = config['app']['memory']
        else:
            continue

        if memory_str.endswith('M'):
            memory_mb = int(memory_str[:-1])
        elif memory_str.endswith('G'):
            memory_mb = int(memory_str[:-1]) * 1024
        else:
            memory_mb = int(memory_str)

        expected_rows.append([filename, fmt, str(port), str(memory_mb)])

    expected_rows.sort(key=lambda x: x[0])
    return expected_rows

def test_audit_script_exists_and_executable():
    script_path = '/home/user/audit.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_audit_script_uses_parallelization():
    script_path = '/home/user/audit.sh'
    with open(script_path, 'r') as f:
        content = f.read()

    # Check for common parallelization constructs in bash
    has_parallel = re.search(r'\b(parallel|xargs\s+-P|&)\b', content)
    assert has_parallel, "Script does not seem to implement parallel data processing (missing '&', 'xargs -P', or 'parallel')."

def test_config_audit_csv_correctness():
    csv_path = '/home/user/config_audit.csv'
    assert os.path.isfile(csv_path), f"Output file {csv_path} does not exist."

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."

    header = rows[0]
    expected_header = ['filename', 'format', 'port', 'memory_mb']
    assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}."

    data_rows = rows[1:]
    expected_data = get_expected_data()

    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} data rows, got {len(data_rows)}."

    for i, (actual, expected) in enumerate(zip(data_rows, expected_data)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."