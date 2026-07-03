# test_final_state.py

import os
import subprocess
import pytest

def test_final_total_file():
    path = "/home/user/final_total.txt"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read().strip()

    assert content == "1060.95", f"Expected final_total.txt to contain '1060.95', but got '{content}'"

def test_aggregate_billing_uses_decimal():
    path = "/home/user/aggregate_billing.py"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, 'r') as f:
        content = f.read()

    assert "decimal" in content.lower(), "aggregate_billing.py does not appear to import or use the decimal module."

def test_test_billing_script_exists_and_passes():
    path = "/home/user/test_billing.py"
    assert os.path.isfile(path), f"File {path} is missing. You must create a regression test file."

    # Run the test file
    # We can use python3 to execute it. If it uses pytest, it might not run anything if executed directly, 
    # but the instructions say "pass successfully when executed with python3 ... or pytest ...".
    # We'll run it with pytest to be safe, or just python3. Let's run it with python3.
    result = subprocess.run(["python3", path], capture_output=True, text=True)
    assert result.returncode == 0, f"Executing {path} failed with error:\n{result.stderr}\n{result.stdout}"

def test_aggregate_billing_functionality():
    import sys
    sys.path.insert(0, "/home/user")
    try:
        import aggregate_billing
    except ImportError:
        pytest.fail("Could not import aggregate_billing.py")

    # Test the fixed logic on a synthetic log
    test_log = "/tmp/test_billing_logs.txt"
    with open(test_log, "w") as f:
        f.write('txn_id=1 Amount="1,234.56"\n')
        f.write('txn_id=2 Amount="N/A"\n')
        f.write('txn_id=3 Amount=""\n')
        f.write('txn_id=4 Amount="0.10"\n')
        f.write('txn_id=5 Amount="0.20"\n')

    try:
        total = aggregate_billing.aggregate_logs(test_log)
        # 1234.56 + 0.10 + 0.20 = 1234.86
        assert str(total) == "1234.86", f"Expected aggregate_logs to return Decimal('1234.86'), but got {total}"
    finally:
        if os.path.exists(test_log):
            os.remove(test_log)