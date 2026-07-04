# test_final_state.py
import os
import stat
import subprocess
import pytest

def test_rogue_ip_file():
    """Test that rogue_ip.txt contains the correct IP address."""
    file_path = '/home/user/rogue_ip.txt'
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == '203.0.113.42', f"Expected IP '203.0.113.42', but got '{content}' in {file_path}."

def test_secure_run_sh_exists_and_executable():
    """Test that secure_run.sh exists and is executable."""
    script_path = '/home/user/secure_run.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, f"Script {script_path} is not executable."

def test_secure_run_sh_execution():
    """Test that secure_run.sh successfully isolates the network."""
    script_path = '/home/user/secure_run.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    try:
        # Run the wrapper script with `ip link`
        result = subprocess.run(
            [script_path, 'ip', 'link'],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Execution of secure_run.sh timed out.")
    except Exception as e:
        pytest.fail(f"Execution of secure_run.sh failed: {e}")

    assert result.returncode == 0, f"secure_run.sh failed with return code {result.returncode}. Stderr: {result.stderr}"

    output = result.stdout.lower()

    # Check that loopback interface is present
    assert 'lo:' in output or 'loopback' in output, "Loopback interface (lo) not found in the output. The command might not have executed properly."

    # Check that external interfaces (like eth0) are NOT present
    assert 'eth0:' not in output, "Network is not isolated: 'eth0' was found in the output of 'ip link' inside the sandbox."