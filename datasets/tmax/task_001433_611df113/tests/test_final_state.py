# test_final_state.py

import os
import sys
import string
import hashlib
import stat
import pytest

def calculate_wer(reference, hypothesis):
    ref_words = reference.split()
    hyp_words = hypothesis.split()

    d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]

    for i in range(len(ref_words) + 1):
        d[i][0] = i
    for j in range(len(hyp_words) + 1):
        d[0][j] = j

    for i in range(1, len(ref_words) + 1):
        for j in range(1, len(hyp_words) + 1):
            if ref_words[i - 1] == hyp_words[j - 1]:
                cost = 0
            else:
                cost = 1
            d[i][j] = min(d[i - 1][j] + 1,      # deletion
                          d[i][j - 1] + 1,      # insertion
                          d[i - 1][j - 1] + cost) # substitution

    if len(ref_words) == 0:
        return float('inf')
    return d[len(ref_words)][len(hyp_words)] / float(len(ref_words))

def test_transcript_wer():
    """Check that the transcript exists and meets the Word Error Rate threshold."""
    transcript_path = "/home/user/transcript.txt"
    assert os.path.exists(transcript_path), f"Transcript file not found at {transcript_path}."

    with open(transcript_path, "r") as f:
        hypothesis = f.read().strip().lower()

    # Remove basic punctuation just in case
    hypothesis = hypothesis.translate(str.maketrans('', '', string.punctuation))

    reference = "the payload was delivered via open redirect on our login page the target domain was secure dash update dot net and the exfiltration ip is one nine two dot one six eight dot one five dot seven"

    wer = calculate_wer(reference, hypothesis)
    threshold = 0.20

    assert wer <= threshold, f"Transcript WER is {wer:.4f}, which is above the threshold of {threshold}. Hypothesis text: '{hypothesis}'"

def test_firewall_rule():
    """Check that the firewall rule matches the exact expected string with the extracted IP."""
    rule_path = "/home/user/firewall_rule.txt"
    assert os.path.exists(rule_path), f"Firewall rule file not found at {rule_path}."

    with open(rule_path, "r") as f:
        content = f.read().strip()

    # Normalize spaces for robust comparison
    normalized_content = " ".join(content.split())
    expected_rule = "iptables -A OUTPUT -d 192.168.15.7 -j DROP"

    assert normalized_content == expected_rule, f"Expected firewall rule '{expected_rule}', but got '{normalized_content}'."

def test_csp_rule():
    """Check that the CSP header matches the exact expected string."""
    csp_path = "/home/user/csp.txt"
    assert os.path.exists(csp_path), f"CSP file not found at {csp_path}."

    with open(csp_path, "r") as f:
        content = f.read().strip()

    expected_csp = "Content-Security-Policy: default-src 'self'; form-action 'self';"
    assert content == expected_csp, f"Expected CSP '{expected_csp}', but got '{content}'."

def test_transcript_hash():
    """Check that the transcript hash matches the actual SHA-256 of the transcript file."""
    transcript_path = "/home/user/transcript.txt"
    hash_path = "/home/user/transcript_hash.txt"

    assert os.path.exists(transcript_path), f"Transcript file not found at {transcript_path}."
    assert os.path.exists(hash_path), f"Hash file not found at {hash_path}."

    with open(transcript_path, 'rb') as f:
        expected_hash = hashlib.sha256(f.read()).hexdigest()

    with open(hash_path, 'r') as f:
        content = f.read().strip()

    assert expected_hash in content, f"Expected hash '{expected_hash}' not found in {hash_path}. Content was: '{content}'"

def test_file_permissions():
    """Check that all generated files have strict 600 permissions."""
    files = [
        '/home/user/transcript.txt',
        '/home/user/firewall_rule.txt',
        '/home/user/csp.txt',
        '/home/user/transcript_hash.txt'
    ]

    for f_path in files:
        assert os.path.exists(f_path), f"File {f_path} does not exist, cannot check permissions."
        st = os.stat(f_path)
        perms = stat.S_IMODE(st.st_mode)
        assert perms == 0o600, f"File {f_path} has permissions {oct(perms)}, expected 0o600."