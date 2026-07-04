# test_final_state.py

import os
import json
import pytest
from collections import defaultdict

def compute_expected_results():
    jsonl_path = '/home/user/data/papers.jsonl'

    if not os.path.isfile(jsonl_path):
        pytest.fail(f"Missing input file: {jsonl_path}")

    papers = {}
    in_degree = defaultdict(int)

    with open(jsonl_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            papers[data['paper_id']] = {
                'authors': set(data.get('authors', [])),
                'citations': set(data.get('citations', []))
            }
            # Initialize in_degree for all papers
            if data['paper_id'] not in in_degree:
                in_degree[data['paper_id']] = 0

    for pid, pdata in papers.items():
        for cited in pdata['citations']:
            in_degree[cited] += 1

    # Find highest centrality paper
    max_degree = -1
    highest_papers = []
    for pid, degree in in_degree.items():
        if degree > max_degree:
            max_degree = degree
            highest_papers = [pid]
        elif degree == max_degree:
            highest_papers.append(pid)

    highest_centrality_paper = sorted(highest_papers)[0] if highest_papers else ""

    # Find triads
    triads = []
    paper_ids = sorted(papers.keys())

    for a in paper_ids:
        for b in papers[a]['citations']:
            if b not in papers:
                continue
            for c in papers[b]['citations']:
                if c not in papers:
                    continue
                if a in papers[c]['citations']:
                    # Found a cycle A -> B -> C -> A
                    # Ensure distinct papers
                    if len({a, b, c}) == 3:
                        shared_authors = papers[a]['authors'].intersection(papers[b]['authors']).intersection(papers[c]['authors'])
                        for author in shared_authors:
                            triad_papers = sorted([a, b, c])
                            triad_entry = {
                                "shared_author_id": author,
                                "papers": triad_papers
                            }
                            if triad_entry not in triads:
                                triads.append(triad_entry)

    # Sort triads for deterministic comparison
    triads.sort(key=lambda x: (x["shared_author_id"], x["papers"]))

    return highest_centrality_paper, triads

def test_results_json_exists():
    results_path = '/home/user/workspace/results.json'
    assert os.path.isfile(results_path), f"The output file {results_path} is missing."

def test_results_json_content():
    results_path = '/home/user/workspace/results.json'
    if not os.path.isfile(results_path):
        pytest.fail("results.json not found")

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    expected_highest, expected_triads = compute_expected_results()

    assert "highest_centrality_paper" in results, "Missing 'highest_centrality_paper' key in results.json"
    assert results["highest_centrality_paper"] == expected_highest, \
        f"Incorrect highest centrality paper. Expected {expected_highest}, got {results['highest_centrality_paper']}"

    assert "triad_patterns" in results, "Missing 'triad_patterns' key in results.json"

    actual_triads = results["triad_patterns"]
    assert isinstance(actual_triads, list), "'triad_patterns' must be a list"

    # Normalize actual triads
    normalized_actual = []
    for t in actual_triads:
        assert "shared_author_id" in t, "Missing 'shared_author_id' in triad pattern"
        assert "papers" in t, "Missing 'papers' in triad pattern"
        assert isinstance(t["papers"], list), "'papers' must be a list"
        normalized_actual.append({
            "shared_author_id": t["shared_author_id"],
            "papers": sorted(t["papers"])
        })

    normalized_actual.sort(key=lambda x: (x["shared_author_id"], x["papers"]))

    assert len(normalized_actual) == len(expected_triads), \
        f"Incorrect number of triads. Expected {len(expected_triads)}, got {len(normalized_actual)}"

    for actual, expected in zip(normalized_actual, expected_triads):
        assert actual == expected, f"Triad mismatch. Expected {expected}, got {actual}"