# test_final_state.py

import os
import subprocess
import configparser

def test_symlink_created():
    """Verify that the symlink settings.ini points to smtp_production.ini."""
    link_path = '/home/user/sysapp/mail/settings.ini'
    target_path = '/home/user/sysconfig/smtp_production.ini'

    assert os.path.islink(link_path), f"{link_path} is not a symbolic link."
    assert os.readlink(link_path) == target_path, f"Symlink {link_path} does not point to {target_path}."

def test_config_updated():
    """Verify that smtp_production.ini has the updated bind_address and port."""
    config_path = '/home/user/sysconfig/smtp_production.ini'
    assert os.path.isfile(config_path), f"Configuration file {config_path} is missing."

    config = configparser.ConfigParser()
    config.read(config_path)

    assert 'smtp' in config, "Section [smtp] is missing in smtp_production.ini."
    assert config['smtp'].get('bind_address') == '127.0.0.1', "bind_address in smtp_production.ini is not 127.0.0.1."
    assert config['smtp'].get('port') == '2525', "port in smtp_production.ini is not 2525."

def test_bashrc_updated():
    """Verify that .bashrc contains the required environment variable exports."""
    bashrc_path = '/home/user/.bashrc'
    assert os.path.isfile(bashrc_path), f"{bashrc_path} is missing."

    with open(bashrc_path, 'r') as f:
        content = f.read()

    assert 'MAIL_SERVER_HOST=127.0.0.1' in content, "MAIL_SERVER_HOST=127.0.0.1 not found in .bashrc."
    assert 'MAIL_SERVER_PORT=2525' in content, "MAIL_SERVER_PORT=2525 not found in .bashrc."

def test_verify_script_functionality():
    """Verify that verify.py writes the correct log based on environment variables."""
    script_path = '/home/user/sysapp/mail/verify.py'
    log_path = '/home/user/sysapp/mail/validation.log'

    assert os.path.isfile(script_path), f"Python script {script_path} is missing."

    # Clean up log file if it exists
    if os.path.exists(log_path):
        os.remove(log_path)

    # Test matching case
    env_match = os.environ.copy()
    env_match['MAIL_SERVER_HOST'] = '127.0.0.1'
    env_match['MAIL_SERVER_PORT'] = '2525'

    result = subprocess.run(['python3', script_path], env=env_match, capture_output=True)
    assert result.returncode == 0, f"Script execution failed: {result.stderr.decode()}"

    assert os.path.isfile(log_path), f"Log file {log_path} was not created."
    with open(log_path, 'r') as f:
        log_content = f.read().strip()
    assert log_content == 'MATCH: 127.0.0.1:2525', f"Expected 'MATCH: 127.0.0.1:2525', got '{log_content}'"

    # Clean up log file
    os.remove(log_path)

    # Test error case
    env_error = os.environ.copy()
    env_error['MAIL_SERVER_HOST'] = '10.0.0.1'
    env_error['MAIL_SERVER_PORT'] = '2525'

    subprocess.run(['python3', script_path], env=env_error, capture_output=True)

    assert os.path.isfile(log_path), f"Log file {log_path} was not created on error case."
    with open(log_path, 'r') as f:
        log_content = f.read().strip()
    assert log_content == 'ERROR', f"Expected 'ERROR', got '{log_content}'"