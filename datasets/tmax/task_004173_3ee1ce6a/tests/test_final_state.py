# test_final_state.py

import os
import json
import subprocess
import stat
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_pipeline():
    """Run the pipeline script before executing tests to ensure the state is generated."""
    pipeline_path = '/home/user/pipeline.sh'
    if os.path.isfile(pipeline_path):
        # Ensure it's executable before running
        st = os.stat(pipeline_path)
        if not bool(st.st_mode & stat.S_IXUSR):
            os.chmod(pipeline_path, st.st_mode | stat.S_IXUSR)
        subprocess.run([pipeline_path], capture_output=True, text=True)

def test_scripts_exist_and_executable():
    """Test that all required scripts exist and have executable permissions."""
    scripts = [
        '/home/user/migrate_config.py',
        '/home/user/check_endpoints.py',
        '/home/user/pipeline.sh'
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} is missing."
        st = os.stat(script)
        assert bool(st.st_mode & stat.S_IXUSR), f"Script {script} is not executable."

def test_pipeline_execution_success():
    """Test that pipeline.sh executes successfully."""
    result = subprocess.run(['/home/user/pipeline.sh'], capture_output=True, text=True)
    assert result.returncode == 0, f"pipeline.sh failed with exit code {result.returncode}. Stderr: {result.stderr}"

def test_config_json_content():
    """Test that config.json contains the correct structure and values."""
    config_path = '/home/user/cloud/config.json'
    assert os.path.isfile(config_path), f"{config_path} does not exist."

    with open(config_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{config_path} does not contain valid JSON.")

    assert data.get('cloud_region') == 'us-east-1', "cloud_region is incorrect or missing."

    db = data.get('database', {})
    assert db.get('host') == 'localhost', "database host is incorrect."
    assert db.get('port') in (33060, "33060"), "database port is incorrect."
    assert int(db.get('port')) == 33060, "database port should be 33060."
    assert db.get('user') == 'admin', "database user is incorrect."

    cache = data.get('cache', {})
    assert cache.get('host') == 'localhost', "cache host is incorrect."
    assert cache.get('port') in (63790, "63790"), "cache port is incorrect."
    assert int(cache.get('port')) == 63790, "cache port should be 63790."

def test_migrate_config_idempotency():
    """Test that migrate_config.py is idempotent."""
    result = subprocess.run(['/home/user/migrate_config.py'], capture_output=True, text=True)
    assert result.returncode == 0, f"migrate_config.py failed on subsequent run. Stderr: {result.stderr}"

    # Verify the file is still valid after a second run
    test_config_json_content()

def test_check_endpoints_execution():
    """Test that check_endpoints.py executes successfully and exits with 0."""
    result = subprocess.run(['/home/user/check_endpoints.py'], capture_output=True, text=True)
    assert result.returncode == 0, f"check_endpoints.py failed with exit code {result.returncode}. Stderr: {result.stderr}"

def test_deploy_success_log():
    """Test that the deployment success log contains the expected string."""
    log_path = '/home/user/deploy_success.log'
    assert os.path.isfile(log_path), f"{log_path} does not exist. Pipeline may have failed."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content == "DEPLOYMENT_READY", f"Expected 'DEPLOYMENT_READY' in {log_path}, got '{content}'"