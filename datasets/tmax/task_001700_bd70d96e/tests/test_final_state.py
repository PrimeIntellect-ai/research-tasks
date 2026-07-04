# test_final_state.py
import os
import csv
import json
import unicodedata

def test_monthly_stats():
    stats_path = '/home/user/monthly_stats.csv'
    assert os.path.isfile(stats_path), f"File {stats_path} is missing."

    with open(stats_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 4, f"Expected 4 rows (including header) in {stats_path}, found {len(rows)}"
    assert rows[0] == ['month', 'total_reviews', 'avg_rating', 'avg_review_length'], "Header is incorrect"

    # Allow for .0 or .00 formatting
    def check_row(row, expected_month, expected_total, expected_rating, expected_len):
        assert row[0] == expected_month, f"Expected month {expected_month}, got {row[0]}"
        assert row[1] == expected_total, f"Expected total_reviews {expected_total}, got {row[1]}"
        assert float(row[2]) == float(expected_rating), f"Expected avg_rating {expected_rating}, got {row[2]}"
        assert float(row[3]) == float(expected_len), f"Expected avg_review_length {expected_len}, got {row[3]}"

    check_row(rows[1], '2023-01', '2', '4.5', '20.0')
    check_row(rows[2], '2023-02', '2', '2.5', '8.5')
    check_row(rows[3], '2023-03', '1', '4.0', '22.0')

def test_cleaned_reviews():
    jsonl_path = '/home/user/cleaned_reviews.jsonl'
    assert os.path.isfile(jsonl_path), f"File {jsonl_path} is missing."

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 5, f"Expected 5 records in {jsonl_path}, found {len(lines)}"

    users = set()
    for line in lines:
        record = json.loads(line)
        users.add(record['user_id'])

        # Check no newlines
        assert '\n' not in record['review_text'], f"Found newline in review_text for user {record['user_id']}"
        assert '\r' not in record['review_text'], f"Found carriage return in review_text for user {record['user_id']}"

        # Check rating is int
        assert isinstance(record['rating'], int), f"Rating for user {record['user_id']} is not an integer"

        # Check NFKC normalization
        assert record['review_text'] == unicodedata.normalize('NFKC', record['review_text']), f"review_text for user {record['user_id']} is not NFKC normalized"

        if record['user_id'] == 'u4':
            assert len(record['review_text']) == 4, "Length of review_text for u4 should be 4 after NFKC normalization"
            assert record['review_text'] == 'café', "review_text for u4 is incorrect"

    assert users == {'u1', 'u2', 'u4', 'u5', 'u6'}, f"Expected users {{u1, u2, u4, u5, u6}}, found {users}"