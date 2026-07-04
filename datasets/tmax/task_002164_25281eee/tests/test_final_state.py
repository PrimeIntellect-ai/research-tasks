# test_final_state.py

import os
import random
import subprocess
import tempfile
import pytest

def test_libcsv_installed():
    assert os.path.isfile("/home/user/local/include/csv.h"), "libcsv header not installed in /home/user/local/include/"
    has_so = os.path.isfile("/home/user/local/lib/libcsv.so")
    has_a = os.path.isfile("/home/user/local/lib/libcsv.a")
    assert has_so or has_a, "libcsv library not installed in /home/user/local/lib/"

def test_imputer_exists():
    assert os.path.isfile("/home/user/imputer.c"), "/home/user/imputer.c is missing"
    assert os.path.isfile("/home/user/imputer"), "/home/user/imputer binary is missing"
    assert os.access("/home/user/imputer", os.X_OK), "/home/user/imputer is not executable"

def test_pipeline_script():
    assert os.path.isfile("/home/user/pipeline.sh"), "/home/user/pipeline.sh is missing"
    assert os.access("/home/user/pipeline.sh", os.X_OK), "/home/user/pipeline.sh is not executable"

def test_pipeline_cron():
    assert os.path.isfile("/home/user/pipeline.cron"), "/home/user/pipeline.cron is missing"
    with open("/home/user/pipeline.cron", "r") as f:
        content = f.read().strip()
    assert "*/5" in content or "0,5" in content or "5" in content, "Cron schedule must be every 5 minutes"
    assert "/home/user/pipeline.sh" in content, "Cron must execute /home/user/pipeline.sh"

def generate_csv(filename, num_lines, missing_prob, block_prob, block_size_max):
    with open(filename, "w") as f:
        ts = 1600000000
        val = random.uniform(-100.0, 100.0)
        in_block = False
        block_rem = 0

        for i in range(num_lines):
            ts += random.randint(1, 10)
            val += random.uniform(-1.0, 1.0)

            is_missing = False
            if in_block:
                is_missing = True
                block_rem -= 1
                if block_rem <= 0:
                    in_block = False
            else:
                if random.random() < block_prob:
                    in_block = True
                    block_rem = random.randint(1, block_size_max)
                    is_missing = True
                elif random.random() < missing_prob:
                    is_missing = True

            if is_missing:
                missing_str = "" if random.random() < 0.5 else "NaN"
                f.write(f"{ts},{missing_str}\n")
            else:
                f.write(f"{ts},{val:.6f}\n")

def test_fuzz_equivalence():
    oracle = "/app/oracle_imputer"
    agent = "/home/user/imputer"

    assert os.path.isfile(oracle), f"Oracle program {oracle} is missing"
    assert os.path.isfile(agent), f"Agent program {agent} is missing"

    random.seed(42)
    N = 100  # Running 100 iterations for performance while maintaining robust coverage

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(N):
            csv_path = os.path.join(tmpdir, f"test_{i}.csv")
            num_lines = random.randint(10, 5000)
            missing_prob = random.uniform(0.05, 0.40)
            block_prob = random.uniform(0.0, 0.05)

            # Edge cases: occasionally force very small files
            if random.random() < 0.05:
                num_lines = random.randint(1, 5)

            generate_csv(csv_path, num_lines, missing_prob, block_prob, min(1000, num_lines))

            # Occasionally force missing values at the very start or end
            if random.random() < 0.1:
                with open(csv_path, "r") as f:
                    lines = f.readlines()
                if lines:
                    parts = lines[0].split(",")
                    lines[0] = f"{parts[0]},\n"
                with open(csv_path, "w") as f:
                    f.writelines(lines)

            proc_oracle = subprocess.run([oracle, csv_path], capture_output=True, text=True)
            proc_agent = subprocess.run([agent, csv_path], capture_output=True, text=True)

            assert proc_agent.returncode == 0, f"Agent failed (exit code {proc_agent.returncode}) on {csv_path}\nStderr: {proc_agent.stderr}"

            if proc_oracle.stdout != proc_agent.stdout:
                oracle_lines = proc_oracle.stdout.splitlines()
                agent_lines = proc_agent.stdout.splitlines()
                mismatch_idx = -1
                for j, (o, a) in enumerate(zip(oracle_lines, agent_lines)):
                    if o != a:
                        mismatch_idx = j
                        break
                if mismatch_idx == -1 and len(oracle_lines) != len(agent_lines):
                    mismatch_idx = min(len(oracle_lines), len(agent_lines))

                oracle_val = oracle_lines[mismatch_idx] if mismatch_idx < len(oracle_lines) else 'EOF'
                agent_val = agent_lines[mismatch_idx] if mismatch_idx < len(agent_lines) else 'EOF'

                pytest.fail(f"Mismatch on dynamically generated input {csv_path} at line {mismatch_idx + 1}.\n"
                            f"Oracle output: {oracle_val}\n"
                            f"Agent output:  {agent_val}")