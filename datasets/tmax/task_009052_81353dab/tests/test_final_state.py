# test_final_state.py

import os
import stat
import subprocess
import re

def test_integrate_script_fixed():
    integrate_script = "/home/user/sim/integrate.sh"
    assert os.path.isfile(integrate_script), f"{integrate_script} does not exist."

    st = os.stat(integrate_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"{integrate_script} is not executable."

    with open(integrate_script, 'r') as f:
        content = f.read()

    assert "dt_new = dt * (err / tol)" not in content, "The bug in step-size adaptation logic was not fixed."

def test_validate_script_exists_and_executable():
    validate_script = "/home/user/sim/validate.sh"
    assert os.path.isfile(validate_script), f"{validate_script} does not exist."

    st = os.stat(validate_script)
    assert bool(st.st_mode & stat.S_IXUSR), f"{validate_script} is not executable."

def test_validate_script_execution_and_output():
    validate_script = "/home/user/sim/validate.sh"

    # Run the validate script
    result = subprocess.run([validate_script], cwd="/home/user/sim", capture_output=True, text=True)
    assert result.returncode == 0, f"{validate_script} failed to execute properly. Error: {result.stderr}"

    rmse_log = "/home/user/sim/rmse.log"
    status_log = "/home/user/sim/status.log"

    assert os.path.isfile(rmse_log), f"{rmse_log} was not created."
    assert os.path.isfile(status_log), f"{status_log} was not created."

    with open(rmse_log, 'r') as f:
        rmse_content = f.read().strip()

    assert re.match(r"^RMSE: 0\.[0-9]{4}$", rmse_content), f"RMSE log format is incorrect. Found: {rmse_content}"

    # Extract the RMSE value to ensure it's < 0.05
    rmse_val = float(rmse_content.split(":")[1].strip())
    assert rmse_val < 0.05, f"RMSE value {rmse_val} is not strictly less than 0.05. The integration fix might be incorrect."

    with open(status_log, 'r') as f:
        status_content = f.read().strip()

    assert status_content == "PASS", f"Status log does not contain 'PASS'. Found: {status_content}"