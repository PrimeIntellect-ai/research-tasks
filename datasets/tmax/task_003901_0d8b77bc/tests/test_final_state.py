# test_final_state.py

import os
import re
import stat

def test_directories_exist():
    """Verify that the required directories exist."""
    dirs = [
        '/home/user/project/src',
        '/home/user/project/data',
        '/home/user/project/build'
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} is missing."

def test_routes_file_moved():
    """Verify that routes.txt was moved to the data directory."""
    assert not os.path.exists('/home/user/project/routes.txt'), "routes.txt should have been moved from /home/user/project/."
    assert os.path.isfile('/home/user/project/data/routes.txt'), "routes.txt is missing in /home/user/project/data/."

def test_mapper_source_exists():
    """Verify that mapper.c was created."""
    assert os.path.isfile('/home/user/project/src/mapper.c'), "mapper.c source file is missing."

def test_binaries_exist_and_executable():
    """Verify that the compiled binaries exist and are executable."""
    binaries = [
        '/home/user/project/build/mapper_prod',
        '/home/user/project/build/mapper_test'
    ]
    for b in binaries:
        assert os.path.isfile(b), f"Binary {b} is missing."
        assert os.access(b, os.X_OK), f"Binary {b} is not executable."

def compute_expected_output(routes_file_path, seed):
    """Helper to compute the expected output given the routes file and a seed."""
    expected_lines = []
    with open(routes_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('->')
            if len(parts) == 2:
                url = parts[0].strip()
                method = parts[1].strip()

                # Strip parameters enclosed in {}
                stripped_url = re.sub(r'\{[^}]*\}', '', url)

                sum_url = sum(ord(c) for c in stripped_url)
                sum_method = sum(ord(c) for c in method)

                checksum = (sum_url * sum_method) % seed
                expected_lines.append(f"Checksum: {checksum} | Method: {method}")
    return expected_lines

def test_output_prod_log():
    """Verify the contents of output_prod.log."""
    log_path = '/home/user/project/build/output_prod.log'
    routes_path = '/home/user/project/data/routes.txt'

    assert os.path.isfile(log_path), f"Output log {log_path} is missing."

    expected_lines = compute_expected_output(routes_path, 17)

    with open(log_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {log_path} do not match the expected checksums and format."

def test_output_test_log():
    """Verify the contents of output_test.log."""
    log_path = '/home/user/project/build/output_test.log'
    routes_path = '/home/user/project/data/routes.txt'

    assert os.path.isfile(log_path), f"Output log {log_path} is missing."

    expected_lines = compute_expected_output(routes_path, 31)

    with open(log_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Contents of {log_path} do not match the expected checksums and format."