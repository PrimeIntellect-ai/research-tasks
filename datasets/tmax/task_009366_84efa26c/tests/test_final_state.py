# test_final_state.py
import os
import subprocess
import pytest

def test_crash_func_txt():
    path = "/home/user/crash_func.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you analyze the container logs?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "load_obfuscated_module", f"Incorrect function name in {path}. Look closely at the traceback in the container logs."

def test_malware_conf_exists():
    path = "/tmp/.malware_conf_9921"
    assert os.path.isfile(path), f"File {path} does not exist. Did you trace the system calls of dropper.py?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "CONFIG_LOADED", f"File {path} does not contain the correct text."

def test_decoder_fixed():
    path = "/home/user/incident/decoder.py"
    assert os.path.isfile(path), f"File {path} is missing."

    # Run the decoder script to see if the integrity check passes.
    # We can just import it and call check_integrity()
    import sys
    sys.path.insert(0, "/home/user/incident")
    try:
        import decoder
        import importlib
        importlib.reload(decoder) # ensure we get the latest version
        assert decoder.check_integrity() is True, "The check_integrity() function in decoder.py still returns False. Fix the floating-point precision bug."
    except ImportError:
        pytest.fail("Could not import decoder.py")
    finally:
        sys.path.pop(0)

def test_flag_extracted():
    path = "/home/user/flag.txt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the decoder script with the correct key?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "FLAG{pr3c1s10n_m3m0ry_m4st3r_8819}", f"The flag in {path} is incorrect."