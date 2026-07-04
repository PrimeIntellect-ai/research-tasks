# test_final_state.py
import os
import subprocess
import random

def test_detect_script_accuracy():
    script_path = "/home/user/detect.sh"
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

    # Base test cases from the prompt
    base_cases = [
        ("test.txt", 0),
        ("images/pic.png", 0),
        ("../etc/passwd", 0),
        ("....//etc/passwd", 1),
        ("images/....//secret.txt", 1),
        ("..../....//", 0),
        ("..././", 1),
    ]

    # Generate more test cases to reach 1000
    # We'll use a mix of known patterns
    test_cases = list(base_cases)
    random.seed(42)

    for _ in range(1000 - len(base_cases)):
        choice = random.randint(0, 4)
        if choice == 0:
            test_cases.append((f"dir{random.randint(1,100)}/file.txt", 0))
        elif choice == 1:
            test_cases.append((f"../" * random.randint(1, 4) + "file.txt", 0))
        elif choice == 2:
            test_cases.append((f"....//" * random.randint(1, 4) + "file.txt", 1))
        elif choice == 3:
            test_cases.append((f"..././" * random.randint(1, 4) + "file.txt", 1))
        else:
            # Some random combinations
            test_cases.append((f"images/....//data{random.randint(1,100)}.txt", 1))

    random.shuffle(test_cases)

    test_input = "\n".join([tc[0] for tc in test_cases])
    expected = [tc[1] for tc in test_cases]

    try:
        process = subprocess.run(
            ["/bin/bash", script_path],
            input=test_input,
            text=True,
            capture_output=True,
            timeout=15
        )
    except subprocess.TimeoutExpired:
        assert False, "Script execution timed out after 15 seconds"

    assert process.returncode == 0, f"Script exited with error code {process.returncode}\nStderr: {process.stderr}"

    outputs = process.stdout.strip().split("\n")
    assert len(outputs) == len(expected), f"Expected {len(expected)} lines of output, got {len(outputs)}"

    correct = 0
    for out, exp in zip(outputs, expected):
        if str(out).strip() == str(exp):
            correct += 1

    accuracy = correct / len(expected)
    assert accuracy >= 0.95, f"Accuracy: {accuracy:.4f} is below the threshold of 0.95"