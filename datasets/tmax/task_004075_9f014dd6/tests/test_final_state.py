# test_final_state.py

import os
import json
import time
import subprocess
import random

def test_analyze_go_correctness_and_speed():
    go_file = "/home/user/analyze.go"
    assert os.path.exists(go_file), f"{go_file} not found"

    # Generate hidden dataset
    hidden_logs_path = "/tmp/hidden_logs.jsonl"
    num_records = 150000

    langs = ["en", "ja", "es", "fr"]
    base_messages = {
        "en": ["helloworld", "testinglog", "erroroccurred"],
        "ja": ["こんにちは世界", "テストログ", "エラー発生"],
        "es": ["holamundo", "pruebaderegistro", "ocurriounerror"],
        "fr": ["bonjourlemonde", "journaldetest", "uneerreursestproduite"]
    }

    expected_counts = {lang: {msg: 0 for msg in msgs} for lang, msgs in base_messages.items()}

    # Use a fixed seed for reproducibility
    random.seed(42)

    with open(hidden_logs_path, "w", encoding="utf-8") as f:
        for i in range(num_records):
            lang = random.choice(langs)
            base_msg = random.choice(base_messages[lang])
            expected_counts[lang][base_msg] += 1

            # Obfuscate base_msg with punctuation, spaces, and casing
            obfuscated = ""
            for char in base_msg:
                # Randomly uppercase
                if random.random() < 0.5:
                    obfuscated += char.upper()
                else:
                    obfuscated += char

                # Insert random non-letter/number characters
                if random.random() < 0.3:
                    obfuscated += random.choice(" \t\n!@#$%^&*()_+-=[]{}|;':\",./<>?~`")

            record = {"id": str(i), "lang": lang, "message": obfuscated}
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Calculate expected summary
    expected_summary = {
        "total_records": num_records,
        "unique_normalized_messages": sum(len(msgs) for msgs in base_messages.values()),
        "top_message_per_lang": {}
    }
    for lang, counts in expected_counts.items():
        top_msg = max(counts.items(), key=lambda x: (x[1], x[0])) # Tie-breaker
        expected_summary["top_message_per_lang"][lang] = {
            "normalized_message": top_msg[0],
            "count": top_msg[1]
        }

    # Compile the Go program so we don't measure compilation time
    compile_cmd = ["go", "build", "-o", "/tmp/analyze", go_file]
    try:
        subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to compile {go_file}:\n{e.stderr}"

    # Run the compiled program
    start_time = time.time()
    run_cmd = ["/tmp/analyze", hidden_logs_path]
    try:
        subprocess.run(run_cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        assert False, f"Execution of compiled Go program failed:\n{e.stderr}"
    runtime = time.time() - start_time

    # Check output
    summary_path = "/home/user/summary.json"
    assert os.path.exists(summary_path), f"{summary_path} not found. Did your program create it?"

    with open(summary_path, "r", encoding="utf-8") as f:
        try:
            output_summary = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{summary_path} does not contain valid JSON"

    assert output_summary == expected_summary, f"Output summary does not match expected.\nOutput: {output_summary}\nExpected: {expected_summary}"
    assert runtime <= 2.0, f"Runtime {runtime:.2f}s exceeded threshold of 2.0s. The program is not fast enough (are you shelling out to the binary?)"