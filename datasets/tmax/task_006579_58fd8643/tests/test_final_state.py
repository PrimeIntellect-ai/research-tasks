# test_final_state.py
import os

APP_DIR = "/home/user/app"
GCD_CALC = os.path.join(APP_DIR, "gcd_calc")
PROP_TEST_SH = os.path.join(APP_DIR, "prop_test.sh")
TEST_REPORT_LOG = os.path.join(APP_DIR, "test_report.log")

def test_gcd_calc_exists_and_executable():
    assert os.path.exists(GCD_CALC), f"Expected executable {GCD_CALC} does not exist. Did you fix and run build.sh?"
    assert os.path.isfile(GCD_CALC), f"{GCD_CALC} is not a file."
    assert os.access(GCD_CALC, os.X_OK), f"{GCD_CALC} is not executable."

def test_prop_test_sh_exists():
    assert os.path.exists(PROP_TEST_SH), f"Expected script {PROP_TEST_SH} does not exist."
    assert os.path.isfile(PROP_TEST_SH), f"{PROP_TEST_SH} is not a file."

def test_test_report_log_content():
    assert os.path.exists(TEST_REPORT_LOG), f"Expected log file {TEST_REPORT_LOG} does not exist. Did you run prop_test.sh?"
    assert os.path.isfile(TEST_REPORT_LOG), f"{TEST_REPORT_LOG} is not a file."

    with open(TEST_REPORT_LOG, "r") as f:
        lines = f.readlines()

    non_empty_lines = [line.strip() for line in lines if line.strip()]
    assert len(non_empty_lines) > 0, f"{TEST_REPORT_LOG} is empty."

    last_line = non_empty_lines[-1]
    assert last_line == "ALL PROPERTIES PASSED", f"Expected log to end with 'ALL PROPERTIES PASSED', but got '{last_line}'."