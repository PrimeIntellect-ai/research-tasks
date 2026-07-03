# test_final_state.py

import os
import json
import re
import subprocess

def get_elf_info(filepath):
    # Get entry point
    out_h = subprocess.check_output(['readelf', '-h', filepath], text=True)
    entry_point = None
    for line in out_h.splitlines():
        if 'Entry point address:' in line:
            # Convert to standard hex format (e.g., 0x401000)
            entry_point = hex(int(line.split(':')[1].strip(), 16))
            break

    # Get .text size
    out_s = subprocess.check_output(['readelf', '-W', '-S', filepath], text=True)
    text_size = None
    for line in out_s.splitlines():
        if '.text' in line:
            # Typical wide format: [Nr] Name Type Address Off Size ES Flg Lk Inf Al
            parts = line.split()
            try:
                idx = parts.index('.text')
                # Size is 4 columns after Name (.text -> Type -> Address -> Off -> Size)
                text_size = int(parts[idx + 4], 16)
                break
            except (ValueError, IndexError):
                continue

    return entry_point, text_size

def test_config_json_updated():
    config_path = "/home/user/config.json"
    assert os.path.isfile(config_path), f"Missing configuration file at {config_path}"

    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {config_path} does not contain valid JSON"

    assert config.get('host') == 'localhost', "config.json 'host' should be 'localhost'"
    assert config.get('retries') == '5', "config.json 'retries' should be '5' (applied from WAL txn 1)"
    assert config.get('timeout') == '30', "config.json 'timeout' should be '30' (applied from WAL txn 3)"
    assert 'debug' not in config, "config.json 'debug' should be deleted (applied from WAL txn 4)"

    # Ensure no extra keys were added
    expected_keys = {'host', 'retries', 'timeout'}
    assert set(config.keys()) == expected_keys, f"config.json contains unexpected keys: {set(config.keys()) - expected_keys}"

def test_summary_yaml_created_and_correct():
    summary_path = "/home/user/summary.yaml"
    assert os.path.isfile(summary_path), f"Missing summary file at {summary_path}"

    with open(summary_path, 'r') as f:
        content = f.read()

    # Extract entry point
    ep_match = re.search(r'entry_point:\s*["\']?(0x[0-9a-fA-F]+)["\']?', content)
    assert ep_match, "Could not find valid 'entry_point' in summary.yaml"
    actual_entry_point = ep_match.group(1)

    # Extract text size
    ts_match = re.search(r'text_size:\s*(\d+)', content)
    assert ts_match, "Could not find valid 'text_size' in summary.yaml"
    actual_text_size = int(ts_match.group(1))

    # Extract config keys
    keys_section = re.search(r'config_keys:\s*\n(\s*-\s*\w+\s*\n?)+', content)
    assert keys_section, "Could not find 'config_keys' list in summary.yaml"
    actual_keys = re.findall(r'-\s*(\w+)', keys_section.group(0))

    # Verify against ground truth from /tmp/firmware.elf
    firmware_path = "/tmp/firmware.elf"
    assert os.path.isfile(firmware_path), f"Missing firmware at {firmware_path} to verify against"

    expected_entry_point, expected_text_size = get_elf_info(firmware_path)

    assert expected_entry_point is not None, "Failed to determine expected entry point from firmware"
    assert expected_text_size is not None, "Failed to determine expected .text size from firmware"

    # Hex strings can sometimes have leading zeros depending on formatting, so compare as integers
    assert int(actual_entry_point, 16) == int(expected_entry_point, 16), \
        f"Expected entry_point {expected_entry_point}, but got {actual_entry_point}"

    assert actual_text_size == expected_text_size, \
        f"Expected text_size {expected_text_size}, but got {actual_text_size}"

    expected_keys = ['host', 'retries', 'timeout']
    assert actual_keys == expected_keys, \
        f"Expected config_keys {expected_keys}, but got {actual_keys}"