# test_final_state.py

import os
import subprocess
import pytest

def test_reproducer():
    reproducer_path = "/home/user/reproducer.txt"
    assert os.path.isfile(reproducer_path), f"Expected reproducer file at {reproducer_path} is missing."

    with open(reproducer_path, "r") as f:
        hex_str = f.read().strip()

    try:
        bytes_data = bytes.fromhex(hex_str)
    except ValueError:
        pytest.fail("reproducer.txt does not contain a valid hex string.")

    assert len(bytes_data) >= 3, "Reproducer byte sequence must be at least 3 bytes long to pass the 'Too short' check."
    assert bytes_data[0] == 0xAA, "Reproducer byte sequence must start with 0xAA to pass the magic byte check."

    # The panic occurs when 2 + length > data.len()
    length_field = bytes_data[1]
    assert 2 + length_field > len(bytes_data), "Reproducer byte sequence does not trigger the out-of-bounds condition."

def test_rust_code_compiles_and_passes_tests():
    project_dir = "/home/user/packet_parser"

    # Run the existing tests to ensure code compiles and passes
    res = subprocess.run(
        ["cargo", "test"], 
        cwd=project_dir, 
        capture_output=True, 
        text=True
    )
    assert res.returncode == 0, f"cargo test failed. The code must compile and pass existing tests.\nStdout:\n{res.stdout}\nStderr:\n{res.stderr}"

def test_rust_code_fixes_out_of_bounds():
    project_dir = "/home/user/packet_parser"
    tests_dir = os.path.join(project_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)

    eval_test_path = os.path.join(tests_dir, "eval_test.rs")
    with open(eval_test_path, "w") as f:
        f.write("""
        use packet_parser::process_packet;

        #[test]
        fn test_verify_out_of_bounds_fix() {
            assert_eq!(process_packet(&[0xAA, 0xFF, 0x00, 0x00]), Err("Out of bounds"));
            assert_eq!(process_packet(&[0xAA, 0x05, 0x01, 0x02, 0x03]), Err("Out of bounds"));
        }
        """)

    res = subprocess.run(
        ["cargo", "test", "--test", "eval_test"], 
        cwd=project_dir, 
        capture_output=True, 
        text=True
    )

    # Clean up the test file so we don't leave artifacts
    if os.path.exists(eval_test_path):
        os.remove(eval_test_path)

    assert res.returncode == 0, f"The fix verification failed. Ensure that out-of-bounds conditions return Err(\"Out of bounds\").\nStdout:\n{res.stdout}\nStderr:\n{res.stderr}"