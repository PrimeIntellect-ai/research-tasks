# test_final_state.py

import os
import json
import csv
from collections import defaultdict

def test_top_authors_output():
    authors_path = "/home/user/authors.csv"
    papers_path = "/home/user/papers.jsonl"
    citations_path = "/home/user/citations.txt"
    output_path = "/home/user/top_authors.txt"

    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    # 1. Read authors
    authors = {}
    with open(authors_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            authors[int(row["author_id"])] = row["name"]

    # 2. Read papers
    papers = {}
    with open(papers_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            papers[data["id"]] = {
                "year": data["year"],
                "authors": data["authors"]
            }

    # 3. Read citations and compute valid counts
    author_counts = defaultdict(int)
    with open(citations_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            citing_id, cited_id = line.split()

            if citing_id in papers and cited_id in papers:
                citing_year = papers[citing_id]["year"]
                cited_year = papers[cited_id]["year"]

                if cited_year < 2020 and citing_year >= 2022:
                    for author_id in papers[cited_id]["authors"]:
                        author_counts[author_id] += 1

    # 4. Format and sort expected output
    expected_results = []
    for author_id, count in author_counts.items():
        if count > 0:
            name = authors[author_id]
            expected_results.append((name, count))

    expected_results.sort(key=lambda x: (-x[1], x[0]))
    expected_lines = [f"{name}:{count}" for name, count in expected_results]

    # 5. Read actual output
    with open(output_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {output_path} do not match the expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )