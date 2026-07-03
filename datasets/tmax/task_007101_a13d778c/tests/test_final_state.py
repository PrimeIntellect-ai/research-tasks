# test_final_state.py
import os
import subprocess
import shutil
import pwd

def run_as_user(cmd, cwd):
    """Run a command as 'user' if currently root, otherwise run normally."""
    current_user = pwd.getpwuid(os.getuid()).pw_name
    if current_user == 'user':
        return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True)
    else:
        return subprocess.run(["su", "user", "-c", f"cd {cwd} && {cmd}"], capture_output=True)

def test_fix_patch_exists_and_valid():
    patch_file = "/home/user/web-app/fix.patch"
    assert os.path.isfile(patch_file), f"Patch file {patch_file} is missing."

    with open(patch_file, "r") as f:
        content = f.read()

    # The patch should add json_serializer.o to the linking step
    assert "json_serializer.o" in content, "The patch file does not appear to add json_serializer.o to the Makefile."
    assert "---" in content and "+++" in content, "The patch file does not look like a unified diff."

def test_ci_test_executable():
    ci_script = "/home/user/web-app/ci_test.sh"
    assert os.path.isfile(ci_script), f"CI script {ci_script} is missing."
    assert os.access(ci_script, os.X_OK), f"CI script {ci_script} is not executable."

def test_ci_test_success():
    ci_script = "/home/user/web-app/ci_test.sh"
    result = run_as_user("./ci_test.sh", "/home/user/web-app")
    assert result.returncode == 0, (
        f"ci_test.sh failed when it should have succeeded.\n"
        f"Stdout: {result.stdout.decode()}\n"
        f"Stderr: {result.stderr.decode()}"
    )

def test_ci_test_failure_on_bad_output():
    ci_script = "/home/user/web-app/ci_test.sh"
    main_c = "/home/user/web-app/main.c"
    backup_main_c = "/home/user/web-app/main.c.bak"

    # Backup main.c
    shutil.copy(main_c, backup_main_c)

    try:
        # Replace main.c with code that outputs the wrong string
        bad_main = """#include <stdio.h>
int main() {
    printf("BAD OUTPUT");
    return 0;
}
"""
        with open(main_c, "w") as f:
            f.write(bad_main)

        result = run_as_user("./ci_test.sh", "/home/user/web-app")
        assert result.returncode == 1, (
            "ci_test.sh should exit with code 1 when the application output does not match the expected JSON. "
            f"It exited with code {result.returncode} instead."
        )
    finally:
        # Restore main.c
        shutil.move(backup_main_c, main_c)