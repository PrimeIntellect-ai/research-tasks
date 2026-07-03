# test_final_state.py
import os
import re

def test_uptime_monitor_c_fixed():
    path = "/home/user/uptime_monitor.c"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read()

    # Check Bug 1 fix
    assert "i <= payload_len" not in content, "Bug 1 (off-by-one) is still present: 'i <= payload_len' found."
    assert re.search(r"i\s*<\s*payload_len", content), "Bug 1 fix not found: expected 'i < payload_len' in the loop condition."

    # Check Bug 2 fix
    assert "1.0 + alpha" not in content, "Bug 2 (EMA formula) is still present: '1.0 + alpha' found."
    assert re.search(r"1\.0\s*-\s*alpha", content), "Bug 2 fix not found: expected '1.0 - alpha' in the EMA formula."

def test_final_ema_value():
    path = "/home/user/final_ema.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you save the output?"

    with open(path, "r") as f:
        content = f.read().strip()

    # Recompute the expected EMA value based on the logic
    # 5 packets, each with avg_latency = 10.0
    ema = 0.0
    alpha = 0.25
    avg_latency = 10.0
    for _ in range(5):
        ema = (alpha * avg_latency) + ((1.0 - alpha) * ema)

    expected_output = f"{ema:.4f}"

    assert content == expected_output, f"Incorrect EMA value in {path}. Expected '{expected_output}', got '{content}'."