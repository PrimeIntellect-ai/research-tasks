# test_final_state.py

import os
import json
import stat
import pytest

def test_merge_plugins_script_exists():
    """Verify that the Python script exists."""
    assert os.path.isfile('/home/user/merge_plugins.py'), "/home/user/merge_plugins.py is missing."

def test_run_e2e_script_exists_and_executable():
    """Verify that the bash script exists and is executable."""
    script_path = '/home/user/run_e2e.sh'
    assert os.path.isfile(script_path), f"{script_path} is missing."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_final_json_exists():
    """Verify that final.json was generated."""
    assert os.path.isfile('/home/user/final.json'), "/home/user/final.json is missing. Did the script run?"

def test_final_json_content_and_sorting():
    """Verify the content and key sorting of final.json."""
    with open('/home/user/final.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/final.json is not valid JSON.")

    expected = {
        "plugins": {
            "auth": {
                "required_version": "1.2.0",
                "status": "active"
            },
            "cache": {
                "required_version": "1.0.0",
                "status": "active"
            },
            "db": {
                "required_version": "2.1.0",
                "status": "active"
            },
            "ui": {
                "required_version": "3.0.0",
                "status": "inactive"
            }
        }
    }

    assert data == expected, "The contents of /home/user/final.json do not match the expected merged output."

    # Verify alphabetical sorting of plugins
    plugins = data.get("plugins", {})
    plugin_keys = list(plugins.keys())
    assert plugin_keys == sorted(plugin_keys), "The plugins in final.json are not sorted alphabetically by name."