# test_final_state.py

import os

def test_recovered_payload():
    payload_path = "/home/user/recovered_payload.txt"

    assert os.path.exists(payload_path), f"Output file not found: {payload_path}"

    with open(payload_path, "r") as f:
        content = f.read().strip()

    expected_payload = "PAYMENT_DATA_REQ_77491_SUCCESS"
    assert content == expected_payload, f"Incorrect payload recovered. Expected '{expected_payload}', but got '{content}'"

def test_recover_tx_script_fixed():
    script_path = "/home/user/recover_tx.py"

    if os.path.exists(script_path):
        with open(script_path, "r") as f:
            content = f.read()

        # The buggy line was: payload = data[payload_start : end_idx - 1]
        # It should be fixed to not have the `- 1`
        assert "data[payload_start : end_idx - 1]" not in content, "The off-by-one error in recover_tx.py was not fixed."