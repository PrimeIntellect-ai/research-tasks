# test_final_state.py
import os
import re
import subprocess
import struct
import random
import string
import tempfile
import fcntl
import pytest

def test_transcription():
    transcript_path = "/home/user/transcript.txt"
    assert os.path.exists(transcript_path), "Transcript file is missing."
    with open(transcript_path, "r") as f:
        content = f.read()

    # Strip punctuation and whitespace, convert to lowercase
    cleaned_content = re.sub(r'[^\w\s]', '', content).strip().lower()
    expected = "incremental backups provide differential payload structures"

    assert expected in cleaned_content, f"Transcript does not contain the expected text. Got: {content}"

def create_wav(path, chunk_size, num_channels, sample_rate):
    with open(path, 'wb') as f:
        f.write(b'RIFF')
        f.write(struct.pack('<I', chunk_size))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16)) # Subchunk1Size
        f.write(struct.pack('<H', 1))  # AudioFormat
        f.write(struct.pack('<H', num_channels))
        f.write(struct.pack('<I', sample_rate))
        byte_rate = sample_rate * num_channels * 2
        f.write(struct.pack('<I', byte_rate))
        block_align = num_channels * 2
        f.write(struct.pack('<H', block_align))
        f.write(struct.pack('<H', 16)) # BitsPerSample
        f.write(b'data')
        subchunk2_size = chunk_size - 36 if chunk_size >= 36 else 0
        f.write(struct.pack('<I', subchunk2_size))

def test_indexer_fuzz_equivalence():
    agent_bin = "/home/user/indexer"
    oracle_bin = "/opt/oracle/indexer_oracle"

    assert os.path.exists(agent_bin), "Agent binary /home/user/indexer is missing."
    assert os.access(agent_bin, os.X_OK), "Agent binary is not executable."
    assert os.path.exists(oracle_bin), "Oracle binary is missing."

    random.seed(42)
    N = 1000

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(N):
            chunk_size = random.randint(36, 2**31 - 1)
            num_channels = random.randint(1, 16)
            sample_rate = random.randint(8000, 192000)

            wav_path = os.path.join(tmpdir, f"test_{i}.wav")
            create_wav(wav_path, chunk_size, num_channels, sample_rate)

            # Run oracle
            oracle_proc = subprocess.run([oracle_bin, wav_path], capture_output=True, text=True)
            # Run agent
            agent_proc = subprocess.run([agent_bin, wav_path], capture_output=True, text=True)

            assert agent_proc.returncode == oracle_proc.returncode, f"Exit code mismatch on input {wav_path}. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"
            assert agent_proc.stdout == oracle_proc.stdout, f"Output mismatch on input {wav_path} (ChunkSize={chunk_size}, Channels={num_channels}, SampleRate={sample_rate}).\nOracle:\n{oracle_proc.stdout}\nAgent:\n{agent_proc.stdout}"

def test_indexer_locking():
    agent_bin = "/home/user/indexer"
    assert os.path.exists(agent_bin), "Agent binary /home/user/indexer is missing."

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
        create_wav(tmp_path, 100, 2, 44100)

    try:
        # Acquire an exclusive write lock to simulate backup process
        with open(tmp_path, 'r+b') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

            # Run agent, it should fail to acquire read lock
            agent_proc = subprocess.run([agent_bin, tmp_path], capture_output=True, text=True)

            assert agent_proc.returncode == 1, "Agent should exit with code 1 when file is locked exclusively."

            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    finally:
        os.remove(tmp_path)