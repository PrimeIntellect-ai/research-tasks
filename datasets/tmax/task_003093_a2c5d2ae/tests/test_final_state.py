# test_final_state.py

import os
import glob
import json
import pytest

def parse_loc_reference(filepath):
    """Reference implementation to parse .loc files correctly."""
    result = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()

    current_key = None
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('[') and line.endswith(']'):
            current_key = line[1:-1]
        elif current_key:
            result[current_key] = line
            current_key = None
    return result

def populate_reference(template_node, translations):
    """Recursively populate the template with translations."""
    if isinstance(template_node, dict):
        return {k: populate_reference(v, translations) if isinstance(v, (dict, list)) else translations.get(k, "") for k, v in template_node.items()}
    elif isinstance(template_node, list):
        return [populate_reference(v, translations) for v in template_node]
    return template_node

def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def test_translation_accuracy():
    data_dir = "/home/user/data"
    output_dir = "/home/user/output"
    template_file = "/home/user/template.json"

    assert os.path.exists(template_file), f"Template file {template_file} is missing."
    with open(template_file, 'r', encoding='utf-8') as f:
        template = json.load(f)

    loc_files = glob.glob(os.path.join(data_dir, "*.loc"))
    assert len(loc_files) > 0, "No .loc files found to process."

    total_keys = 0
    correct_keys = 0

    for loc_file in loc_files:
        basename = os.path.basename(loc_file)
        lang = os.path.splitext(basename)[0]
        output_file = os.path.join(output_dir, f"{lang}.json")

        # Ground truth
        translations = parse_loc_reference(loc_file)
        expected_json = populate_reference(template, translations)
        expected_flat = flatten_dict(expected_json)

        total_keys += len(expected_flat)

        if not os.path.exists(output_file):
            continue

        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                actual_json = json.load(f)
            actual_flat = flatten_dict(actual_json)

            for k, v in expected_flat.items():
                if actual_flat.get(k) == v:
                    correct_keys += 1
        except Exception:
            pass

    assert total_keys > 0, "No keys found in the template."
    accuracy = correct_keys / total_keys
    assert accuracy >= 0.98, f"Accuracy {accuracy:.4f} is below the threshold of 0.98. Correct: {correct_keys}, Total: {total_keys}"

def test_pipeline_log():
    log_file = "/home/user/pipeline.log"
    assert os.path.exists(log_file), f"Log file {log_file} does not exist."

    with open(log_file, 'r', encoding='utf-8') as f:
        log_content = f.read()

    data_dir = "/home/user/data"
    loc_files = glob.glob(os.path.join(data_dir, "*.loc"))

    for loc_file in loc_files:
        basename = os.path.basename(loc_file)
        translations = parse_loc_reference(loc_file)
        expected_log_entry = f"[INFO] Processed {basename}: extracted {len(translations)} keys."
        assert expected_log_entry in log_content, f"Expected log entry not found: {expected_log_entry}"