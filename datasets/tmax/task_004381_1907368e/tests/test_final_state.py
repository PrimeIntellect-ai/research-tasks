# test_final_state.py
import os
import sys
import subprocess
import tempfile
import pytest

def custom_hash(data: bytes) -> str:
    h = 0x1337BEEF
    for b in data:
        h ^= b
        h = ((h << 3) & 0xFFFFFFFF) | (h >> 29)
    return f"{h:08x}"

def test_analyzer_script_accuracy():
    analyzer_path = "/home/user/analyzer.py"
    assert os.path.exists(analyzer_path), f"Script {analyzer_path} not found."

    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate varied test files evaluating CSP constraints
        test_cases = {
            "ok1.html": (b"<html><body><script src='app.js'></script></body></html>", False),
            "ok2.html": (b"<html><script src=\"https://cdn.trusted.com/lib.js\"></script></html>", False),
            "ok3.html": (b"<div>No scripts here</div>", False),
            "ok4.html": (b"<script src='/absolute/path/to/self.js'></script>", False),
            "ok5.html": (b"<script src='./relative/path.js'></script>", False),
            "bad1.html": (b"<html><script>alert(1)</script></html>", True),
            "bad2.html": (b"<script src='https://evil.com/x.js'></script>", True),
            "bad3.html": (b"<body><object data='x.swf'></object></body>", True),
            "bad4.html": (b"<script src=\"http://cdn.trusted.com/lib.js\"></script>", True),
            "bad5.html": (b"<script type='text/javascript'>console.log(1)</script>", True),
            "bad6.html": (b"<script src='//malicious.com/script.js'></script>", True),
            "bad7.html": (b"<OBJECT data='test'></OBJECT>", True),
        }

        expected_csv_lines = []
        for filename, (content, is_violation) in test_cases.items():
            filepath = os.path.join(tmpdir, filename)
            with open(filepath, "wb") as f:
                f.write(content)
            if is_violation:
                h = custom_hash(content)
                expected_csv_lines.append(f"{filename},{h}")

        expected_csv_lines.sort()

        # Ensure binary is removed to test standalone capability
        if os.path.exists("/app/auth_tool"):
            os.remove("/app/auth_tool")

        output_csv = os.path.join(tmpdir, "output.csv")

        try:
            subprocess.run(
                [sys.executable, analyzer_path, tmpdir, output_csv],
                timeout=15,
                check=True,
                capture_output=True,
                text=True
            )
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Analyzer script failed with return code {e.returncode}. Stderr: {e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail("Analyzer script timed out.")

        assert os.path.exists(output_csv), "Output CSV was not created by the script."

        with open(output_csv, "r") as f:
            agent_lines = [line.strip() for line in f if line.strip()]

        gt_set = set(expected_csv_lines)
        agent_set = set(agent_lines)

        if not gt_set:
            accuracy = 0.0
        else:
            correct = len(gt_set.intersection(agent_set))
            total_evaluated = len(gt_set) + max(0, len(agent_set) - len(gt_set))
            accuracy = correct / total_evaluated

        assert accuracy >= 1.0, (
            f"Metric accuracy = {accuracy:.2f} (Threshold >= 1.0). "
            f"Expected {len(gt_set)} correct rows, got {len(agent_set)} rows. "
            f"Missing: {gt_set - agent_set}, Unexpected: {agent_set - gt_set}"
        )