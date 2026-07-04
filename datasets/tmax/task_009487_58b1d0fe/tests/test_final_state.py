# test_final_state.py

import os
import subprocess

def test_directories_exist():
    """Ensure the required directories were created."""
    directories = [
        "/home/user/k8s-manifests",
        "/home/user/active-manifests",
        "/home/user/network"
    ]
    for d in directories:
        assert os.path.isdir(d), f"Directory {d} is missing or not a directory."

def test_scripts_exist_and_executable():
    """Ensure operator.py exists and operator.sh exists and is executable."""
    assert os.path.isfile("/home/user/operator.py"), "/home/user/operator.py does not exist or is not a file."

    sh_path = "/home/user/operator.sh"
    assert os.path.isfile(sh_path), f"{sh_path} does not exist or is not a file."
    assert os.access(sh_path, os.X_OK), f"{sh_path} is not executable."

def test_lifecycle_state():
    """Ensure the daemon is stopped and the PID file is removed."""
    pid_file = "/home/user/operator.pid"
    assert not os.path.exists(pid_file), f"PID file {pid_file} still exists. The daemon might not have been stopped properly."

    try:
        output = subprocess.check_output(["pgrep", "-f", "operator.py"], text=True)
        assert not output.strip(), "An operator.py process is still running."
    except subprocess.CalledProcessError:
        # pgrep returns 1 when no processes matched, which is the expected state
        pass

def test_routes_conf_contents():
    """Ensure routes.conf contains the correct routing rules with no duplicates."""
    conf_path = "/home/user/network/routes.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_routes = {
        "ip route add 192.168.10.0/24 dev mock0 metric 100",
        "ip route add 10.5.0.0/16 dev mock0 metric 100"
    }

    # Check for missing routes
    for route in expected_routes:
        assert route in lines, f"Missing expected route: '{route}' in {conf_path}"

    # Check for duplicates
    assert len(lines) == len(set(lines)), f"Duplicate lines found in {conf_path}."

    # Check for unexpected routes
    for line in lines:
        assert line in expected_routes, f"Unexpected route found: '{line}' in {conf_path}"

def test_symlinks():
    """Ensure the correct symlinks are created and point to the right files."""
    symlinks = {
        "/home/user/active-manifests/alpha-route.yaml": "/home/user/k8s-manifests/route-alpha.yaml",
        "/home/user/active-manifests/beta-route.yaml": "/home/user/k8s-manifests/route-beta.yaml"
    }

    for link, target in symlinks.items():
        assert os.path.islink(link), f"{link} does not exist or is not a symlink."

        # Resolve the symlink target (in case they used relative paths)
        link_target = os.readlink(link)
        absolute_target = os.path.normpath(os.path.join(os.path.dirname(link), link_target))

        assert absolute_target == target, f"Symlink {link} points to {absolute_target} instead of {target}."