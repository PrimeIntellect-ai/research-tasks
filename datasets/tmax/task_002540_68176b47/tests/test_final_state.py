# test_final_state.py

import os
import time
import tarfile
import subprocess
import tempfile
import shutil

def test_restored_configs_archive():
    archive_path = "/home/user/restored_configs.tar.gz"
    assert os.path.exists(archive_path), f"{archive_path} does not exist"

    # Extract and check contents
    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        # Check if files are patched
        rogue_string = b"[ROGUE_OVERRIDE_ENABLED=TRUE]"
        secure_string = b"[SECURE_DEFAULT_LOCKED]"

        found_conf = False
        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                if file.endswith(".conf"):
                    found_conf = True
                    file_path = os.path.join(root, file)
                    with open(file_path, "rb") as f:
                        content = f.read()
                        assert rogue_string not in content, f"Rogue string found in {file}"
                        # Only check for secure_string if it was one of the target files
                        # The target files are 142, 455, 891, 1024, 1560
                        if file in ["config_batch_142.conf", "config_batch_455.conf", 
                                    "config_batch_891.conf", "config_batch_1024.conf", 
                                    "config_batch_1560.conf"]:
                            assert secure_string in content, f"Secure string not found in patched file {file}"

        assert found_conf, "No .conf files found in the restored archive"

def test_fast_patch_speedup():
    patcher_script = "/home/user/fast_patch.py"
    assert os.path.exists(patcher_script), f"{patcher_script} does not exist"

    # Create a benchmark file (~500MB)
    with tempfile.TemporaryDirectory() as tmpdir:
        # We will create two identical directories with one large file each
        naive_dir = os.path.join(tmpdir, "naive")
        agent_dir = os.path.join(tmpdir, "agent")
        os.makedirs(naive_dir)
        os.makedirs(agent_dir)

        naive_file = os.path.join(naive_dir, "large_config.conf")
        agent_file = os.path.join(agent_dir, "large_config.conf")

        chunk = b"Some filler config data line 1\nSome filler config data line 2\n[ROGUE_OVERRIDE_ENABLED=TRUE]\n" * 1000
        # 1000 reps = ~100KB. 5000 reps = ~500MB

        with open(naive_file, "wb") as f:
            for _ in range(5000):
                f.write(chunk)

        shutil.copy2(naive_file, agent_file)

        # Naive implementation
        start_time = time.time()
        with open(naive_file, "rb") as f:
            content = f.read()
        content = content.replace(b"[ROGUE_OVERRIDE_ENABLED=TRUE]", b"[SECURE_DEFAULT_LOCKED]")
        with open(naive_file, "wb") as f:
            f.write(content)
        t_ref = time.time() - start_time

        # Agent implementation
        start_time = time.time()
        subprocess.run(["python3", patcher_script, agent_dir], check=True)
        t_agent = time.time() - start_time

        # Verify agent actually replaced it
        with open(agent_file, "rb") as f:
            # Check just a chunk to avoid memory issues
            agent_content = f.read(1024 * 1024)
            assert b"[ROGUE_OVERRIDE_ENABLED=TRUE]" not in agent_content, "Agent script did not replace the string correctly"
            assert b"[SECURE_DEFAULT_LOCKED]" in agent_content, "Agent script did not insert the secure string"

        speedup = t_ref / max(t_agent, 0.0001)
        assert speedup >= 2.5, f"Patcher speedup was {speedup:.2f}x, which is below the 2.5x threshold. T_ref={t_ref:.2f}s, T_agent={t_agent:.2f}s"