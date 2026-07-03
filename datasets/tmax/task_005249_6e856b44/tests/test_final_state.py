# test_final_state.py
import subprocess
from pathlib import Path

def test_fix_patch_exists():
    patch_path = Path("/home/user/fix.patch")
    assert patch_path.exists(), f"Patch file {patch_path} does not exist."
    assert patch_path.is_file(), f"{patch_path} is not a file."

def test_performance_regression_fixed():
    url = "http://localhost:8000/process?data=verification_payload"

    times = []
    for i in range(5):
        try:
            result = subprocess.run(
                ["curl", "-s", "-w", "%{time_total}", "-o", "/dev/null", url],
                capture_output=True,
                text=True,
                check=True,
                timeout=5
            )
            time_total = float(result.stdout.strip())
            times.append(time_total)
        except subprocess.TimeoutExpired:
            assert False, f"Request {i+1} timed out after 5 seconds. The performance regression was not fixed."
        except subprocess.CalledProcessError as e:
            assert False, f"curl command failed. Is the service running? Error: {e.stderr}"
        except ValueError:
            assert False, f"Failed to parse curl output: {result.stdout}"

    avg_time = sum(times) / len(times)

    assert avg_time <= 0.5, f"Average response time {avg_time:.3f}s exceeds threshold of 0.5s. Times: {times}"