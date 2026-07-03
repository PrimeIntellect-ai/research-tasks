# test_final_state.py
import os
import json
import pytest

def test_operator_conf():
    conf_path = '/home/user/operator.conf'
    assert os.path.isfile(conf_path), f"{conf_path} is missing. Did you run the setup wizard script?"

    with open(conf_path, 'r') as f:
        content = f.read()

    assert "env=production" in content, f"{conf_path} missing 'env=production'."
    assert "dir=/home/user/manifests/active" in content, f"{conf_path} missing 'dir=/home/user/manifests/active'."

def test_manifest_symlinks():
    active_dir = '/home/user/manifests/active'
    available_dir = '/home/user/manifests/available'

    assert os.path.isdir(active_dir), f"{active_dir} directory is missing."

    app1_link = os.path.join(active_dir, 'app1.yaml')
    app3_link = os.path.join(active_dir, 'app3.yaml')
    app2_link = os.path.join(active_dir, 'app2.yaml')

    assert os.path.islink(app1_link), f"{app1_link} is not a symlink."
    assert os.readlink(app1_link) == os.path.join(available_dir, 'app1.yaml') or os.path.abspath(os.path.join(active_dir, os.readlink(app1_link))) == os.path.join(available_dir, 'app1.yaml'), f"{app1_link} does not point to the correct available manifest."

    assert os.path.islink(app3_link), f"{app3_link} is not a symlink."
    assert os.readlink(app3_link) == os.path.join(available_dir, 'app3.yaml') or os.path.abspath(os.path.join(active_dir, os.readlink(app3_link))) == os.path.join(available_dir, 'app3.yaml'), f"{app3_link} does not point to the correct available manifest."

    assert not os.path.exists(app2_link), f"{app2_link} should not exist because it is not a Deployment."

def test_services_json_dependency():
    json_path = '/home/user/services.json'
    assert os.path.isfile(json_path), f"{json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            services = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON.")

    assert 'operator' in services, "operator block missing in services.json."
    assert services['operator'].get('depends_on') == 'validator', "operator block does not have 'depends_on': 'validator'."

def test_operator_success_log():
    log_path = '/home/user/operator_success.log'
    assert os.path.isfile(log_path), f"{log_path} is missing. Did you run runner.py successfully?"

    with open(log_path, 'r') as f:
        content = f.read()

    assert "All systems nominal." in content, f"{log_path} does not contain the expected success message."