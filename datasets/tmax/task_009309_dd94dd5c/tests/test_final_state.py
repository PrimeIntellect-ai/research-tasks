# test_final_state.py
import os
import stat
import subprocess
import time
import signal

def test_files_exist_and_executable():
    assert os.path.exists("/home/user/monitor.c"), "/home/user/monitor.c does not exist"
    assert os.path.exists("/home/user/prepare_migration.sh"), "/home/user/prepare_migration.sh does not exist"

    st = os.stat("/home/user/prepare_migration.sh")
    assert bool(st.st_mode & stat.S_IXUSR), "/home/user/prepare_migration.sh is not executable"

def test_script_execution_and_outputs():
    # Run the script
    result = subprocess.run(["/home/user/prepare_migration.sh"], capture_output=True, text=True)
    assert result.returncode == 0, f"prepare_migration.sh failed with return code {result.returncode}\n{result.stderr}"

    # Check generated files
    assert os.path.exists("/home/user/firewall.sh"), "/home/user/firewall.sh was not created"
    with open("/home/user/firewall.sh", "r") as f:
        firewall_content = f.read().strip()
    assert firewall_content == "iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 443 -j DNAT --to-destination 10.10.10.50:8443", "firewall.sh content is incorrect"

    assert os.path.exists("/home/user/routes.sh"), "/home/user/routes.sh was not created"
    with open("/home/user/routes.sh", "r") as f:
        routes_content = f.read().strip()
    assert routes_content == "ip route add 10.10.10.0/24 via 172.16.0.1 dev eth1", "routes.sh content is incorrect"

    assert os.path.exists("/home/user/fstab.append"), "/home/user/fstab.append was not created"
    with open("/home/user/fstab.append", "r") as f:
        fstab_content = f.read().strip()
    assert fstab_content == "10.10.10.50:/var/nfs /mnt/shared nfs rw,hard,intr 0 0", "fstab.append content is incorrect"

def test_monitor_daemon_behavior():
    assert os.path.exists("/home/user/monitor.pid"), "/home/user/monitor.pid was not created"
    with open("/home/user/monitor.pid", "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), "/home/user/monitor.pid does not contain a valid integer PID"
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Process with PID {pid} is not running"

    # Wait for the log to be written
    time.sleep(1.5)

    assert os.path.exists("/home/user/migration.log"), "/home/user/migration.log was not created"
    with open("/home/user/migration.log", "r") as f:
        log_content = f.read()

    assert "[SERVICE_MIGRATION_ACTIVE]" in log_content, "migration.log does not contain [SERVICE_MIGRATION_ACTIVE]"

    # Send SIGTERM
    os.kill(pid, signal.SIGTERM)

    # Wait for process to terminate and write to log
    time.sleep(1.5)

    # Check if process has terminated
    process_running = True
    try:
        os.kill(pid, 0)
    except OSError:
        process_running = False

    assert not process_running, f"Process with PID {pid} did not terminate after receiving SIGTERM"

    # Check log for stopped message
    with open("/home/user/migration.log", "r") as f:
        lines = f.read().strip().split('\n')

    assert lines[-1] == "[SERVICE_MIGRATION_STOPPED]", "The last line of migration.log is not [SERVICE_MIGRATION_STOPPED]"