# test_final_state.py

import os
import stat

def test_bashrc_updated():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist."
    with open(bashrc_path, "r") as f:
        content = f.read()
    assert "export BACKUP_ENV_ACTIVE=1" in content, ".bashrc does not contain the required export statement."

def test_git_bare_repo_and_hook():
    repo_path = "/home/user/restore_deploy.git"
    assert os.path.isdir(repo_path), f"Bare repo {repo_path} does not exist."
    assert os.path.isdir(os.path.join(repo_path, "objects")), f"{repo_path} does not look like a bare git repo."

    hook_path = os.path.join(repo_path, "hooks", "post-receive")
    assert os.path.isfile(hook_path), f"Hook {hook_path} does not exist."

    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Hook {hook_path} is not executable."

def test_staging_directory_and_binary():
    staging_path = "/home/user/deploy_staging"
    assert os.path.isdir(staging_path), f"Staging directory {staging_path} does not exist."

    bin_path = os.path.join(staging_path, "restore_bin")
    assert os.path.isfile(bin_path), f"Compiled binary {bin_path} does not exist in staging area."
    st = os.stat(bin_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Binary {bin_path} is not executable."

def test_production_restore_files():
    restore_dir = "/home/user/production_restore"
    assert os.path.isdir(restore_dir), f"Restore directory {restore_dir} does not exist."

    for filename in ["data1.bin", "data2.bin"]:
        file_path = os.path.join(restore_dir, filename)
        assert os.path.isfile(file_path), f"Restored file {file_path} does not exist."
        with open(file_path, "r") as f:
            content = f.read()
        assert content == "RESTORED_SUCCESS\n", f"File {file_path} does not contain the correct content."

def test_workspace_setup():
    workspace = "/home/user/workspace"
    assert os.path.isdir(workspace), f"Workspace {workspace} does not exist."
    assert os.path.isdir(os.path.join(workspace, ".git")), f"Workspace {workspace} is not a git repository."

    index_file = os.path.join(workspace, "backup_index.txt")
    assert os.path.isfile(index_file), f"{index_file} does not exist."

    c_file = os.path.join(workspace, "restore_sim.c")
    assert os.path.isfile(c_file), f"{c_file} does not exist."