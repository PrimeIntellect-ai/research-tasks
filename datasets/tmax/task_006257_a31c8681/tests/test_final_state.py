# test_final_state.py
import os

def test_ci_output_exists():
    """Verify that the ci_output.txt file exists."""
    assert os.path.isfile("/home/user/ci_output.txt"), "The file /home/user/ci_output.txt does not exist."

def test_ci_output_content():
    """Verify that the confidence interval output is correct."""
    with open("/home/user/ci_output.txt", "r") as f:
        content = f.read().strip()

    parts = content.split(",")
    assert len(parts) == 2, f"The file /home/user/ci_output.txt must contain exactly two comma-separated values. Found: {content}"

    try:
        lower = float(parts[0].strip())
        upper = float(parts[1].strip())
    except ValueError:
        assert False, "The values in /home/user/ci_output.txt must be valid numbers."

    assert abs(lower - (-0.2117)) <= 0.0002, f"Expected lower bound approx -0.2117, got {lower}"
    assert abs(upper - 0.1659) <= 0.0002, f"Expected upper bound approx 0.1659, got {upper}"

def test_pipeline_fixed():
    """Verify that the pipeline script no longer contains the obvious data leakage lines."""
    assert os.path.isfile("/home/user/pipeline.py"), "The file /home/user/pipeline.py does not exist."

    with open("/home/user/pipeline.py", "r") as f:
        content = f.read()

    assert "imputer.fit_transform(X)" not in content, "The pipeline.py still contains the data leakage: imputer.fit_transform(X)"
    assert "scaler.fit_transform(X_imputed)" not in content, "The pipeline.py still contains the data leakage: scaler.fit_transform(X_imputed)"