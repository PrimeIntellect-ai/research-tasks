# test_final_state.py

import os
import sqlite3

def compute_expected_metrics(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT id, name FROM authors")
    authors = c.fetchall()

    c.execute("SELECT author_id, paper_id FROM author_paper")
    author_paper = c.fetchall()

    c.execute("SELECT cited_paper_id, count FROM citations")
    citations = dict(c.fetchall())
    conn.close()

    author_papers_dict = {}
    paper_authors_dict = {}
    for aid, pid in author_paper:
        author_papers_dict.setdefault(aid, set()).add(pid)
        paper_authors_dict.setdefault(pid, set()).add(aid)

    results = []
    for aid, name in authors:
        coauthors = set()
        for pid in author_papers_dict.get(aid, []):
            for co_aid in paper_authors_dict.get(pid, []):
                if co_aid != aid:
                    coauthors.add(co_aid)

        coauthor_papers = set()
        for co_aid in coauthors:
            coauthor_papers.update(author_papers_dict.get(co_aid, []))

        total_citations = sum(citations.get(pid, 0) for pid in coauthor_papers)

        results.append((name, len(coauthors), total_citations))

    # Sort by citations DESC, name ASC
    results.sort(key=lambda x: (-x[2], x[0]))
    return results[:10]

def test_output_file_exists_and_correct():
    out_path = '/home/user/top_coauthor_metrics.txt'
    db_path = '/home/user/dataset.db'

    assert os.path.exists(out_path), f"The output file was not found at {out_path}."
    assert os.path.exists(db_path), f"The database file was not found at {db_path}."

    expected = compute_expected_metrics(db_path)

    with open(out_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "The output file is empty."

    parsed_results = []
    for i, line in enumerate(lines):
        parts = line.split('|')
        assert len(parts) == 3, f"Line {i+1} does not have exactly 3 parts separated by '|': {line}"
        name = parts[0]
        try:
            coauthors = int(parts[1])
            citations = 0 if parts[2] == '' else int(parts[2])
        except ValueError:
            assert False, f"Non-integer value found in metrics on line {i+1}: {line}"
        parsed_results.append((name, coauthors, citations))

    # Exclude Eve (0 coauthors) if the student's query omitted her due to INNER JOINs
    expected_non_zero = [r for r in expected if r[1] > 0]

    # Check if the parsed results match either the full expected list or the non-zero list
    if len(parsed_results) == len(expected_non_zero):
        assert parsed_results == expected_non_zero, f"The output metrics do not match the expected values. Got {parsed_results}, expected {expected_non_zero}"
    else:
        # If Eve is included, we compare against the full list up to the number of parsed results
        assert parsed_results[:len(expected_non_zero)] == expected_non_zero, f"The top non-zero output metrics do not match the expected values. Got {parsed_results[:len(expected_non_zero)]}, expected {expected_non_zero}"
        if len(parsed_results) > len(expected_non_zero):
            eve_result = parsed_results[len(expected_non_zero)]
            assert eve_result[0] == 'Eve', "Expected 'Eve' as the author with 0 coauthors."
            assert eve_result[1] == 0, "Expected 0 coauthors for Eve."
            assert eve_result[2] == 0, "Expected 0 citations for Eve's coauthors."