# test_final_state.py
import os
import re

def test_script_exists_and_has_loop():
    script_path = "/home/user/analyze_mutations.sh"
    assert os.path.exists(script_path), f"Script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert re.search(r'\b(for|while)\b', content), "The script must contain a Bash loop (for or while)."

def test_report_exists_and_correct():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"Report {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read()

    # Check Base Rate B
    base_rate_match = re.search(r'Base Rate B:\s*([0-9.]+)', content)
    assert base_rate_match, "Could not find 'Base Rate B:' in report.txt."
    base_rate = float(base_rate_match.group(1))
    assert abs(base_rate - 0.3950) < 1e-4, f"Expected Base Rate B to be 0.3950, got {base_rate}."

    # Check Divergence Gen
    div_gen_match = re.search(r'Divergence Gen:\s*([0-9]+)', content)
    assert div_gen_match, "Could not find 'Divergence Gen:' in report.txt."
    div_gen = int(div_gen_match.group(1))
    assert div_gen == 25, f"Expected Divergence Gen to be 25, got {div_gen}."

    # Check Bootstrap 2.5%
    boot_low_match = re.search(r'Bootstrap 2\.5%:\s*([0-9.]+)', content)
    assert boot_low_match, "Could not find 'Bootstrap 2.5%:' in report.txt."
    boot_low = float(boot_low_match.group(1))
    assert 0.2 < boot_low < 0.5, f"Bootstrap 2.5% value {boot_low} is outside expected range."

    # Check Bootstrap 97.5%
    boot_high_match = re.search(r'Bootstrap 97\.5%:\s*([0-9.]+)', content)
    assert boot_high_match, "Could not find 'Bootstrap 97.5%:' in report.txt."
    boot_high = float(boot_high_match.group(1))
    assert 0.3 < boot_high < 0.6, f"Bootstrap 97.5% value {boot_high} is outside expected range."

    assert boot_low <= boot_high, "Bootstrap 2.5% should be less than or equal to Bootstrap 97.5%."