# test_final_state.py
import os
import pytest

def test_metric_result():
    """Check that the average shortest path distance is correctly calculated and written."""
    result_file = "/home/user/metric_result.txt"

    assert os.path.exists(result_file), f"Expected result file {result_file} does not exist."
    assert os.path.isfile(result_file), f"{result_file} is not a file."

    try:
        with open(result_file, "r") as f:
            content = f.read().strip()
            agent_val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {result_file} as a float. Content: '{content}'")
    except Exception as e:
        pytest.fail(f"Error reading {result_file}: {e}")

    reference = 7.4
    threshold = 0.05
    diff = abs(agent_val - reference)

    assert diff <= threshold, (
        f"The calculated average shortest path ({agent_val}) differs from the expected "
        f"value ({reference}) by {diff}, which is greater than the allowed threshold of {threshold}."
    )