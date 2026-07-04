# test_final_state.py
import os
import tarfile

def test_curation_log():
    log_path = '/home/user/curation.log'
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(log_path, 'r') as f:
        log_content = f.read()

    expected_loops = [
        'LOOP_DETECTED: /home/user/artifacts/loop1.sym',
        'LOOP_DETECTED: /home/user/artifacts/loop2.sym'
    ]
    for loop in expected_loops:
        assert loop in log_content, f"Missing expected loop detection in log: {loop}"

    expected_locked = 'LOCKED: /home/user/artifacts/locked.dat'
    assert expected_locked in log_content, f"Missing expected locked file in log: {expected_locked}"

def test_safe_artifacts_txt():
    safe_path = '/home/user/safe_artifacts.txt'
    assert os.path.exists(safe_path), f"{safe_path} does not exist."

    with open(safe_path, 'r') as f:
        safe_content = f.read()

    expected_safe_files = [
        '/home/user/artifacts/bin1.dat',
        '/home/user/artifacts/module_a/bin2.dat',
        '/home/user/artifacts/module_b/bin3.dat'
    ]

    for safe_file in expected_safe_files:
        assert safe_file in safe_content, f"Expected safe file missing from {safe_path}: {safe_file}"

    assert 'locked.dat' not in safe_content, f"Locked file should not be in {safe_path}"

def test_safe_archive():
    archive_path = '/home/user/safe_archive.tar.gz'
    assert os.path.exists(archive_path), f"{archive_path} does not exist."

    assert tarfile.is_tarfile(archive_path), f"{archive_path} is not a valid tar file."

    with tarfile.open(archive_path, 'r:gz') as tar:
        names = tar.getnames()

        # The paths in the tarball might be absolute or relative, but the filenames should be present.
        # We'll check if the basenames are in the tarball names
        basenames = [os.path.basename(name) for name in names]

        expected_basenames = ['bin1.dat', 'bin2.dat', 'bin3.dat']
        for expected in expected_basenames:
            assert expected in basenames, f"Expected file {expected} missing from archive {archive_path}"