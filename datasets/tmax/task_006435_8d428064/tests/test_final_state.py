# test_final_state.py

import os
import subprocess
import tarfile
import stat

def test_provisioner_cpp_exists():
    assert os.path.isfile("/home/user/provisioner.cpp"), "/home/user/provisioner.cpp does not exist"

def test_provisioner_cpp_logic():
    # Compile the cpp file to a temporary location to test its logic
    compile_result = subprocess.run(
        ["g++", "/home/user/provisioner.cpp", "-o", "/tmp/test_prov"],
        capture_output=True
    )
    assert compile_result.returncode == 0, f"Compilation failed: {compile_result.stderr.decode()}"

    # Test without environment variable
    env = os.environ.copy()
    if "PROVISION_TARGET_DIR" in env:
        del env["PROVISION_TARGET_DIR"]

    run_no_env = subprocess.run(["/tmp/test_prov"], env=env, capture_output=True)
    assert run_no_env.returncode != 0, "Program should exit with non-zero code when PROVISION_TARGET_DIR is not set"

    # Test with environment variable
    test_dir = "/tmp/test_target"
    os.makedirs(test_dir, exist_ok=True)
    env["PROVISION_TARGET_DIR"] = test_dir

    run_with_env = subprocess.run(["/tmp/test_prov"], env=env, capture_output=True)
    assert run_with_env.returncode == 0, "Program should exit with 0 when PROVISION_TARGET_DIR is set"

    status_file = os.path.join(test_dir, "status.txt")
    assert os.path.isfile(status_file), "status.txt was not created in the target directory"

    with open(status_file, "r") as f:
        content = f.read()
    assert content == "SUCCESS\n", f"status.txt content is incorrect. Expected 'SUCCESS\\n', got {repr(content)}"

def test_ci_pipeline_script():
    script_path = "/home/user/ci_pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable"

def test_pipeline_results():
    assert os.path.isfile("/home/user/provisioner"), "/home/user/provisioner executable does not exist"
    assert os.path.isdir("/home/user/target_env"), "/home/user/target_env directory does not exist"

    status_path = "/home/user/target_env/status.txt"
    assert os.path.isfile(status_path), f"{status_path} does not exist"
    with open(status_path, "r") as f:
        assert f.read() == "SUCCESS\n", f"{status_path} does not contain exactly 'SUCCESS\\n'"

def test_release_tarball():
    tar_path = "/home/user/release.tar.gz"
    assert os.path.isfile(tar_path), f"{tar_path} does not exist"

    with tarfile.open(tar_path, "r:gz") as tar:
        names = tar.getnames()
        assert len(names) == 1, f"Tarball should contain exactly 1 file, found {len(names)}: {names}"
        assert names[0] in ["provisioner", "./provisioner"], f"Tarball contains incorrect file: {names[0]}"

def test_bashrc_configuration():
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist"

    with open(bashrc_path, "r") as f:
        lines = f.readlines()

    found = any("export PROVISION_ENV_MODE=production" in line for line in lines)
    assert found, "/home/user/.bashrc does not contain 'export PROVISION_ENV_MODE=production'"