# test_final_state.py

import os
import re
import stat

def test_files_exist():
    """Verify that all required files have been created."""
    required_files = [
        "/home/user/ws_api_test/server.js",
        "/home/user/ws_api_test/test.py",
        "/home/user/ws_api_test/run_tests.sh",
        "/home/user/ws_api_test/test_report.log"
    ]
    for file_path in required_files:
        assert os.path.isfile(file_path), f"Required file missing: {file_path}"

def test_runner_executable():
    """Verify that the bash runner script is executable."""
    runner_path = "/home/user/ws_api_test/run_tests.sh"
    assert os.path.isfile(runner_path), f"Runner script missing: {runner_path}"
    st = os.stat(runner_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Runner script is not executable: {runner_path}"

def is_valid_semver(v):
    pattern = r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-zA-Z0-9-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-zA-Z0-9-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
    return re.match(pattern, v) is not None

def is_greater_than_2_0_0(v):
    # Try to use packaging.version if available
    try:
        from packaging.version import Version, InvalidVersion
        try:
            return Version(v) > Version("2.0.0")
        except InvalidVersion:
            return None
    except ImportError:
        # Fallback basic check
        match = re.match(r'^(\d+)\.(\d+)\.(\d+)', v)
        if not match:
            return None
        major, minor, patch = map(int, match.groups())
        if major > 2: return True
        if major == 2 and minor > 0: return True
        if major == 2 and minor == 0 and patch > 0: return True
        return False

def test_log_correctness():
    """Verify that test_report.log has exactly 13 correctly formatted entries with valid semantic logic."""
    log_path = "/home/user/ws_api_test/test_report.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 13, f"Expected exactly 13 test cases in log, found {len(lines)}"

    success_count = 0
    rejected_count = 0
    error_count = 0

    for line in lines:
        parts = line.split(',')
        assert len(parts) == 2, f"Invalid log format (expected 'version,status'): {line}"

        version, status = parts[0], parts[1]
        is_valid = is_valid_semver(version)

        if status == "success":
            success_count += 1
            assert is_valid, f"Expected valid semver > 2.0.0 for success, got invalid: {version}"
            gt_2 = is_greater_than_2_0_0(version)
            assert gt_2 is not False, f"Version {version} is not > 2.0.0 but got 'success'"

        elif status == "rejected":
            rejected_count += 1
            assert is_valid, f"Expected valid semver <= 2.0.0 for rejected, got invalid: {version}"
            gt_2 = is_greater_than_2_0_0(version)
            assert gt_2 is not True, f"Version {version} is > 2.0.0 but got 'rejected'"

        elif status == "error":
            error_count += 1
            assert not is_valid, f"Expected invalid semver for 'error', got valid: {version}"

        else:
            assert False, f"Unknown status '{status}' in log for version {version}"

    assert success_count == 5, f"Expected 5 'success' entries, found {success_count}"
    assert rejected_count == 5, f"Expected 5 'rejected' entries, found {rejected_count}"
    assert error_count == 3, f"Expected 3 'error' entries, found {error_count}"