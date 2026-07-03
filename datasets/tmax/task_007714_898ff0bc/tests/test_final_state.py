# test_final_state.py
import os
import pytest

def test_updated_master_csv():
    output_path = "/home/user/updated_master.csv"
    assert os.path.isfile(output_path), f"Expected output file {output_path} does not exist."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, f"File {output_path} is empty."

    # Check header
    header = lines[0]
    assert header == "string_id,en_text,es_text,status", f"Header is incorrect: {header}"

    # Check data rows (ignoring order as per requirements)
    data_lines = sorted(lines[1:])

    expected_data = [
        "STR_001,Hello world,Hola mundo,approved",
        "STR_002,Save,Guardar,approved",
        "STR_003,Cancel,Cancelar,updated",
        "STR_004,Delete,Eliminar,updated",
        "STR_006,Settings,Configuracion,updated"
    ]

    expected_data_sorted = sorted(expected_data)

    assert data_lines == expected_data_sorted, (
        f"Data rows in {output_path} do not match expected output.\n"
        f"Expected: {expected_data_sorted}\n"
        f"Actual: {data_lines}"
    )