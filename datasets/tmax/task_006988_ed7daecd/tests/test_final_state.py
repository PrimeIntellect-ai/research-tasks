# test_final_state.py

import os

def test_build_output_exists_and_correct():
    output_path = '/home/user/build_output.txt'
    assert os.path.exists(output_path), f"Verification failed: Output file {output_path} not found. Did you run the script?"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    expected_content = (
        "core_kernel:1.0.4 [none]\n"
        "lib_network:2.1.0 [core_kernel]\n"
        "audio_driver:1.1.2 [core_kernel]"
    )

    assert content == expected_content, "Verification failed: Content of build_output.txt does not match expected output. Ensure malformed lines are skipped entirely."