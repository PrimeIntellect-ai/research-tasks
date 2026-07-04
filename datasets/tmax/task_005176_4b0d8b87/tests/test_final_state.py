# test_final_state.py
import os
import subprocess
import configparser
import glob

def test_filter_script_exists_and_executable():
    script_path = '/home/user/filter.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_config_ini_updated():
    config_path = '/home/user/app/config.ini'
    assert os.path.isfile(config_path), f"Config file {config_path} does not exist."

    config = configparser.ConfigParser()
    config.read(config_path)

    assert 'DEFAULT' in config, "DEFAULT section missing in config.ini"
    assert config['DEFAULT'].get('PRE_FILTER_CMD') == '/home/user/filter.sh', "PRE_FILTER_CMD is not updated to /home/user/filter.sh"

def test_adversarial_corpus():
    script_path = '/home/user/filter.sh'
    clean_dir = '/home/user/corpora/clean/'
    evil_dir = '/home/user/corpora/evil/'

    # We look for files in the directories, assuming they are files.
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "No clean files found in corpus."
    assert len(evil_files) > 0, "No evil files found in corpus."

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run([script_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        result = subprocess.run([script_path, ef], capture_output=True)
        if result.returncode == 0:
            evil_failed.append(os.path.basename(ef))

    error_msgs = []
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed[:10])}")
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed[:10])}")

    assert not clean_failed and not evil_failed, " | ".join(error_msgs)