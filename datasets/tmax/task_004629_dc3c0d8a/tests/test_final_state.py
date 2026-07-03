# test_final_state.py
import os
import pytest

def get_users_info():
    passwd_path = "/home/user/mock_passwd"
    assert os.path.isfile(passwd_path), f"{passwd_path} is missing"

    users = []
    with open(passwd_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(":")
            if len(parts) >= 6:
                users.append({
                    "username": parts[0],
                    "gid": parts[3],
                    "homedir": parts[5]
                })
    return users

def test_symlinks_updated():
    users = get_users_info()
    v1_target = "/home/user/releases/v1/config.ini"
    v2_target = "/home/user/releases/v2/config.ini"

    for user in users:
        symlink_path = os.path.join(user["homedir"], "app_config")
        assert os.path.islink(symlink_path), f"Symlink {symlink_path} is missing or not a symlink"

        target = os.readlink(symlink_path)
        if user["gid"] == "1001":
            assert target == v2_target, f"Symlink for {user['username']} (GID 1001) should point to {v2_target}, but points to {target}"
        else:
            assert target == v1_target, f"Symlink for {user['username']} (GID != 1001) should point to {v1_target}, but points to {target}"

def test_logrotate_updates_content():
    users = get_users_info()
    expected_blocks = []

    for user in users:
        if user["gid"] == "1001":
            block = (
                f"{user['homedir']}/logs/*.log {{\n"
                "    daily\n"
                "    rotate 7\n"
                "    compress\n"
                "}"
            )
            expected_blocks.append(block)

    expected_content = "\n".join(expected_blocks) + "\n"

    conf_path = "/home/user/logrotate_updates.conf"
    assert os.path.isfile(conf_path), f"{conf_path} is missing"

    with open(conf_path, "r") as f:
        actual_content = f.read()

    # Normalize newlines and strip trailing whitespace for robust comparison
    expected_normalized = "\n".join(line.rstrip() for line in expected_content.strip().splitlines())
    actual_normalized = "\n".join(line.rstrip() for line in actual_content.strip().splitlines())

    assert actual_normalized == expected_normalized, (
        f"Content of {conf_path} does not match expected format.\n"
        f"Expected:\n{expected_normalized}\n\nActual:\n{actual_normalized}"
    )