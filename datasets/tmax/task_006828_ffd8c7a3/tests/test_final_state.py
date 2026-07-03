# test_final_state.py
import os
import re
import pytest

def test_pwned_txt_exists():
    """Verify that the exploit successfully created the pwned.txt file."""
    assert os.path.isfile("/home/user/pwned.txt"), "The file /home/user/pwned.txt was not created. The exploit failed."

def test_makefile_fixed():
    """Verify that the Makefile was fixed to use tabs and include security flags."""
    makefile_path = "/home/user/app/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} does not exist."

    with open(makefile_path, "r") as f:
        content = f.read()

    # Check for tab character
    assert "\tgcc" in content, "The Makefile does not use a tab character for the gcc command."

    # Check for required flags
    assert "-z execstack" in content, "The Makefile is missing the '-z execstack' flag."
    assert "-fno-stack-protector" in content, "The Makefile is missing the '-fno-stack-protector' flag."

def test_processor_executable_exists():
    """Verify that the processor executable was compiled."""
    assert os.path.isfile("/home/user/app/processor"), "The 'processor' executable was not found. Did you run make?"
    assert os.access("/home/user/app/processor", os.X_OK), "The 'processor' file is not executable."

def test_exploit_script_exists():
    """Verify that the exploit script was created."""
    exploit_path = "/home/user/exploit.py"
    assert os.path.isfile(exploit_path), f"{exploit_path} does not exist."

    with open(exploit_path, "r") as f:
        content = f.read()

    # Check for concurrency logic clues
    has_threading = "threading" in content or "Thread" in content
    has_asyncio = "asyncio" in content or "aiohttp" in content
    has_multiprocessing = "multiprocessing" in content or "Process" in content
    assert has_threading or has_asyncio or has_multiprocessing, "The exploit.py script does not seem to contain concurrency logic (threading, asyncio, or multiprocessing)."