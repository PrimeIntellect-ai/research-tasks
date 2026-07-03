# test_final_state.py

import os
import json
from collections import defaultdict, Counter

def test_influential_topics_output():
    papers_file = "/home/user/papers.jsonl"
    output_file = "/home/user/influential_topics.json"

    assert os.path.exists(papers_file), f"Input file {papers_file} is missing."
    assert os.path.exists(output_file), f"Output file {output_file} was not created."

    # Recompute the truth from the papers.jsonl file
    papers = {}
    with open(papers_file, 'r') as f:
        for line in f:
            if line.strip():
                paper = json.loads(line)
                papers[paper['id']] = paper

    # Build citation graph: who cites whom
    cited_by = defaultdict(set)
    for p_id, p_data in papers.items():
        for ref in p_data.get('references', []):
            cited_by[ref].add(p_id)

    expected_output = {}
    for p_id in papers:
        citing_papers = cited_by[p_id]
        if len(citing_papers) >= 3:
            # Check if each citing paper is cited by at least 1 distinct paper
            if all(len(cited_by[c_id]) >= 1 for c_id in citing_papers):
                # It is influential
                topics_counter = Counter()
                for c_id in citing_papers:
                    for topic in papers[c_id].get('topics', []):
                        topics_counter[topic] += 1

                # Sort by count descending, then alphabetically ascending
                sorted_topics = sorted(topics_counter.items(), key=lambda x: (-x[1], x[0]))
                top_2_topics = [t[0] for t in sorted_topics[:2]]
                expected_output[p_id] = top_2_topics

    # Read the student's output
    with open(output_file, 'r') as f:
        try:
            student_output = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{output_file} does not contain valid JSON."

    assert isinstance(student_output, dict), f"Output JSON must be an object (dict), got {type(student_output).__name__}."

    assert student_output == expected_output, (
        f"Output does not match expected results.\n"
        f"Expected: {expected_output}\n"
        f"Got: {student_output}"
    )