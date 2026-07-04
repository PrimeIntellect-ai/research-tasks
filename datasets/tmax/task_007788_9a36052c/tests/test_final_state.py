# test_final_state.py

import os
import stat

def test_c_program_modified():
    c_file = "/home/user/src/net_monitor.c"
    assert os.path.isfile(c_file), f"{c_file} is missing"
    with open(c_file, "r") as f:
        content = f.read()
    assert 'getenv("LOG_DIR")' in content, "net_monitor.c does not use getenv(\"LOG_DIR\")"
    assert '/tmp/net_stats.log' in content, "net_monitor.c does not contain the default fallback path /tmp/net_stats.log"

def test_directories_exist():
    for d in ["/home/user/logs", "/home/user/bin"]:
        assert os.path.isdir(d), f"Directory {d} does not exist"

def test_bare_git_repo():
    repo_dir = "/home/user/git/capacity.git"
    assert os.path.isdir(repo_dir), f"Bare repository directory {repo_dir} does not exist"
    assert os.path.isfile(os.path.join(repo_dir, "HEAD")), "Git HEAD file missing, not a valid bare repo"
    config_file = os.path.join(repo_dir, "config")
    assert os.path.isfile(config_file), "Git config file missing"
    with open(config_file, "r") as f:
        content = f.read()
    assert "bare = true" in content, "Repository is not configured as bare"

def test_git_hook():
    hook_file = "/home/user/git/capacity.git/hooks/post-receive"
    assert os.path.isfile(hook_file), f"Hook file {hook_file} is missing"

    st = os.stat(hook_file)
    assert bool(st.st_mode & stat.S_IXUSR), f"Hook file {hook_file} is not executable"

    with open(hook_file, "r") as f:
        content = f.read()
    assert "LOG_DIR=/home/user/logs" in content, "Hook does not export LOG_DIR correctly"
    assert "/home/user/bin/net_monitor" in content, "Hook does not execute the compiled binary"
    assert "gcc" in content or "cc" in content or "make" in content, "Hook does not seem to compile the C program"

def test_expect_script():
    script_file = "/home/user/simulate_push.exp"
    assert os.path.isfile(script_file), f"Expect script {script_file} is missing"
    st = os.stat(script_file)
    assert bool(st.st_mode & stat.S_IXUSR), f"Expect script {script_file} is not executable"

    with open(script_file, "r") as f:
        content = f.read()
    assert "git clone" in content, "Expect script missing git clone command"
    assert "trigger.txt" in content, "Expect script does not create trigger.txt"
    assert "git push" in content, "Expect script missing git push command"

def test_logrotate_config():
    conf_file = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_file), f"Logrotate config {conf_file} is missing"
    with open(conf_file, "r") as f:
        content = f.read()

    assert "/home/user/logs/net_stats.log" in content, "Logrotate config does not target the correct log file"
    assert "daily" in content, "Logrotate config missing 'daily'"
    assert "rotate 5" in content, "Logrotate config missing 'rotate 5'"
    assert "compress" in content, "Logrotate config missing 'compress'"
    assert "missingok" in content, "Logrotate config missing 'missingok'"

def test_log_file_generated():
    log_file = "/home/user/logs/net_stats.log"
    assert os.path.isfile(log_file), f"Log file {log_file} was not generated. Did the Expect script run successfully?"
    with open(log_file, "r") as f:
        content = f.read()
    assert "Network stats recorded at" in content, "Log file does not contain the expected output string"