# test_final_state.py

import os
import subprocess
import tarfile

def test_protobuf_compiled():
    """Verify that the protobuf file was compiled into Python code."""
    assert os.path.isfile('/home/user/deps_pb2.py'), "deps_pb2.py is missing"
    assert os.path.isfile('/home/user/deps_pb2_grpc.py'), "deps_pb2_grpc.py is missing"

def test_files_exist():
    """Verify that the required Python scripts exist."""
    for filename in ['server.py', 'client.py', 'test_server.py']:
        path = os.path.join('/home/user', filename)
        assert os.path.isfile(path), f"{filename} is missing at {path}"

def test_bundle_list():
    """Verify that bundle_list.txt exists, is sorted, and contains expected libraries."""
    bundle_path = '/home/user/bundle_list.txt'
    assert os.path.isfile(bundle_path), f"bundle_list.txt is missing at {bundle_path}"

    with open(bundle_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert '/usr/bin/sqlite3' in lines, "Missing main binary (/usr/bin/sqlite3) in bundle_list.txt"

    has_libc = any('libc.so' in p for p in lines)
    has_libm = any('libm.so' in p for p in lines)
    assert has_libc, "Missing libc dependency in bundle_list.txt"
    assert has_libm, "Missing libm dependency in bundle_list.txt"

    assert lines == sorted(lines), "bundle_list.txt is not sorted alphabetically"

def test_tar_contents():
    """Verify that minimal_sqlite3.tar exists and contains exactly the files in bundle_list.txt."""
    tar_path = '/home/user/minimal_sqlite3.tar'
    bundle_path = '/home/user/bundle_list.txt'

    assert os.path.isfile(tar_path), f"Tar archive is missing at {tar_path}"
    assert os.path.isfile(bundle_path), f"bundle_list.txt is missing at {bundle_path}"

    with open(bundle_path, 'r') as f:
        expected_paths = set(line.strip() for line in f if line.strip())

    # Check if tar is uncompressed
    assert tarfile.is_tarfile(tar_path), f"{tar_path} is not a valid tar file"

    with tarfile.open(tar_path, 'r') as tar:
        tar_members = tar.getnames()

    # Normalize tar paths (tar might remove leading slash)
    normalized_tar_members = set('/' + m.lstrip('/') for m in tar_members)
    normalized_expected = set('/' + p.lstrip('/') for p in expected_paths)

    assert '/usr/bin/sqlite3' in normalized_tar_members, "Tar archive missing sqlite3"
    assert normalized_expected.issubset(normalized_tar_members), "Tar archive is missing some files from bundle_list.txt"

def test_hypothesis_tests_pass():
    """Verify that the hypothesis tests in test_server.py pass."""
    test_script = '/home/user/test_server.py'
    assert os.path.isfile(test_script), f"{test_script} is missing"

    try:
        subprocess.run(['pytest', test_script], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        assert False, f"Hypothesis tests failed in {test_script}:\n{e.stdout}\n{e.stderr}"