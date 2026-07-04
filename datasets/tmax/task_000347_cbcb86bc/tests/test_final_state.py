# test_final_state.py
import os
import stat

def test_run_pipeline_script_exists_and_executable():
    path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(path), f"File {path} is missing."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_processed_samples_csv_exists():
    path = "/home/user/processed_samples.csv"
    assert os.path.isfile(path), f"File {path} is missing."

def test_processed_samples_csv_content():
    path = "/home/user/processed_samples.csv"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_content = """bucket,locale,masked_id,cleaned_text
2023-10-24-14,es_ES,MASKED,Hola
2023-10-24-14,fr_FR,MASKED,Bonjour\\nle monde
2023-10-24-14,fr_FR,MASKED,Merci beaucoup
2023-10-24-15,es_ES,MASKED,Hola\\nAmigo
2023-10-24-15,es_ES,MASKED,Adiós
2023-10-25-09,de_DE,MASKED,Guten\\nMorgen"""

    assert content == expected_content.strip(), "Content of processed_samples.csv does not match the expected final state."

def test_rust_project_exists():
    path = "/home/user/loc_pipeline"
    assert os.path.isdir(path), f"Directory {path} is missing. A Rust project was expected here."
    cargo_toml = os.path.join(path, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"File {cargo_toml} is missing. Not a valid Rust project."