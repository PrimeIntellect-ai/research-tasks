# test_final_state.py

import os
import random
import subprocess
import pytest

def test_firewall_block_script():
    """Test that the firewall block script contains the correct iptables rule."""
    script_path = "/home/user/firewall_block.sh"
    assert os.path.exists(script_path), f"Script not found at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file"

    with open(script_path, "r") as f:
        content = f.read().strip()

    # Check for essential components of the iptables command
    assert "iptables" in content, "Script does not contain 'iptables' command."
    assert "-A OUTPUT" in content or "-I OUTPUT" in content, "Script does not append or insert to the OUTPUT chain."
    assert "-p tcp" in content, "Script does not specify TCP protocol."
    assert "-d 192.168.45.99" in content, "Script does not specify the correct destination IP (192.168.45.99)."
    assert "--dport 8080" in content, "Script does not specify the correct destination port (8080)."
    assert "-j DROP" in content, "Script does not DROP the traffic."

def test_rust_obfuscator_fuzz_equivalence():
    """Test that the Rust obfuscator behaves exactly like the C obfuscator on random inputs."""
    oracle_path = "/app/c2_obfuscator"
    agent_path = "/home/user/rust_obfuscator/target/release/rust_obfuscator"

    assert os.path.exists(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    random.seed(42)
    iterations = 1000

    for i in range(iterations):
        # Generate random length between 0 and 65536
        length = random.randint(0, 65536)

        # Generate random bytes
        input_data = bytearray(random.getrandbits(8) for _ in range(length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data,
            capture_output=True
        )

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=input_data,
            capture_output=True
        )

        # Check exit codes
        assert agent_proc.returncode == oracle_proc.returncode, \
            f"Exit code mismatch on iteration {i} (len={length}). Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

        # Check outputs
        if agent_proc.stdout != oracle_proc.stdout:
            # Truncate output for error message if it's too long
            out_oracle = oracle_proc.stdout[:100].hex() + ("..." if len(oracle_proc.stdout) > 100 else "")
            out_agent = agent_proc.stdout[:100].hex() + ("..." if len(agent_proc.stdout) > 100 else "")
            pytest.fail(f"Output mismatch on iteration {i} (len={length}).\nOracle stdout (hex): {out_oracle}\nAgent stdout (hex): {out_agent}")