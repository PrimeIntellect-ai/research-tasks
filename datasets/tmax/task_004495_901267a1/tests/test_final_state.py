# test_final_state.py
import os
import csv
import stat

def test_scripts_exist():
    """Check if the required scripts were created."""
    assert os.path.isfile('/home/user/normalize.py'), "normalize.py is missing"
    assert os.path.isfile('/home/user/aggregate.py'), "aggregate.py is missing"
    assert os.path.isfile('/home/user/pipeline.sh'), "pipeline.sh is missing"

def test_pipeline_executable_and_set_e():
    """Check if pipeline.sh is executable and uses set -e."""
    pipeline_path = '/home/user/pipeline.sh'
    st = os.stat(pipeline_path)
    assert bool(st.st_mode & stat.S_IXUSR), "pipeline.sh is not executable"

    with open(pipeline_path, 'r') as f:
        content = f.read()
    assert 'set -e' in content, "pipeline.sh must use 'set -e'"

def test_final_csv_exists_and_content():
    """Check if the final CSV is generated with the correct content."""
    csv_path = '/home/user/final_translations.csv'
    assert os.path.isfile(csv_path), "final_translations.csv was not generated"

    expected_csv = [
        ["lang", "id", "normalized_text"],
        ["es-ES", "btn_save", "Guardar"],
        ["es-ES", "err_404", "No encontrado"],
        ["es-ES", "msg_welcome", '"Bienvenidos" a la aplicación'],
        ["fr-FR", "btn_save", "Enregistrer"],
        ["fr-FR", "err_404", "La page n'existe pas"]
    ]

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))

    assert reader == expected_csv, f"CSV content mismatch.\nExpected: {expected_csv}\nGot: {reader}"