# test_final_state.py

import os
import pytest

BASE_DIR = "/home/user/messy_project"
ALL_CODE_PATH = "/home/user/all_code.py"
CHUNKS_DIR = "/home/user/chunks"

def test_renamed_files():
    # note1.txt should remain untouched
    note1_path = os.path.join(BASE_DIR, "docs", "note1.txt")
    assert os.path.isfile(note1_path), f"File should be untouched: {note1_path}"

    # note2.txt and todo_list.txt should be renamed to .todo
    note2_todo = os.path.join(BASE_DIR, "docs", "note2.todo")
    todo_list_todo = os.path.join(BASE_DIR, "src", "todo_list.todo")
    note2_txt = os.path.join(BASE_DIR, "docs", "note2.txt")
    todo_list_txt = os.path.join(BASE_DIR, "src", "todo_list.txt")

    assert os.path.isfile(note2_todo), f"File not found or not renamed properly: {note2_todo}"
    assert os.path.isfile(todo_list_todo), f"File not found or not renamed properly: {todo_list_todo}"

    assert not os.path.exists(note2_txt), f"Original file should not exist: {note2_txt}"
    assert not os.path.exists(todo_list_txt), f"Original file should not exist: {todo_list_txt}"

def test_all_code_file():
    assert os.path.isfile(ALL_CODE_PATH), f"Merged file not found: {ALL_CODE_PATH}"

    with open(ALL_CODE_PATH, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 115, f"Expected 115 lines in {ALL_CODE_PATH}, found {len(lines)}"

    # Check alphabetical ordering based on absolute paths:
    # 1. /home/user/messy_project/lib/utils/helper.py (30 lines)
    # 2. /home/user/messy_project/src/app.py (25 lines)
    # 3. /home/user/messy_project/src/core/main.py (60 lines)
    assert lines[0] == 'print("Helper line 1")', "First line does not match expected output from helper.py"
    assert lines[30] == 'print("App line 1")', "Line 31 does not match expected output from app.py"
    assert lines[55] == 'print("Main line 1")', "Line 56 does not match expected output from main.py"

def test_chunks():
    assert os.path.isdir(CHUNKS_DIR), f"Chunks directory not found: {CHUNKS_DIR}"

    chunk_00 = os.path.join(CHUNKS_DIR, "chunk_00.py")
    chunk_01 = os.path.join(CHUNKS_DIR, "chunk_01.py")
    chunk_02 = os.path.join(CHUNKS_DIR, "chunk_02.py")

    assert os.path.isfile(chunk_00), f"Chunk file missing: {chunk_00}"
    assert os.path.isfile(chunk_01), f"Chunk file missing: {chunk_01}"
    assert os.path.isfile(chunk_02), f"Chunk file missing: {chunk_02}"

    with open(chunk_00, "r") as f:
        assert len(f.readlines()) == 50, f"Expected 50 lines in {chunk_00}"

    with open(chunk_01, "r") as f:
        assert len(f.readlines()) == 50, f"Expected 50 lines in {chunk_01}"

    with open(chunk_02, "r") as f:
        assert len(f.readlines()) == 15, f"Expected 15 lines in {chunk_02}"

    # Ensure no extra chunk files exist
    all_chunks = [f for f in os.listdir(CHUNKS_DIR) if f.startswith("chunk_") and f.endswith(".py")]
    assert len(all_chunks) == 3, f"Expected exactly 3 chunk files, found {len(all_chunks)}"