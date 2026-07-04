# test_final_state.py
import os
import subprocess
import random
import tempfile
import shutil

def test_parse_elf_equivalence():
    agent_script = "/home/user/parse_elf.sh"
    oracle_script = "/test/oracle_parse_elf.sh"

    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"
    assert os.access(agent_script, os.X_OK), f"Agent script {agent_script} is not executable"
    assert os.path.isfile(oracle_script), f"Oracle script not found at {oracle_script}"

    random.seed(42)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a dummy C file
        c_file = os.path.join(tmpdir, "dummy.c")
        with open(c_file, "w") as f:
            f.write("int main() { return 0; }\n")

        # Compile base valid ELF
        valid_elf = os.path.join(tmpdir, "valid.elf")
        subprocess.run(["gcc", c_file, "-o", valid_elf], check=True)

        # Compile REL object
        rel_elf = os.path.join(tmpdir, "rel.o")
        subprocess.run(["gcc", "-c", c_file, "-o", rel_elf], check=True)

        # Create ELF without .rodata
        no_rodata_elf = os.path.join(tmpdir, "no_rodata.elf")
        subprocess.run(["objcopy", "--remove-section", ".rodata", valid_elf, no_rodata_elf], check=True)

        test_files = []

        for i in range(100):
            test_file = os.path.join(tmpdir, f"test_{i}")
            category = i % 5

            if category == 0:
                # Random text/garbage
                with open(test_file, "wb") as f:
                    f.write(bytes(random.getrandbits(8) for _ in range(100)))
            elif category == 1:
                # Valid x86-64 ELF
                shutil.copy(valid_elf, test_file)
            elif category == 2:
                # x86-64 without .rodata
                shutil.copy(no_rodata_elf, test_file)
            elif category == 3:
                # ARM64 ELF (faked by modifying e_machine in ELF header)
                with open(valid_elf, "rb") as f:
                    data = bytearray(f.read())
                # e_machine is at offset 0x12 in 64-bit ELF
                data[0x12] = 0xB7
                data[0x13] = 0x00
                with open(test_file, "wb") as f:
                    f.write(data)
            elif category == 4:
                # REL object
                shutil.copy(rel_elf, test_file)

            test_files.append(test_file)

        for test_file in test_files:
            oracle_proc = subprocess.run(
                ["bash", oracle_script, test_file],
                capture_output=True, text=True
            )
            agent_proc = subprocess.run(
                ["bash", agent_script, test_file],
                capture_output=True, text=True
            )

            oracle_out = oracle_proc.stdout.strip()
            agent_out = agent_proc.stdout.strip()

            assert agent_out == oracle_out, (
                f"Mismatch on file {test_file}.\n"
                f"Expected (Oracle): {oracle_out}\n"
                f"Got (Agent): {agent_out}"
            )