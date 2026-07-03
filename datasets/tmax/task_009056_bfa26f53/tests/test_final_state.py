# test_final_state.py

import os
import csv
import hashlib
from collections import defaultdict

def test_summary_report_exists_and_correct():
    report_path = '/home/user/summary_report.md'
    csv_path = '/home/user/reviews.csv'
    template_path = '/home/user/template.md'

    assert os.path.isfile(report_path), f"Failure: {report_path} not found."
    assert os.path.isfile(csv_path), f"Failure: {csv_path} not found."
    assert os.path.isfile(template_path), f"Failure: {template_path} not found."

    # 1. Read and deduplicate
    # Key: SHA-256 of UserID|ProductID|ReviewText
    # Value: row dict
    deduped = {}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            hash_str = f"{row['UserID']}|{row['ProductID']}|{row['ReviewText']}"
            h = hashlib.sha256(hash_str.encode('utf-8')).hexdigest()

            if h not in deduped:
                deduped[h] = row
            else:
                # Keep earliest timestamp
                if row['Timestamp'] < deduped[h]['Timestamp']:
                    deduped[h] = row

    # 2. Compute statistics
    stats = defaultdict(lambda: {'count': 0, 'sum': 0.0})
    for row in deduped.values():
        pid = row['ProductID']
        stats[pid]['count'] += 1
        stats[pid]['sum'] += float(row['Rating'])

    # 3. Generate expected report
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()

    expected_sections = ["# Product Review Summary\n"]

    for pid in sorted(stats.keys()):
        count = stats[pid]['count']
        avg = stats[pid]['sum'] / count

        section = template_content.replace('{{ProductID}}', pid)
        section = section.replace('{{TotalReviews}}', str(count))
        section = section.replace('{{AverageRating}}', f"{avg:.2f}")
        expected_sections.append(section)

    expected_output = "\n".join(expected_sections).strip()

    # Read actual report
    with open(report_path, 'r', encoding='utf-8') as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, (
        f"Failure: Output does not match expected result.\n"
        f"Expected:\n{expected_output}\n\n"
        f"Actual:\n{actual_output}"
    )