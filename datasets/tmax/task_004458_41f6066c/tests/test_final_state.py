# test_final_state.py
import os
import re
import subprocess
import pytest

def get_section_data(elf_path, section_name):
    """Extracts the raw binary data of a specific ELF section using objcopy."""
    out_path = f"/tmp/extracted_{os.path.basename(elf_path)}.bin"
    result = subprocess.run(
        ["objcopy", "-O", "binary", f"--only-section={section_name}", elf_path, out_path],
        capture_output=True
    )
    if result.returncode != 0 or not os.path.exists(out_path):
        return None

    with open(out_path, "rb") as f:
        data = f.read()

    if os.path.exists(out_path):
        os.remove(out_path)

    return data

def test_sanitized_elf_exists():
    assert os.path.isfile("/home/user/sanitized.elf"), "The sanitized ELF binary /home/user/sanitized.elf is missing."

def test_redaction_f1_score():
    orig_elf = "/app/malware.elf"
    sanitized_elf = "/home/user/sanitized.elf"

    assert os.path.isfile(orig_elf), f"Original ELF {orig_elf} is missing."
    assert os.path.isfile(sanitized_elf), f"Sanitized ELF {sanitized_elf} is missing."

    orig_data = get_section_data(orig_elf, ".exfil_data")
    sanitized_data = get_section_data(sanitized_elf, ".exfil_data")

    assert orig_data is not None, "Failed to extract .exfil_data from original ELF."
    assert sanitized_data is not None, "Failed to extract .exfil_data from sanitized ELF."
    assert len(orig_data) == len(sanitized_data), "The length of the .exfil_data section was altered."

    # Ground truth masks
    is_sensitive = [False] * len(orig_data)

    # Regex patterns for sensitive data
    cc_pattern = re.compile(br'(?<!\d)\d{4}-\d{4}-\d{4}-\d{4}(?!\d)')
    email_pattern = re.compile(br'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    for match in cc_pattern.finditer(orig_data):
        for i in range(match.start(), match.end()):
            is_sensitive[i] = True

    for match in email_pattern.finditer(orig_data):
        for i in range(match.start(), match.end()):
            is_sensitive[i] = True

    tp = 0
    fp = 0
    fn = 0

    for i in range(len(orig_data)):
        orig_byte = orig_data[i]
        sanitized_byte = sanitized_data[i]

        was_redacted = (sanitized_byte == ord('*')) and (orig_byte != ord('*'))

        if is_sensitive[i]:
            if was_redacted:
                tp += 1
            else:
                fn += 1
        else:
            if was_redacted:
                fp += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    threshold = 0.95
    assert f1 >= threshold, f"F1 score for redaction is {f1:.4f}, which is below the threshold of {threshold}. TP={tp}, FP={fp}, FN={fn}."