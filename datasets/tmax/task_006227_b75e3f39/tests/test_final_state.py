# test_final_state.py

import os
import json
import re

def compute_expected_results(input_path):
    expected_normalized = []
    stats = {}

    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            msg_id = data['id']
            locale = data['locale']
            content = data['content']

            # Find math blocks
            math_blocks = re.findall(r'\$(.*?)\$', content)

            # Normalize content
            def replace_math(match):
                inner = match.group(1)
                inner_no_ws = re.sub(r'\s+', '', inner)
                return f"${inner_no_ws}$"

            normalized_content = re.sub(r'\$(.*?)\$', replace_math, content)
            expected_normalized.append({
                "id": msg_id,
                "locale": locale,
                "normalized_content": normalized_content
            })

            # Calculate complexity
            complexity = 0
            for block in math_blocks:
                complexity += sum(block.count(op) for op in ['+', '-', '*', '/', '='])

            # Calculate text length
            text_only = re.sub(r'\$.*?\$', '', content)
            text_length = len(text_only.strip())

            # Update stats
            if locale not in stats:
                stats[locale] = {
                    "message_count": 0,
                    "total_text_length": 0,
                    "max_math_complexity": 0
                }

            stats[locale]["message_count"] += 1
            stats[locale]["total_text_length"] += text_length
            stats[locale]["max_math_complexity"] = max(stats[locale]["max_math_complexity"], complexity)

    expected_stats = {}
    for loc, s in stats.items():
        avg_len = s["total_text_length"] / s["message_count"]
        expected_stats[loc] = {
            "message_count": s["message_count"],
            "avg_text_length": round(avg_len, 2),
            "max_math_complexity": s["max_math_complexity"]
        }

    return expected_normalized, expected_stats

def test_normalized_translations():
    input_path = "/home/user/raw_translations.jsonl"
    output_path = "/home/user/normalized_translations.jsonl"

    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    expected_normalized, _ = compute_expected_results(input_path)

    actual_normalized = []
    with open(output_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                actual_normalized.append(json.loads(line))
            except json.JSONDecodeError:
                assert False, f"Invalid JSON line in {output_path}: {line}"

    assert len(actual_normalized) == len(expected_normalized), f"Expected {len(expected_normalized)} lines, found {len(actual_normalized)}"

    for expected, actual in zip(expected_normalized, actual_normalized):
        assert actual.get("id") == expected["id"], f"Expected id {expected['id']}, got {actual.get('id')}"
        assert actual.get("locale") == expected["locale"], f"Expected locale {expected['locale']}, got {actual.get('locale')}"
        assert actual.get("normalized_content") == expected["normalized_content"], f"Content mismatch for id {expected['id']}. Expected: {expected['normalized_content']}, Got: {actual.get('normalized_content')}"

def test_locale_stats():
    input_path = "/home/user/raw_translations.jsonl"
    stats_path = "/home/user/locale_stats.json"

    assert os.path.exists(stats_path), f"Output file {stats_path} does not exist."

    _, expected_stats = compute_expected_results(input_path)

    with open(stats_path, 'r', encoding='utf-8') as f:
        try:
            actual_stats = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Invalid JSON in {stats_path}"

    assert set(actual_stats.keys()) == set(expected_stats.keys()), f"Locales mismatch. Expected {set(expected_stats.keys())}, got {set(actual_stats.keys())}"

    for loc, expected in expected_stats.items():
        actual = actual_stats[loc]
        assert actual.get("message_count") == expected["message_count"], f"Message count mismatch for {loc}"
        assert actual.get("max_math_complexity") == expected["max_math_complexity"], f"Max math complexity mismatch for {loc}"

        # Check avg_text_length with some tolerance for float precision
        actual_avg = actual.get("avg_text_length")
        assert actual_avg is not None, f"Missing avg_text_length for {loc}"
        assert abs(actual_avg - expected["avg_text_length"]) < 0.02, f"Avg text length mismatch for {loc}. Expected {expected['avg_text_length']}, got {actual_avg}"