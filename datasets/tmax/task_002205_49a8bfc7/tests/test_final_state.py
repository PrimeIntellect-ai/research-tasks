# test_final_state.py

import os
import stat
import tarfile
import pytest

def get_expected_excludes(log_path):
    if not os.path.exists(log_path):
        return []

    with open(log_path, 'r') as f:
        content = f.read()

    excludes = []
    blocks = content.split('--BEGIN--')
    for block in blocks:
        if not block.strip():
            continue

        target = None
        has_symlink_loop = False

        for line in block.splitlines():
            line = line.strip()
            if line.startswith('Target:'):
                target = line.split('Target:', 1)[1].strip()
            elif line.startswith('Details:') and 'Symlink loop' in line:
                has_symlink_loop = True

        if target and has_symlink_loop:
            excludes.append(target)

    return sorted(excludes)

def test_script_exists_and_executable():
    script_path = '/home/user/safe_backup.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_exclude_file_correct():
    exclude_path = '/home/user/exclude.txt'
    assert os.path.isfile(exclude_path), f"Exclude file {exclude_path} does not exist."

    with open(exclude_path, 'r') as f:
        actual_excludes = sorted([line.strip() for line in f if line.strip()])

    expected_excludes = get_expected_excludes('/home/user/backup.log')

    assert actual_excludes == expected_excludes, f"Exclude file contents are incorrect. Expected {expected_excludes}, got {actual_excludes}."

def test_tarball_exists_and_valid():
    tar_path = '/home/user/safe_backup.tar.gz'
    assert os.path.isfile(tar_path), f"Archive {tar_path} does not exist."
    assert tarfile.is_tarfile(tar_path), f"Archive {tar_path} is not a valid tarball."

def test_tarball_contents():
    tar_path = '/home/user/safe_backup.tar.gz'
    if not os.path.isfile(tar_path) or not tarfile.is_tarfile(tar_path):
        pytest.skip("Tarball missing or invalid")

    expected_excludes = get_expected_excludes('/home/user/backup.log')

    with tarfile.open(tar_path, 'r:gz') as tar:
        members = tar.getnames()

    # Check that normal files are included
    # Tar might strip leading slashes, so we check for the suffix
    expected_files = [
        'home/user/data/docs/file1.txt',
        'home/user/data/docs/file2.txt',
        'home/user/data/images/pic.jpg'
    ]

    for ef in expected_files:
        # Check if any member ends with the expected file path
        found = any(m.endswith(ef) for m in members)
        assert found, f"Expected file {ef} is missing from the archive."

    # Check that excluded directories are NOT included
    for exc in expected_excludes:
        # Remove leading slash for matching against tar members
        exc_stripped = exc.lstrip('/')

        for m in members:
            m_stripped = m.lstrip('/')
            assert not m_stripped.startswith(exc_stripped), f"Excluded path {exc} was found in the archive as {m}."