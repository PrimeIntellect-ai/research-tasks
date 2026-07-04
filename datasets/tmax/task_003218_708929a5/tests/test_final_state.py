# test_final_state.py

import os
import json
import pytest

def test_diagnostics_jsonl_valid_lines():
    target_file = "/home/user/diagnostics.jsonl"
    assert os.path.isfile(target_file), f"Output file {target_file} does not exist. Did you run the script?"

    valid_lines = 0
    with open(target_file, "r") as f:
        for line in f:
            try:
                json.loads(line)
                valid_lines += 1
            except ValueError:
                pass

    threshold = 10000
    assert valid_lines >= threshold, (
        f"Expected at least {threshold} valid JSON lines in {target_file}, "
        f"but found {valid_lines}. The output might be corrupted due to race conditions or incomplete."
    )

def test_ujson_installed():
    try:
        import ujson
    except ImportError:
        pytest.fail("ujson module could not be imported. The vendored package was not successfully installed.")

    # Just to be sure it works
    try:
        res = ujson.loads('{"test": 1}')
        assert res == {"test": 1}
    except Exception as e:
        pytest.fail(f"ujson is installed but failed to parse a simple JSON string: {e}")