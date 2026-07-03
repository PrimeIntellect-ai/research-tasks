# test_final_state.py

import os
import subprocess
import tempfile
from urllib.parse import urlparse, parse_qs
import pytest

def is_open_redirect(url):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    for param in ['next', 'redirect_uri', 'url', 'return_to']:
        if param in qs:
            target = qs[param][0]
            t_parsed = urlparse(target)
            if t_parsed.netloc and t_parsed.netloc != parsed.netloc:
                return True
    return False

def get_truth(video_path):
    qr_codes = set()
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.run(['ffmpeg', '-i', video_path, f'{tmpdir}/%04d.png'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        res = subprocess.run(['zbarimg', '-q', '--raw', tmpdir], capture_output=True, text=True)
        for line in res.stdout.splitlines():
            if line.strip():
                qr_codes.add(line.strip())

    expected_keys = set()
    expected_redirects = set()
    for qr in qr_codes:
        if qr.startswith('ENC:'):
            b64 = qr[4:]
            key_hex = b'Sup3rS3cr3tP4ssw0rd!'.hex().ljust(64, '0')
            iv_hex = b'1234567890123456'.hex()
            proc = subprocess.run(
                ['openssl', 'enc', '-d', '-aes-256-cbc', '-a', '-K', key_hex, '-iv', iv_hex],
                input=b64.encode(), capture_output=True
            )
            if proc.returncode == 0:
                expected_keys.add(proc.stdout.decode().strip())
        elif qr.startswith('http'):
            if is_open_redirect(qr):
                expected_redirects.add(qr)

    return expected_keys, expected_redirects

def load_lines(path):
    if not os.path.exists(path): return set()
    with open(path, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def test_analyze_script_f1_score():
    script_path = "/home/user/analyze.sh"
    test_video = "/app/test_session.mp4"

    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

    # Run the student's script on the held-out test video
    proc = subprocess.run([script_path, test_video], capture_output=True, text=True)
    assert proc.returncode == 0, f"Script exited with non-zero status: {proc.stderr}"

    expected_keys, expected_redirects = get_truth(test_video)

    actual_keys = load_lines('/home/user/decrypted_keys.txt')
    actual_redirects = load_lines('/home/user/open_redirects.txt')

    tp_keys = len(expected_keys.intersection(actual_keys))
    fp_keys = len(actual_keys - expected_keys)
    fn_keys = len(expected_keys - actual_keys)

    tp_redirs = len(expected_redirects.intersection(actual_redirects))
    fp_redirs = len(actual_redirects - expected_redirects)
    fn_redirs = len(expected_redirects - actual_redirects)

    tp = tp_keys + tp_redirs
    fp = fp_keys + fp_redirs
    fn = fn_keys + fn_redirs

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    assert f1 >= 0.90, (
        f"F1 Score {f1:.3f} is below the 0.90 threshold. "
        f"TP:{tp} FP:{fp} FN:{fn} "
        f"(Keys: TP={tp_keys}, FP={fp_keys}, FN={fn_keys} | "
        f"Redirects: TP={tp_redirs}, FP={fp_redirs}, FN={fn_redirs})"
    )