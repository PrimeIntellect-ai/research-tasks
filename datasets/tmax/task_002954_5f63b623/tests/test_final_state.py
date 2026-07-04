# test_final_state.py
import os
import re
import pytest

def test_routing_conf_mse():
    """Test that the routing configuration weights are within the acceptable MSE threshold."""
    routing_file = "/home/user/routing.conf"
    assert os.path.isfile(routing_file), f"Routing configuration file missing at {routing_file}"

    with open(routing_file, "r") as f:
        content = f.read()

    match = re.search(r"route_weights node1=([0-9.]+) node2=([0-9.]+) node3=([0-9.]+)", content)
    assert match is not None, "Routing configuration format is incorrect or missing."

    w1, w2, w3 = float(match.group(1)), float(match.group(2)), float(match.group(3))

    # Ground truth weights derived from the video frames
    # Total frames = 135 (45 + 30 + 60)
    gt_w1, gt_w2, gt_w3 = 45/135, 30/135, 60/135

    mse = ((w1 - gt_w1)**2 + (w2 - gt_w2)**2 + (w3 - gt_w3)**2) / 3.0

    assert mse <= 0.0001, f"MSE {mse} exceeds threshold 0.0001. Weights found: {w1}, {w2}, {w3}"

def test_group_mock():
    """Test that the group_mock file correctly assigns teams to GIDs and users to teams."""
    group_file = "/home/user/group_mock"
    assert os.path.isfile(group_file), f"Group mock file missing at {group_file}"

    with open(group_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    parsed_groups = {}
    for line in lines:
        parts = line.split(":")
        assert len(parts) == 4, f"Invalid group line format: {line}"
        team, pwd, gid, users = parts
        users_list = sorted(users.split(","))
        parsed_groups[team] = {"gid": int(gid), "users": users_list}

    assert "backend" in parsed_groups, "Missing 'backend' team in group_mock"
    assert parsed_groups["backend"]["users"] == ["alice", "charlie"], "Incorrect users in 'backend' team"

    assert "frontend" in parsed_groups, "Missing 'frontend' team in group_mock"
    assert parsed_groups["frontend"]["users"] == ["bob"], "Incorrect users in 'frontend' team"

    assert "devops" in parsed_groups, "Missing 'devops' team in group_mock"
    assert parsed_groups["devops"]["users"] == ["diana"], "Incorrect users in 'devops' team"

    gids = [g["gid"] for g in parsed_groups.values()]
    assert len(set(gids)) == 3, "GIDs must be unique for each team"
    assert all(g >= 2000 for g in gids), "GIDs must start at 2000"

def test_passwd_mock():
    """Test that the passwd_mock file correctly assigns users to UIDs, GIDs, and home directories."""
    passwd_file = "/home/user/passwd_mock"
    group_file = "/home/user/group_mock"

    assert os.path.isfile(passwd_file), f"Passwd mock file missing at {passwd_file}"
    assert os.path.isfile(group_file), f"Group mock file missing at {group_file}"

    with open(group_file, "r") as f:
        group_lines = [line.strip() for line in f if line.strip()]

    team_to_gid = {}
    for line in group_lines:
        parts = line.split(":")
        team_to_gid[parts[0]] = int(parts[2])

    with open(passwd_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    parsed_users = {}
    for line in lines:
        parts = line.split(":")
        assert len(parts) == 7, f"Invalid passwd line format: {line}"
        user, pwd, uid, gid, gecos, home, shell = parts
        parsed_users[user] = {
            "uid": int(uid),
            "gid": int(gid),
            "home": home,
            "shell": shell
        }

    expected_users = {
        "alice": "backend",
        "bob": "frontend",
        "charlie": "backend",
        "diana": "devops"
    }

    assert set(parsed_users.keys()) == set(expected_users.keys()), "Mismatch in expected users in passwd_mock"

    uids = [u["uid"] for u in parsed_users.values()]
    assert len(set(uids)) == 4, "UIDs must be unique for each user"
    assert all(u >= 3000 for u in uids), "UIDs must start at 3000"

    for user, team in expected_users.items():
        assert parsed_users[user]["gid"] == team_to_gid[team], f"User {user} has incorrect GID for team {team}"
        assert parsed_users[user]["home"] == f"/home/{user}", f"User {user} has incorrect home directory"
        assert parsed_users[user]["shell"] == "/bin/bash", f"User {user} has incorrect shell"