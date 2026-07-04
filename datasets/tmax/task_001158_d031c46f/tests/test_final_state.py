# test_final_state.py

import os
import subprocess
import time
import pytest

def test_finder_binary_exists():
    """Check that the compiled binary exists and is executable."""
    binary_path = "/home/user/finder"
    assert os.path.isfile(binary_path), f"The compiled binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"The file {binary_path} is not executable."

def test_finder_accuracy():
    """Verify the accuracy of the finder program using the metric threshold."""
    passed = 0
    tests = [
        (8443, "AlphaPass"),
        (9090, "Bravo123"),
        (10022, "Charlie!"),
        (1337, "Delta_Key"),
        (8080, "Echo456")
    ]

    for port, pass_val in tests:
        # Start a dummy background process acting as the rogue service
        cmd = [
            "python3", "-c",
            f"import socket, time; s=socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); s.bind(('127.0.0.1', {port})); s.listen(1); time.sleep(10)",
            f"--passphrase={pass_val}"
        ]
        proc = subprocess.Popen(cmd)
        time.sleep(0.5) # Wait for the socket to bind and listen

        try:
            # Run the student's finder program
            out = subprocess.check_output(["/home/user/finder", str(port)], timeout=2).decode('utf-8').strip()
            if out == pass_val:
                passed += 1
        except subprocess.TimeoutExpired:
            pass
        except subprocess.CalledProcessError:
            pass
        except Exception:
            pass
        finally:
            proc.terminate()
            proc.wait()

    accuracy = passed / len(tests)
    assert accuracy >= 1.0, f"Finder accuracy is {accuracy} ({passed}/{len(tests)} correctly identified), expected threshold is >= 1.0"

def test_firewall_rule_script():
    """Check that the firewall script outputs the correct iptables command."""
    script_path = "/home/user/firewall_rule.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    try:
        out = subprocess.check_output(["bash", script_path], timeout=2).decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {script_path} failed: {e}")
    except Exception as e:
        pytest.fail(f"Failed to run {script_path}: {e}")

    expected_command = "iptables -A INPUT -p tcp --dport 8443 -j DROP"
    assert out == expected_command, f"Firewall script output mismatch.\nGot: '{out}'\nExpected: '{expected_command}'"