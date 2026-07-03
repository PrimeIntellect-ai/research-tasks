# test_final_state.py
import os
import json
import pytest

def test_pipeline_go_exists_and_concurrent():
    go_file = "/home/user/pipeline.go"
    assert os.path.isfile(go_file), f"File {go_file} does not exist."

    with open(go_file, "r", encoding="utf-8") as f:
        content = f.read()

    has_sync = '"sync"' in content or "sync." in content
    has_chan = "chan " in content or "chan<-" in content or "<-chan" in content or "make(chan" in content
    assert has_sync or has_chan, "The Go program must use concurrency primitives (sync or channels)."

def test_output_jsonl():
    out_file = "/home/user/output.jsonl"
    assert os.path.isfile(out_file), f"File {out_file} does not exist."

    results = []
    with open(out_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                results.append(data)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON line in output: {line}")

    assert len(results) == 3, f"Expected 3 categories in output, got {len(results)}."

    categories = [r.get("category") for r in results]
    assert categories == sorted(categories), "The output JSONL file must be sorted alphabetically by category."

    expected = {
        "Electronics": 4.0,
        "Home": 2.0,
        "Outdoors": 5.0
    }

    for r in results:
        cat = r.get("category")
        assert cat in expected, f"Unexpected category {cat} in output."
        rating = float(r.get("average_rating"))
        assert rating == expected[cat], f"Expected average rating for {cat} to be {expected[cat]}, got {rating}."