# test_final_state.py
import os
import subprocess
import re

def test_compilation():
    """Verify that the project compiles cleanly with make."""
    build_dir = "/home/user/api_server"

    # Clean first
    subprocess.run(["make", "clean"], cwd=build_dir, capture_output=True)

    # Make
    result = subprocess.run(["make"], cwd=build_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with error:\n{result.stderr}"

    # Check if executable exists
    assert os.path.isfile(os.path.join(build_dir, "server")), "Executable 'server' was not created."

def test_test_results_log():
    """Verify that the test_results.log contains the expected HTTP status codes."""
    log_path = "/home/user/api_server/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected = ["200", "200", "429"]
    assert lines == expected, f"Expected {expected} in {log_path}, but got {lines}"

def test_api_c_memory_leak_fixed():
    """Verify that api.c frees the allocated memory in the error path."""
    api_c_path = "/home/user/api_server/api.c"
    assert os.path.isfile(api_c_path), f"{api_c_path} does not exist."

    with open(api_c_path, "r") as f:
        content = f.read()

    # Find the block where 400 is returned.
    # We expect free(ctx->ip_addr) and free(ctx) before return 400;
    error_path_match = re.search(r'if\s*\([^)]*\)\s*\{([^}]*return\s+400\s*;[^}]*)\}', content)
    assert error_path_match is not None, "Could not find the error path returning 400 in api.c."

    error_block = error_path_match.group(1)
    assert "free(ctx->ip_addr)" in error_block or "free(ctx->ip_addr);" in error_block.replace(" ", ""), "Missing free(ctx->ip_addr) in the error path of api.c."
    assert "free(ctx)" in error_block or "free(ctx);" in error_block.replace(" ", ""), "Missing free(ctx) in the error path of api.c."

def test_hash_c_clobber_fixed():
    """Verify that hash.c includes the missing clobber register in the inline assembly."""
    hash_c_path = "/home/user/api_server/hash.c"
    assert os.path.isfile(hash_c_path), f"{hash_c_path} does not exist."

    with open(hash_c_path, "r") as f:
        content = f.read()

    # Extract the asm block
    asm_match = re.search(r'__asm__\s*\((.*?)\);', content, re.DOTALL)
    assert asm_match is not None, "Could not find the __asm__ block in hash.c."

    asm_block = asm_match.group(1)

    # Check for clobber list containing "%eax" or "%rax" or "eax" or "rax"
    # The clobber list is the third colon-separated section after the assembly string.
    parts = asm_block.split(':')
    assert len(parts) >= 4, "The inline assembly block does not have a clobber list."

    clobber_list = parts[-1]
    assert "eax" in clobber_list or "rax" in clobber_list, "The clobber list in hash.c does not contain '%eax' or '%rax'."