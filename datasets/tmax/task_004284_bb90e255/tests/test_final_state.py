# test_final_state.py

import os
import subprocess
import csv
import math

def test_detector_adversarial_corpus():
    detector_script = "/home/user/detector.sh"
    assert os.path.isfile(detector_script), f"Detector script not found at {detector_script}"
    assert os.access(detector_script, os.X_OK), f"Detector script {detector_script} is not executable"

    evil_dir = "/app/test_data/evil_corpus"
    clean_dir = "/app/test_data/clean_corpus"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_files = sorted([os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.jpg')])
    clean_files = sorted([os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.jpg')])

    assert len(evil_files) > 0, "No evil files found to test."
    assert len(clean_files) > 0, "No clean files found to test."

    evil_bypassed = []
    for f in evil_files:
        res = subprocess.run([detector_script, f], capture_output=True)
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        res = subprocess.run([detector_script, f], capture_output=True)
        if res.returncode != 0:
            clean_modified.append(os.path.basename(f))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_etl_report_format():
    report_path = "/home/user/etl_report.csv"
    assert os.path.isfile(report_path), f"ETL report not found at {report_path}"

    with open(report_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['frame_filename', 'is_glitch', 'brightness', 'fault_probability'], \
            f"CSV header is incorrect. Got: {header}"

        rows = list(reader)
        assert len(rows) >= 15, f"Expected at least 15 frames in the report, got {len(rows)}."

        # Check basic row format
        for i, row in enumerate(rows):
            assert len(row) == 4, f"Row {i+1} does not have exactly 4 columns: {row}"
            frame_filename, is_glitch, brightness, fault_probability = row

            assert is_glitch in ['0', '1'], f"Invalid is_glitch value at row {i+1}: {is_glitch}"

            if is_glitch == '1':
                assert brightness == 'NA', f"Glitch frame should have 'NA' brightness at row {i+1}"
            else:
                assert brightness.isdigit(), f"Valid frame should have integer brightness at row {i+1}"

            try:
                float(fault_probability)
            except ValueError:
                pytest.fail(f"Invalid fault_probability float at row {i+1}: {fault_probability}")

def test_bayesian_update_logic():
    report_path = "/home/user/etl_report.csv"
    assert os.path.isfile(report_path), f"ETL report not found at {report_path}"

    p_fault = 0.05
    p_event_given_fault = 0.8
    p_event_given_no_fault = 0.1

    with open(report_path, 'r') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            is_glitch = row['is_glitch']
            brightness = row['brightness']
            reported_prob = float(row['fault_probability'])

            if is_glitch == '0':
                b_val = int(brightness)
                # Event occurs if brightness < 100
                if b_val < 100:
                    # P(Fault | Event) = P(Event | Fault) * P(Fault) / P(Event)
                    p_event = (p_event_given_fault * p_fault) + (p_event_given_no_fault * (1 - p_fault))
                    p_fault = (p_event_given_fault * p_fault) / p_event
                else:
                    # P(Fault | No Event) = P(No Event | Fault) * P(Fault) / P(No Event)
                    p_no_event_given_fault = 1 - p_event_given_fault
                    p_no_event_given_no_fault = 1 - p_event_given_no_fault
                    p_no_event = (p_no_event_given_fault * p_fault) + (p_no_event_given_no_fault * (1 - p_fault))
                    p_fault = (p_no_event_given_fault * p_fault) / p_no_event

            # Check reported probability matches calculated (rounded to 4 decimal places)
            expected_prob = round(p_fault, 4)
            assert math.isclose(reported_prob, expected_prob, abs_tol=1e-4), \
                f"Row {i+1} ({row['frame_filename']}): Expected probability {expected_prob}, got {reported_prob}"