# test_final_state.py
import os
import sys
import subprocess
import pytest

def test_assembler_fixed():
    """Verify that the JNZ bug in assembler.py has been fixed."""
    file_path = "/home/user/repo/assembler.py"
    assert os.path.isfile(file_path), "assembler.py is missing."
    with open(file_path, "r") as f:
        content = f.read()

    # Check that the relative jump is replaced by an absolute jump
    content_no_spaces = content.replace(" ", "")
    assert "self.pc=int(parts[1])" in content_no_spaces, "The JNZ instruction does not perform an absolute jump (self.pc = int(parts[1]))."
    assert "self.pc+=int(parts[1])" not in content_no_spaces, "The JNZ instruction still contains the relative jump bug."

def test_test_assembler_passes():
    """Verify that test_assembler.py has been fixed and all tests pass."""
    file_path = "/home/user/repo/test_assembler.py"
    assert os.path.isfile(file_path), "test_assembler.py is missing."

    result = subprocess.run(
        [sys.executable, "-m", "pytest", file_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Tests in test_assembler.py failed to pass. Output:\n{result.stdout}\n{result.stderr}"

def test_program_asm_output():
    """Verify that program.asm exists, runs successfully, and leaves 15 on top of the stack."""
    repo_path = "/home/user/repo"
    if repo_path not in sys.path:
        sys.path.insert(0, repo_path)

    try:
        from assembler import AssemblerVM
    except ImportError:
        pytest.fail("Could not import AssemblerVM from assembler.py")

    asm_path = os.path.join(repo_path, "program.asm")
    assert os.path.isfile(asm_path), "program.asm is missing."

    with open(asm_path, "r") as f:
        code = f.read()

    vm = AssemblerVM()
    try:
        vm.run(code)
    except Exception as e:
        pytest.fail(f"Execution of program.asm failed with an exception: {e}")

    assert len(vm.stack) > 0, "The stack is empty after running program.asm. Expected 15 on top."
    assert vm.stack[-1] == 15, f"Expected 15 on top of the stack, but got {vm.stack[-1]}."