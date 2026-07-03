# test_final_state.py
import os
import subprocess

def test_version_map_exists():
    assert os.path.isfile("/home/user/telemetry_lib/version.map"), "version.map does not exist in /home/user/telemetry_lib"

def test_shared_libraries_exist():
    android_so = "/home/user/telemetry_lib/libtelemetry_android.so"
    ios_so = "/home/user/telemetry_lib/libtelemetry_ios.so"

    assert os.path.isfile(android_so), f"{android_so} does not exist."
    assert os.path.isfile(ios_so), f"{ios_so} does not exist."

def test_android_exports_log():
    log_path = "/home/user/android_exports.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip().splitlines()

    assert content == ["telemetry_init", "telemetry_process"], f"Incorrect content in {log_path}: {content}"

def test_ios_exports_log():
    log_path = "/home/user/ios_exports.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip().splitlines()

    assert content == ["telemetry_init", "telemetry_process"], f"Incorrect content in {log_path}: {content}"

def test_shared_libraries_abi():
    android_so = "/home/user/telemetry_lib/libtelemetry_android.so"
    ios_so = "/home/user/telemetry_lib/libtelemetry_ios.so"

    for so_file in [android_so, ios_so]:
        result = subprocess.run(["nm", "-D", "--defined-only", so_file], capture_output=True, text=True)
        assert result.returncode == 0, f"Failed to run nm on {so_file}"

        exports = result.stdout

        # internal_ functions should not be exported
        assert "internal_parse" not in exports, f"internal_parse is exported in {so_file}, ABI is polluted."
        assert "internal_format" not in exports, f"internal_format is exported in {so_file}, ABI is polluted."

        # telemetry_ functions should be exported
        assert "telemetry_init" in exports, f"telemetry_init is missing from exports in {so_file}."
        assert "telemetry_process" in exports, f"telemetry_process is missing from exports in {so_file}."

def test_shared_libraries_preprocessor_flags():
    android_so = "/home/user/telemetry_lib/libtelemetry_android.so"
    ios_so = "/home/user/telemetry_lib/libtelemetry_ios.so"

    # Check for the strings compiled into the binaries
    result_android = subprocess.run(["strings", android_so], capture_output=True, text=True)
    assert "Android" in result_android.stdout, "The string 'Android' was not found in libtelemetry_android.so. Was -DTARGET_ANDROID used?"

    result_ios = subprocess.run(["strings", ios_so], capture_output=True, text=True)
    assert "iOS" in result_ios.stdout, "The string 'iOS' was not found in libtelemetry_ios.so. Was -DTARGET_IOS used?"