# test_final_state.py

import os
import zipfile
import gzip
import pytest

ZIP_PATH = "/home/user/docs_project/modern_manuals.zip"

def test_zip_file_exists():
    assert os.path.isfile(ZIP_PATH), f"Error: {ZIP_PATH} not found"

def test_zip_contents():
    assert os.path.isfile(ZIP_PATH), f"Error: {ZIP_PATH} not found"

    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        namelist = z.namelist()

        # Check if the expected files are in the zip
        assert "chapter1.md.gz" in namelist or any(n.endswith("chapter1.md.gz") for n in namelist), "Error: chapter1.md.gz not found in zip"
        assert "chapter2.md.gz" in namelist or any(n.endswith("chapter2.md.gz") for n in namelist), "Error: chapter2.md.gz not found in zip"

def test_chapter1_content():
    assert os.path.isfile(ZIP_PATH), f"Error: {ZIP_PATH} not found"

    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        chap1_name = next((n for n in z.namelist() if n.endswith("chapter1.md.gz")), None)
        assert chap1_name is not None, "Error: chapter1.md.gz not found in zip"

        with z.open(chap1_name) as f:
            with gzip.open(f, 'rt', encoding='utf-8') as gz:
                content = gz.read()

        assert "# Introducción" in content, "Error: chapter1.md content mismatch or bad encoding"
        assert "Este es el capítulo uno." in content, "Error: chapter1.md content mismatch"
        assert "TITLE" not in content, "Error: Legacy tags were not completely removed"

def test_chapter2_content():
    assert os.path.isfile(ZIP_PATH), f"Error: {ZIP_PATH} not found"

    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        chap2_name = next((n for n in z.namelist() if n.endswith("chapter2.md.gz")), None)
        assert chap2_name is not None, "Error: chapter2.md.gz not found in zip"

        with z.open(chap2_name) as f:
            with gzip.open(f, 'rt', encoding='utf-8') as gz:
                content = gz.read()

        assert "# Conclusión" in content, "Error: chapter2.md content mismatch or bad encoding"
        assert "La documentación está completa." in content, "Error: chapter2.md content mismatch"
        assert "TITLE" not in content, "Error: Legacy tags were not completely removed"