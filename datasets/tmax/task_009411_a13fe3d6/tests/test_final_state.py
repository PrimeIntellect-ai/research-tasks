# test_final_state.py
import os
import json
import pytest

def test_diagnostic_report_exists_and_correct():
    report_path = '/home/user/diagnostic_report.json'
    assert os.path.isfile(report_path), f"Diagnostic report missing at {report_path}"

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    assert "missing_linker_library" in report, "Key 'missing_linker_library' missing in diagnostic report."
    assert report["missing_linker_library"] == "m", "Incorrect missing linker library identified."

    assert "corrected_total_sum" in report, "Key 'corrected_total_sum' missing in diagnostic report."
    assert float(report["corrected_total_sum"]) == 2.0, "Incorrect corrected total sum in diagnostic report."

    assert "first_failing_transaction_id" in report, "Key 'first_failing_transaction_id' missing in diagnostic report."
    assert report["first_failing_transaction_id"] == "TXN-102", "Incorrect first failing transaction ID identified."

def test_build_fix_patch_exists():
    patch_path = '/home/user/support_bundle/build_fix.patch'
    assert os.path.isfile(patch_path), f"Patch file missing at {patch_path}"
    with open(patch_path, 'r') as f:
        content = f.read()
    assert len(content.strip()) > 0, "Patch file is empty."

def test_corrected_sum_txt_exists_and_correct():
    sum_path = '/home/user/support_bundle/corrected_sum.txt'
    assert os.path.isfile(sum_path), f"Corrected sum file missing at {sum_path}"

    with open(sum_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {sum_path} is not a valid number.")

    assert val == 2.0, f"Corrected sum in {sum_path} is incorrect. Expected 2.0, got {val}."