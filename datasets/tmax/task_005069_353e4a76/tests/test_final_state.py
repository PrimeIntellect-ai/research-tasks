# test_final_state.py

import os
import stat
import subprocess
import pytest

SSH_CONFIG_PATH = "/home/user/.ssh/config"
FSTAB_PATH = "/home/user/port_fstab"
PY_SCRIPT_PATH = "/home/user/tunnel_builder.py"
SH_SCRIPT_PATH = "/home/user/start_tunnels.sh"

def test_ssh_config_exists_and_permissions():
    """Verify .ssh/config exists and has correct permissions."""
    assert os.path.isfile(SSH_CONFIG_PATH), f"{SSH_CONFIG_PATH} is missing"
    st = os.stat(SSH_CONFIG_PATH)
    assert bool(st.st_mode & stat.S_IRUSR), f"{SSH_CONFIG_PATH} must be readable by user"

def test_ssh_config_content():
    """Verify .ssh/config contains the correct jump hosts."""
    with open(SSH_CONFIG_PATH, 'r') as f:
        content = f.read().lower()

    # Check jump_web
    assert "host jump_web" in content, "Missing 'Host jump_web' in ssh config"
    assert "hostname ssh.web-infra.example.com" in content, "Missing correct HostName for jump_web"
    assert "user webops" in content, "Missing correct User for jump_web"
    assert "port 2222" in content, "Missing correct Port for jump_web"

    # Check jump_db
    assert "host jump_db" in content, "Missing 'Host jump_db' in ssh config"
    assert "hostname ssh.data-infra.example.internal" in content, "Missing correct HostName for jump_db"
    assert "user dbadmin" in content, "Missing correct User for jump_db"

def test_port_fstab_content():
    """Verify port_fstab contains the correct entries and a comment."""
    assert os.path.isfile(FSTAB_PATH), f"{FSTAB_PATH} is missing"
    with open(FSTAB_PATH, 'r') as f:
        lines = f.readlines()

    content = "".join(lines)
    assert "#" in content, "port_fstab must contain a comment line starting with #"

    # Check entries (ignoring exact spacing)
    entry1_found = any("8080" in line and "10.1.1.50:80" in line and "jump_web" in line and "-N" in line and "-T" in line for line in lines)
    entry2_found = any("5432" in line and "192.168.100.10:5432" in line and "jump_db" in line and "-N" in line and "-f" in line for line in lines)

    assert entry1_found, "Missing or incorrect entry for port 8080 in port_fstab"
    assert entry2_found, "Missing or incorrect entry for port 5432 in port_fstab"

def test_tunnel_builder_script():
    """Verify tunnel_builder.py executes correctly and generates the bash script."""
    assert os.path.isfile(PY_SCRIPT_PATH), f"{PY_SCRIPT_PATH} is missing"

    # Run the script interactively
    process = subprocess.Popen(
        ['python3', PY_SCRIPT_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input="y\ny\n")

    # Verify prompts
    assert "Enable tunnel to 10.1.1.50:80 on local port 8080?" in stdout, "Missing or incorrect prompt for port 8080"
    assert "Enable tunnel to 192.168.100.10:5432 on local port 5432?" in stdout, "Missing or incorrect prompt for port 5432"

def test_generated_bash_script():
    """Verify start_tunnels.sh is generated correctly and is executable."""
    assert os.path.isfile(SH_SCRIPT_PATH), f"{SH_SCRIPT_PATH} was not generated"

    st = os.stat(SH_SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"{SH_SCRIPT_PATH} is not executable"

    with open(SH_SCRIPT_PATH, 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) > 0, f"{SH_SCRIPT_PATH} is empty"
    assert lines[0] == "#!/bin/bash", f"{SH_SCRIPT_PATH} does not start with #!/bin/bash"

    content = "\n".join(lines)
    assert "ssh -L 8080:10.1.1.50:80 -N -T jump_web" in content or "ssh -L 8080:10.1.1.50:80 -N -T jump_web" in " ".join(lines), "Missing or incorrect ssh command for jump_web"
    assert "ssh -L 5432:192.168.100.10:5432 -N -f jump_db" in content or "ssh -L 5432:192.168.100.10:5432 -N -f jump_db" in " ".join(lines), "Missing or incorrect ssh command for jump_db"