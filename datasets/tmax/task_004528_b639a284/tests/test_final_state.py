# test_final_state.py
import os
import re

def test_restore_directory_exists():
    assert os.path.isdir("/home/user/restore"), "The directory /home/user/restore does not exist."

def test_config_updated():
    config_path = "/home/user/restore/config.ini"
    assert os.path.isfile(config_path), f"{config_path} is missing."
    with open(config_path, "r") as f:
        content = f.read()
    assert "upstream=/home/user/backend_service/app.sock" in content, "The upstream socket path in config.ini was not updated correctly."

def test_allowed_users_updated():
    db_path = "/home/user/restore/allowed_users.db"
    assert os.path.isfile(db_path), f"{db_path} is missing."
    with open(db_path, "r") as f:
        users = [line.strip() for line in f]
    assert "backup_operator" in users, "The user 'backup_operator' was not added to allowed_users.db."

def test_run_backend_script():
    script_path = "/home/user/backend_service/run_backend.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    with open(script_path, "r") as f:
        content = f.read()

    # Check for loop
    assert re.search(r'\b(while|until)\b', content), "The run_backend.sh script does not contain a loop to automatically restart the listener."

    # Check for socat or nc and the socket path
    assert re.search(r'\b(socat|nc)\b', content), "The run_backend.sh script does not use socat or nc."
    assert "/home/user/backend_service/app.sock" in content, "The run_backend.sh script does not reference the correct UNIX socket path."

def test_multiplexer_c_fixed():
    c_path = "/home/user/restore/src/multiplexer.c"
    assert os.path.isfile(c_path), f"{c_path} is missing."
    with open(c_path, "r") as f:
        content = f.read()

    # Remove spaces to check for setenv("TZ","UTC",1)
    content_no_spaces = content.replace(" ", "").replace("\t", "")
    assert 'setenv("TZ","UTC",1);' in content_no_spaces, "The multiplexer.c source file does not contain the required setenv call to fix the timezone bug."

def test_restore_success_log():
    log_path = "/home/user/restore_success.log"
    assert os.path.isfile(log_path), f"{log_path} is missing. The multiplexer might not have been compiled, run, or queried correctly."
    with open(log_path, "r") as f:
        content = f.read()
    assert "RESTORE_VALID" in content, "The restore_success.log does not contain the expected response 'RESTORE_VALID'."