# test_final_state.py
import os

def test_malicious_paths_log():
    log_path = "/home/user/malicious_paths.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} not found."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_paths = [
        "../home/user/.bashrc",
        "/etc/shadow",
        "docs/../../etc/passwd"
    ]

    assert lines == expected_paths, f"Expected malicious paths {expected_paths}, but got {lines}."

def test_clean_docs_extracted():
    clean_docs_dir = "/home/user/clean_docs"
    assert os.path.isdir(clean_docs_dir), f"Directory {clean_docs_dir} not found."

    expected_files = {
        "intro.md": "# Introduction\nWelcome to the docs.",
        "setup.md": "# Setup\nRun install.",
        "api/reference.md": "# API\nList of endpoints.",
        "appendix.md": "# Appendix\nExtra details."
    }

    for rel_path, expected_content in expected_files.items():
        full_path = os.path.join(clean_docs_dir, rel_path)
        assert os.path.isfile(full_path), f"Safe file {full_path} was not extracted."
        with open(full_path, "r") as f:
            content = f.read()
            assert content == expected_content, f"Content of {full_path} is incorrect."

def test_master_doc_content():
    master_doc_path = "/home/user/master_doc.md"
    assert os.path.isfile(master_doc_path), f"Master doc {master_doc_path} not found."

    expected_content = (
        "# Appendix\nExtra details.\n\n"
        "# Introduction\nWelcome to the docs.\n\n"
        "# API\nList of endpoints."
    )

    with open(master_doc_path, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"Master doc content is incorrect. Expected:\n{expected_content}\nGot:\n{content}"