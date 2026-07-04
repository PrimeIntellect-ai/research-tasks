# test_final_state.py

import os
import json
import stat
import pytest

def test_bare_repo_exists():
    """Ensure the bare Git repository was created."""
    bare_repo_path = "/home/user/git-server/deploy.git"
    assert os.path.isdir(bare_repo_path), f"Bare Git repository not found at {bare_repo_path}"
    assert os.path.isdir(os.path.join(bare_repo_path, "objects")), f"Directory {bare_repo_path} does not appear to be a bare git repository."

def test_deploy_directories_exist():
    """Ensure the deployment directories exist."""
    src_dir = "/home/user/deploy/src"
    out_dir = "/home/user/deploy/out"
    assert os.path.isdir(src_dir), f"Deployment source directory not found at {src_dir}"
    assert os.path.isdir(out_dir), f"Deployment output directory not found at {out_dir}"

def test_post_receive_hook_exists_and_executable():
    """Ensure the post-receive hook exists and is executable."""
    hook_path = "/home/user/git-server/deploy.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"post-receive hook not found at {hook_path}"
    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"post-receive hook at {hook_path} is not executable."

def test_workspace_exists():
    """Ensure the workspace directory exists and has the required files."""
    workspace_dir = "/home/user/workspace"
    assert os.path.isdir(workspace_dir), f"Workspace directory not found at {workspace_dir}"
    assert os.path.isdir(os.path.join(workspace_dir, ".git")), f"Workspace at {workspace_dir} is not a git repository."

    fstab_path = os.path.join(workspace_dir, "virtual_fstab")
    network_path = os.path.join(workspace_dir, "network_links.txt")
    assert os.path.isfile(fstab_path), f"File {fstab_path} not found in workspace."
    assert os.path.isfile(network_path), f"File {network_path} not found in workspace."

def test_xfs_volumes_output():
    """Ensure the xfs_volumes.txt file is correctly generated."""
    xfs_file = "/home/user/deploy/out/xfs_volumes.txt"
    assert os.path.isfile(xfs_file), f"Output file not found at {xfs_file}"

    with open(xfs_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = [
        "/app/cache",
        "/app/logs",
        "/opt/db"
    ]

    assert lines == expected, f"Contents of {xfs_file} do not match the expected sorted xfs mount points. Got: {lines}"

def test_mesh_json_output():
    """Ensure the mesh.json file is correctly generated."""
    json_file = "/home/user/deploy/out/mesh.json"
    assert os.path.isfile(json_file), f"Output file not found at {json_file}"

    with open(json_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_file} does not contain valid JSON.")

    expected = {
        "api-gateway": [
            "user-service:8080",
            "payment-service:8443"
        ],
        "user-service": [
            "postgres-db:5432"
        ],
        "payment-service": [
            "postgres-db:5432"
        ]
    }

    # Compare structure, ignoring order of keys, but order of list elements might matter. 
    # The requirement says "a list of strings formatted as target_service:port".
    # Sort lists to be robust against ordering differences.
    for k in data:
        if isinstance(data[k], list):
            data[k].sort()

    for k in expected:
        expected[k].sort()

    assert data == expected, f"Contents of {json_file} do not match the expected mesh dictionary. Got: {data}"