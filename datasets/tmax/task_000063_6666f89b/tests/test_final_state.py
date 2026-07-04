# test_final_state.py

import os
import json
import random
import string
import subprocess
import tempfile
import shutil

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_fuzz_directory(base_dir):
    num_files = random.randint(5, 50)
    num_dirs = random.randint(1, 5)
    num_symlinks = random.randint(1, 3)

    # Create subdirectories
    dirs = [base_dir]
    for _ in range(num_dirs):
        d = os.path.join(random.choice(dirs), generate_random_string(8))
        os.makedirs(d, exist_ok=True)
        dirs.append(d)

    # Create files
    extensions = ['.tmp', '.log', '.txt', '.bin', '.dat']
    for _ in range(num_files):
        d = random.choice(dirs)
        ext = random.choice(extensions)
        fpath = os.path.join(d, generate_random_string(8) + ext)
        size = random.randint(0, 10240)
        with open(fpath, 'wb') as f:
            f.write(os.urandom(size))
        # Randomize mtime
        mtime = random.randint(1000000000, 2000000000)
        os.utime(fpath, (mtime, mtime))

    # Create circular symlinks
    for _ in range(num_symlinks):
        d = random.choice(dirs)
        link_name = os.path.join(d, generate_random_string(8))
        target = random.choice(dirs)
        # Create a relative or absolute symlink to a directory to create a loop
        if not os.path.exists(link_name):
            os.symlink(target, link_name)

    # Create backup_config.json in base_dir
    config_path = os.path.join(base_dir, 'backup_config.json')
    exclude_extensions = random.sample(extensions, k=random.randint(1, 3))
    min_mtime = random.randint(1000000000, 2000000000)

    with open(config_path, 'w') as f:
        json.dump({
            "exclude_extensions": exclude_extensions,
            "min_mtime": min_mtime
        }, f)

def test_fuzz_equivalence():
    random.seed(42)
    oracle_path = '/opt/oracle/reference_archiver'
    agent_script = '/home/user/archiver.py'

    assert os.path.isfile(agent_script), f"Agent script {agent_script} not found."
    assert os.path.isfile(oracle_path), f"Oracle binary {oracle_path} not found."

    for i in range(50):
        with tempfile.TemporaryDirectory() as fuzz_dir:
            create_fuzz_directory(fuzz_dir)

            oracle_output = os.path.join(fuzz_dir, 'oracle_output.bin')
            agent_output = os.path.join(fuzz_dir, 'agent_output.bin')

            # Run oracle
            oracle_proc = subprocess.run([oracle_path, fuzz_dir, oracle_output], capture_output=True)
            assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}:\n{oracle_proc.stderr.decode()}"

            # Run agent
            agent_proc = subprocess.run(['python3', agent_script, fuzz_dir, agent_output], capture_output=True)
            assert agent_proc.returncode == 0, f"Agent failed on iteration {i}:\n{agent_proc.stderr.decode()}"

            # Compare outputs
            assert os.path.isfile(oracle_output), "Oracle output not generated."
            assert os.path.isfile(agent_output), "Agent output not generated."

            with open(oracle_output, 'rb') as f_oracle, open(agent_output, 'rb') as f_agent:
                oracle_data = f_oracle.read()
                agent_data = f_agent.read()

            if oracle_data != agent_data:
                assert False, f"Output mismatch on iteration {i}. Oracle size: {len(oracle_data)}, Agent size: {len(agent_data)}"

def test_dirsync_patched():
    import sys
    sys.path.insert(0, '/app/dirsync-2.2.5')
    try:
        import dirsync
    except ImportError:
        assert False, "Could not import dirsync from /app/dirsync-2.2.5"

    with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dst:
        # Create self-referential symlink
        link_path = os.path.join(src, 'loop')
        os.symlink(src, link_path)

        # Add a file to ensure it syncs something
        with open(os.path.join(src, 'test.txt'), 'w') as f:
            f.write("test")

        try:
            dirsync.sync(src, dst, action='update', create=True)
        except RecursionError:
            assert False, "dirsync raised RecursionError, symlink loop detection is not patched."
        except Exception as e:
            assert False, f"dirsync raised unexpected exception: {e}"

        assert os.path.exists(os.path.join(dst, 'test.txt')), "dirsync failed to copy files."