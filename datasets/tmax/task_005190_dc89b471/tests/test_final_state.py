# test_final_state.py

import os
import subprocess
import random
import string
import tempfile
import pytest

def test_makefile_fixed():
    makefile_path = "/app/vendored-tracker-1.2/Makefile"
    assert os.path.isfile(makefile_path), f"File {makefile_path} does not exist."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "sed -i ''" not in content, "Makefile still contains the macOS-style sed command."

def test_make_setup_run():
    test_elfs_path = "/home/user/test_elfs"
    assert os.path.isdir(test_elfs_path), "Directory /home/user/test_elfs does not exist. Did you run make setup?"
    elfs = [f for f in os.listdir(test_elfs_path) if os.path.isfile(os.path.join(test_elfs_path, f))]
    assert len(elfs) > 0, "No ELF files found in /home/user/test_elfs."

def oracle(elf_path):
    result = subprocess.run(["readelf", "-W", "-S", elf_path], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    output = []
    for line in lines:
        parts = line.split()
        # Handle readelf -W -S output format
        if len(parts) >= 6 and parts[1].startswith(".cfg_"):
            name = parts[1]
            offset = parts[4]
            size = parts[5]
            size_dec = int(size, 16)
            # Ensure hex is lowercase and prefixed with 0x, with no extra leading zeros after 0x
            offset_hex = hex(int(offset, 16))
            output.append(f"WAL_RECORD: name={name} size={size_dec} offset={offset_hex}")
    return "\n".join(output)

def create_random_elf(path):
    # Create a dummy C file and compile it to an ELF
    c_file = path + ".c"
    with open(c_file, "w") as f:
        f.write("int main() { return 0; }\n")
    subprocess.run(["gcc", c_file, "-o", path], check=True)

    # Add random .cfg_ sections
    num_sections = random.randint(0, 10)
    for _ in range(num_sections):
        sec_name = ".cfg_" + "".join(random.choices(string.ascii_letters + string.digits + "_", k=8))
        sec_size = random.randint(1, 65536)
        sec_data = os.urandom(sec_size)
        sec_file = path + ".sec"
        with open(sec_file, "wb") as f:
            f.write(sec_data)
        subprocess.run(["objcopy", "--add-section", f"{sec_name}={sec_file}", path], check=True)
        os.remove(sec_file)
    os.remove(c_file)

def test_fuzz_equivalence():
    agent_script = "/home/user/elf_to_wal.sh"
    assert os.path.isfile(agent_script), f"Agent script {agent_script} does not exist."

    random.seed(42)
    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(25):
            elf_path = os.path.join(tmpdir, f"test_{i}.elf")
            create_random_elf(elf_path)

            oracle_out = oracle(elf_path).strip()

            agent_res = subprocess.run(["/bin/bash", agent_script, elf_path], capture_output=True, text=True)
            agent_out = agent_res.stdout.strip()

            assert agent_res.returncode == 0, f"Agent script failed on input with {elf_path}. Stderr: {agent_res.stderr}"
            assert agent_out == oracle_out, f"Mismatch on {elf_path}.\nOracle Output:\n{oracle_out}\n\nAgent Output:\n{agent_out}"