# test_final_state.py
import os
import glob
import subprocess
import tempfile
import stat
from pathlib import Path

def run_student_script(input_dir, output_dir):
    script_path = "/home/user/storage_manager.py"
    assert os.path.isfile(script_path), f"Student script not found at {script_path}"

    try:
        result = subprocess.run(
            ["python3", script_path, str(input_dir), str(output_dir)],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result
    except subprocess.TimeoutExpired:
        assert False, "Student script timed out after 60 seconds."

def test_clean_corpus_processing():
    clean_dir = Path("/app/clean_corpus")
    assert clean_dir.is_dir(), f"Clean corpus missing at {clean_dir}"

    frm1_files = list(clean_dir.glob("*.frm1"))
    assert len(frm1_files) > 0, "No .frm1 files found in clean corpus."

    with tempfile.TemporaryDirectory() as temp_out:
        out_dir = Path(temp_out)
        result = run_student_script(clean_dir, out_dir)

        seq_dir = out_dir / "sequence"
        obj_dir = out_dir / "objects"

        assert seq_dir.is_dir(), f"Sequence directory not created at {seq_dir}"
        assert obj_dir.is_dir(), f"Objects directory not created at {obj_dir}"

        failed_clean = []
        for frm1 in frm1_files:
            expected_symlink = seq_dir / f"{frm1.stem}.raw"
            if not expected_symlink.is_symlink():
                failed_clean.append(frm1.name)
                continue

            target = expected_symlink.resolve()
            if not target.is_file() or target.parent != obj_dir:
                failed_clean.append(frm1.name)

        if failed_clean:
            assert False, f"{len(failed_clean)} of {len(frm1_files)} clean files were modified/rejected or incorrectly processed. Offending files: {', '.join(failed_clean[:10])}"

        # Verify deduplication (40 unique objects expected for the 100 clean files)
        objects = list(obj_dir.glob("*.raw"))
        assert len(objects) == 40, f"Expected exactly 40 deduplicated objects in clean output, found {len(objects)}"

        # Verify hard links by checking total references to inodes
        inodes = set()
        for obj in objects:
            inodes.add(obj.stat().st_ino)
        assert len(inodes) == 40, f"Expected 40 unique inodes in objects directory, found {len(inodes)}"

def test_evil_corpus_rejection():
    evil_dir = Path("/app/evil_corpus")
    assert evil_dir.is_dir(), f"Evil corpus missing at {evil_dir}"

    frm1_files = list(evil_dir.glob("*.frm1"))
    assert len(frm1_files) > 0, "No .frm1 files found in evil corpus."

    with tempfile.TemporaryDirectory() as temp_out:
        out_dir = Path(temp_out)
        result = run_student_script(evil_dir, out_dir)

        seq_dir = out_dir / "sequence"

        bypassed_evil = []
        for frm1 in frm1_files:
            expected_symlink = seq_dir / f"{frm1.stem}.raw"
            if expected_symlink.exists() or expected_symlink.is_symlink():
                bypassed_evil.append(frm1.name)

        if bypassed_evil:
            assert False, f"{len(bypassed_evil)} of {len(frm1_files)} evil files bypassed validation. Offending files: {', '.join(bypassed_evil[:10])}"

        # Also ensure no objects were created
        obj_dir = out_dir / "objects"
        if obj_dir.is_dir():
            objects = list(obj_dir.glob("*.raw"))
            assert len(objects) == 0, f"Expected 0 objects from evil corpus, found {len(objects)}"