# test_final_state.py

import os
import glob
import subprocess
import tempfile
import shutil

def test_audio_transcription():
    secret_path = "/home/user/audio_secret.txt"
    assert os.path.isfile(secret_path), f"Transcription file {secret_path} is missing."

    with open(secret_path, "r") as f:
        content = f.read().strip()

    expected_text = "storage capacity reached"
    assert content == expected_text, f"Expected transcription '{expected_text}', got '{content}'"

def test_audio_sanitizer_validate():
    executable = "/home/user/audio_sanitizer"
    assert os.path.isfile(executable), f"Executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"Executable {executable} is not executable."

    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    evil_files = glob.glob(os.path.join(evil_dir, "*.tar"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.tar"))

    assert len(evil_files) > 0, f"No evil corpus files found in {evil_dir}."
    assert len(clean_files) > 0, f"No clean corpus files found in {clean_dir}."

    bypassed_evil = []
    for evil in evil_files:
        result = subprocess.run([executable, "validate", evil], capture_output=True)
        if result.returncode == 0:
            bypassed_evil.append(os.path.basename(evil))

    rejected_clean = []
    for clean in clean_files:
        result = subprocess.run([executable, "validate", clean], capture_output=True)
        if result.returncode != 0:
            rejected_clean.append(os.path.basename(clean))

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if rejected_clean:
        error_msgs.append(f"{len(rejected_clean)} of {len(clean_files)} clean modified: {', '.join(rejected_clean)}")

    assert not error_msgs, "; ".join(error_msgs)

def test_audio_sanitizer_optimize():
    executable = "/home/user/audio_sanitizer"
    assert os.path.isfile(executable), f"Executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"Executable {executable} is not executable."

    with tempfile.TemporaryDirectory() as tmpdir:
        input_dir = os.path.join(tmpdir, "input")
        output_dir = os.path.join(tmpdir, "output")
        os.mkdir(input_dir)
        os.mkdir(output_dir)

        # Create test chunks with various zero-byte patterns
        c1_path = os.path.join(input_dir, "chunk1.chunk")
        with open(c1_path, "wb") as f:
            f.write(b"\x01\x02\x03")

        c2_path = os.path.join(input_dir, "chunk2.chunk")
        with open(c2_path, "wb") as f:
            f.write(b"\x01\x00\x02")

        c3_path = os.path.join(input_dir, "chunk3.chunk")
        with open(c3_path, "wb") as f:
            f.write(b"\x00" * 255)

        c4_path = os.path.join(input_dir, "chunk4.chunk")
        with open(c4_path, "wb") as f:
            f.write(b"\x00" * 256)

        c5_path = os.path.join(input_dir, "chunk5.chunk")
        with open(c5_path, "wb") as f:
            f.write(b"\x00" * 256)

        result = subprocess.run([executable, "optimize", input_dir, output_dir], capture_output=True)
        assert result.returncode == 0, f"Optimize command failed with code {result.returncode}. Stderr: {result.stderr.decode()}"

        out1 = os.path.join(output_dir, "chunk1.chunk")
        out2 = os.path.join(output_dir, "chunk2.chunk")
        out3 = os.path.join(output_dir, "chunk3.chunk")
        out4 = os.path.join(output_dir, "chunk4.chunk")
        out5 = os.path.join(output_dir, "chunk5.chunk")

        assert os.path.exists(out1), "chunk1.chunk missing in output directory"
        with open(out1, "rb") as f:
            assert f.read() == b"\x01\x02\x03", "chunk1.chunk was not encoded correctly"

        assert os.path.exists(out2), "chunk2.chunk missing in output directory"
        with open(out2, "rb") as f:
            assert f.read() == b"\x01\x00\x01\x02", "chunk2.chunk was not encoded correctly"

        assert os.path.exists(out3), "chunk3.chunk missing in output directory"
        with open(out3, "rb") as f:
            assert f.read() == b"\x00\xff", "chunk3.chunk was not encoded correctly"

        assert os.path.exists(out4), "chunk4.chunk missing in output directory"
        with open(out4, "rb") as f:
            assert f.read() == b"\x00\xff\x00\x01", "chunk4.chunk was not encoded correctly"

        assert os.path.exists(out5), "chunk5.chunk missing in output directory"
        with open(out5, "rb") as f:
            assert f.read() == b"\x00\xff\x00\x01", "chunk5.chunk was not encoded correctly"

        stat4 = os.stat(out4)
        stat5 = os.stat(out5)
        assert stat4.st_ino == stat5.st_ino, "chunk4.chunk and chunk5.chunk should be hardlinked to save disk space"
        assert stat4.st_nlink >= 2, "chunk4.chunk link count should be at least 2 due to hardlinking"