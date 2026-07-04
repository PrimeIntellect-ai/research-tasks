# test_final_state.py

import os
import subprocess
import shutil

def test_nginx_conf_fixed():
    conf_path = "/home/user/nginx/conf/alice.conf"
    assert os.path.isfile(conf_path), f"Nginx config missing: {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    expected_proxy = "http://unix:/home/user/apps/alice/app.sock"
    assert expected_proxy in content, f"Nginx config does not contain the correct proxy_pass: {expected_proxy}"
    assert "/tmp/wrong.sock" not in content, "Nginx config still contains the old wrong socket path."

def test_pre_receive_hook_exists_and_executable():
    hook_path = "/home/user/git/alice.git/hooks/pre-receive"
    assert os.path.isfile(hook_path), f"Git hook missing: {hook_path}"
    assert os.access(hook_path, os.X_OK), f"Git hook is not executable: {hook_path}"

def test_pre_receive_hook_logic():
    hook_path = "/home/user/git/alice.git/hooks/pre-receive"
    apps_dir = "/home/user/apps/alice"
    dummy_file = os.path.join(apps_dir, "dummy_large_file.bin")

    # Ensure apps dir exists
    os.makedirs(apps_dir, exist_ok=True)

    try:
        # Create a file larger than 50,000,000 bytes (e.g., 51 MB)
        with open(dummy_file, "wb") as f:
            f.seek((51 * 1024 * 1024) - 1)
            f.write(b"\0")

        # Run the hook
        result_exceeded = subprocess.run([hook_path], capture_output=True, text=True)

        assert result_exceeded.returncode == 1, "Hook should exit with code 1 when quota is exceeded."
        assert result_exceeded.stdout.strip() == "Error: Quota exceeded", "Hook output did not match exactly 'Error: Quota exceeded'."

        # Remove the large file
        os.remove(dummy_file)

        # Run the hook again
        result_ok = subprocess.run([hook_path], capture_output=True, text=True)

        assert result_ok.returncode == 0, "Hook should exit with code 0 when within quota."

    finally:
        # Cleanup just in case
        if os.path.exists(dummy_file):
            os.remove(dummy_file)

def test_admin_tool_flag():
    flag_path = "/home/user/alice_unlocked.flag"
    assert os.path.isfile(flag_path), f"Flag file missing: {flag_path}. The admin tool was likely not run successfully."

    with open(flag_path, "r") as f:
        content = f.read()

    assert content == "UNLOCKED\n", f"Flag file content is incorrect: {repr(content)}"

def test_fix_site_script_exists():
    script_path = "/home/user/fix_site.py"
    assert os.path.isfile(script_path), f"Automation script missing: {script_path}"