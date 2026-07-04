# test_final_state.py

import os
import re
import urllib.parse
import pytest

def test_verification_log():
    """Check if the verification log exists and contains the correct result."""
    log_path = "/home/user/verification.log"
    assert os.path.isfile(log_path), f"The file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read().strip()

    # Expected result: -17 // 5 = -4. -4 * 2 = -8. 10*6 = 60. 60 + (-8) = 52.
    assert content == "52", f"Expected verification.log to contain '52', but found '{content}'"

def test_server_py_fixed():
    """Check if server.py decodes the URL."""
    server_path = "/home/user/math_pr/server.py"
    assert os.path.isfile(server_path), f"The file {server_path} is missing."

    with open(server_path, "r") as f:
        content = f.read()

    assert "unquote" in content, "server.py does not seem to decode the URL using unquote."

def test_mathstack_c_stack_size():
    """Check if the stack size in mathstack.c was increased to at least 100."""
    c_path = "/home/user/math_pr/mathstack.c"
    assert os.path.isfile(c_path), f"The file {c_path} is missing."

    with open(c_path, "r") as f:
        content = f.read()

    # Look for stack array declaration, e.g., int stack[100];
    match = re.search(r'int\s+stack\s*\[\s*(\d+)\s*\]\s*;', content)
    assert match is not None, "Could not find stack array declaration in mathstack.c"

    size = int(match.group(1))
    assert size >= 100, f"Stack size in mathstack.c is {size}, but needs to be at least 100."

def test_mathstack_c_floor_division():
    """Check if mathstack.c implements floor division."""
    c_path = "/home/user/math_pr/mathstack.c"

    with open(c_path, "r") as f:
        content = f.read()

    # The original was stack[top++] = a / b;
    # A correct implementation for floor division usually involves checking signs
    # or using a function like floor(). We will check that it's not just a / b.
    # Note: A simple check is that the line `stack[top++] = a / b;` is changed.

    # We can check if there's logic handling the negative division or different from just `a / b`
    div_block_match = re.search(r'strcmp\(token,\s*"DIV"\)\s*==\s*0\)(.*?)(?:else\s+if|else\s*\{)', content, re.DOTALL)
    if div_block_match:
        div_block = div_block_match.group(1)
        # It shouldn't just be `a / b` without some conditional or modulo/floor logic
        assert ("%" in div_block or "< 0" in div_block or "floor" in div_block or "^" in div_block or "div" in div_block or "a / b" not in div_block or "if" in div_block.replace("if (b == 0)", "").replace("if (top < 2)", "")), "mathstack.c does not seem to implement floor division correctly."

def test_extension_built():
    """Check if the C extension was built."""
    dir_path = "/home/user/math_pr"
    files = os.listdir(dir_path)
    so_files = [f for f in files if f.startswith("mathstack.") and f.endswith(".so")]
    assert len(so_files) > 0, "The mathstack C extension (.so file) was not found in /home/user/math_pr."