# test_final_state.py
import os
import subprocess
import glob
import pytest

def test_vendor_package_fixed():
    lib_rs = "/app/vendor/packet_decode/src/lib.rs"
    assert os.path.exists(lib_rs), f"Missing {lib_rs}"
    with open(lib_rs, "r") as f:
        content = f.read()
        assert "Reuslt" not in content, "The deliberate typo 'Reuslt' was not fixed in lib.rs"
        assert "Result" in content, "The return type 'Result' is not present in lib.rs"

def test_run_pipeline_script_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"Missing integration script at {script_path}"
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable"

def test_net_classifier_binary_exists():
    debug_bin = "/home/user/net_classifier/target/debug/net_classifier"
    release_bin = "/home/user/net_classifier/target/release/net_classifier"

    # We can also attempt to build it if it's not built, but the prompt says the verifier will directly invoke it.
    # Let's just find the binary. If neither exists, try building it.
    if not os.path.exists(debug_bin) and not os.path.exists(release_bin):
        cargo_toml = "/home/user/net_classifier/Cargo.toml"
        assert os.path.exists(cargo_toml), "net_classifier Rust project is missing"
        subprocess.run(["cargo", "build", "--release"], cwd="/home/user/net_classifier", capture_output=True)

    assert os.path.exists(debug_bin) or os.path.exists(release_bin), "net_classifier binary not found"

def test_adversarial_corpus_verification():
    debug_bin = "/home/user/net_classifier/target/debug/net_classifier"
    release_bin = "/home/user/net_classifier/target/release/net_classifier"

    bin_path = release_bin if os.path.exists(release_bin) else debug_bin
    assert os.path.exists(bin_path), "net_classifier binary not found"

    evil_corpus_path = "/app/corpora/evil"
    clean_corpus_path = "/app/corpora/clean"

    evil_files = glob.glob(os.path.join(evil_corpus_path, "*"))
    clean_files = glob.glob(os.path.join(clean_corpus_path, "*"))

    assert len(evil_files) > 0, "No evil corpus files found"
    assert len(clean_files) > 0, "No clean corpus files found"

    evil_bypassed = []
    clean_modified = []

    # Test Evil Corpus
    for e_file in evil_files:
        with open(e_file, "r") as f:
            lines = f.read().splitlines()

        for line in lines:
            if not line.strip():
                continue
            proc = subprocess.run([bin_path], input=line, text=True, capture_output=True)
            output = proc.stdout.strip()
            if not output.startswith("DROP:"):
                evil_bypassed.append((os.path.basename(e_file), line, output))

    # Test Clean Corpus
    for c_file in clean_files:
        with open(c_file, "r") as f:
            lines = f.read().splitlines()

        for line in lines:
            if not line.strip():
                continue
            proc = subprocess.run([bin_path], input=line, text=True, capture_output=True)
            output = proc.stdout.strip()
            if not output.startswith("ACCEPT:"):
                clean_modified.append((os.path.basename(c_file), line, output))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} evil bypassed. Offending files: {', '.join(set([x[0] for x in evil_bypassed]))}")
    if clean_modified:
        error_messages.append(f"{len(clean_modified)} clean modified. Offending files: {', '.join(set([x[0] for x in clean_modified]))}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_messages)

def test_run_pipeline_functionality(tmp_path):
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), "Missing script"

    test_log = tmp_path / "test.log"
    test_log.write_text("2023-10-10 12:00:00 [INFO] PID:1234 {\"protocol\": \"HTTP\", \"source_ip\": \"192.168.1.5\", \"payload\": \"GET / HTTP/1.1\"}\n")

    proc = subprocess.run(["bash", script_path, str(test_log)], capture_output=True, text=True)
    output = proc.stdout.strip()

    # Since it's clean traffic, it should be ACCEPT
    assert "ACCEPT: {\"protocol\": \"HTTP\", \"source_ip\": \"192.168.1.5\", \"payload\": \"GET / HTTP/1.1\"}" in output, "Pipeline script did not correctly strip prefixes or pipe to binary"