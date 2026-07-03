# test_final_state.py

import os
import subprocess
import random
import tempfile
import pytest

ORACLE = "/app/legacy_extractor"
AGENT = "/home/user/extractor"
N = 100

def test_agent_executable_exists():
    assert os.path.exists(AGENT), f"Agent script {AGENT} does not exist"
    assert os.access(AGENT, os.X_OK), f"Agent script {AGENT} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE), f"Oracle {ORACLE} does not exist"
    assert os.access(ORACLE, os.X_OK), f"Oracle {ORACLE} is not executable"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(N):
            has_meta = random.random() < 0.8
            elf_path = os.path.join(tmpdir, f"test_{i}.elf")

            # Create a basic C file to compile into an ELF
            c_path = os.path.join(tmpdir, f"test_{i}.c")
            with open(c_path, "w") as f:
                f.write("int main() { return 0; }\n")

            # Compile to a 64-bit ELF
            subprocess.run(["gcc", c_path, "-o", elf_path], check=True, capture_output=True)

            if has_meta:
                # Generate a random string with ASCII, Latin-1, and Emoji
                length = random.randint(0, 1024)
                chars = []
                for _ in range(length):
                    c = random.choice([
                        random.randint(0x0020, 0x007E),   # ASCII
                        random.randint(0x00A0, 0x00FF),   # Latin-1
                        random.randint(0x1F300, 0x1F64F)  # Emoji
                    ])
                    chars.append(chr(c))
                text = "".join(chars)
                utf16_bytes = text.encode("utf-16le")

                # XOR encrypt with 0x5A
                xored = bytes([b ^ 0x5A for b in utf16_bytes])

                meta_path = os.path.join(tmpdir, f"test_{i}.meta")
                with open(meta_path, "wb") as f:
                    f.write(xored)

                # Inject the section into the ELF
                subprocess.run(["objcopy", "--add-section", f".pkg_meta={meta_path}", elf_path], check=True, capture_output=True)

            # Run oracle
            oracle_res = subprocess.run([ORACLE, elf_path], capture_output=True)

            # Run agent
            agent_res = subprocess.run([AGENT, elf_path], capture_output=True)

            # Assert exact equivalence
            assert agent_res.returncode == oracle_res.returncode, (
                f"Exit code mismatch on fuzz round {i} (has_meta={has_meta}).\n"
                f"Oracle exit code: {oracle_res.returncode}\n"
                f"Agent exit code: {agent_res.returncode}"
            )
            assert agent_res.stdout == oracle_res.stdout, (
                f"Stdout mismatch on fuzz round {i} (has_meta={has_meta}).\n"
                f"Oracle stdout: {oracle_res.stdout!r}\n"
                f"Agent stdout: {agent_res.stdout!r}"
            )
            assert agent_res.stderr == oracle_res.stderr, (
                f"Stderr mismatch on fuzz round {i} (has_meta={has_meta}).\n"
                f"Oracle stderr: {oracle_res.stderr!r}\n"
                f"Agent stderr: {agent_res.stderr!r}"
            )