# test_final_state.py
import os
import subprocess

def test_script_exists_and_executable():
    script_path = "/home/user/analyze_traffic.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable. Did you run chmod +x?"

def test_accuracy_metric():
    script_path = "/home/user/analyze_traffic.sh"

    # We evaluate against the provided dashboard image
    test_cases = [
        ("/app/dashboard.png", "FLAG{sqli_success_123}")
    ]

    correct = 0
    for image_path, expected_output in test_cases:
        assert os.path.isfile(image_path), f"Test image {image_path} is missing."

        try:
            result = subprocess.run(
                [script_path, image_path], 
                capture_output=True, 
                text=True, 
                timeout=15
            )
            if expected_output in result.stdout:
                correct += 1
            else:
                print(f"Script stdout:\n{result.stdout}")
                print(f"Script stderr:\n{result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"Script timed out processing {image_path}")
        except Exception as e:
            print(f"Error running script: {e}")

    accuracy = correct / len(test_cases)
    assert accuracy >= 1.0, f"Accuracy metric failed: {accuracy} < 1.0. The script did not output the correct flag for all test cases."