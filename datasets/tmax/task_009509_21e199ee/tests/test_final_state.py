# test_final_state.py

import os
import re

SUCCESS_LOG = "/home/user/risk_job/success.log"

def test_success_log_exists():
    assert os.path.isfile(SUCCESS_LOG), (
        f"Expected success log file at {SUCCESS_LOG} does not exist. "
        "Did the script run successfully and converge?"
    )

def test_success_log_content():
    assert os.path.isfile(SUCCESS_LOG), (
        f"Cannot check content because {SUCCESS_LOG} does not exist."
    )
    with open(SUCCESS_LOG, "r") as f:
        content = f.read().strip()

    # Check if the content matches the expected convergence value
    # The expected value is around 2.855196
    match = re.search(r"Converged at 2\.85519.*", content)
    assert match is not None, (
        f"Content of {SUCCESS_LOG} ('{content}') does not match the expected "
        "convergence value pattern 'Converged at 2.85519...'."
    )