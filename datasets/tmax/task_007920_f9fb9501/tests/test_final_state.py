# test_final_state.py
import os
import csv

def test_results_file_exists():
    assert os.path.isfile('/home/user/forensics/results.csv'), "The output file /home/user/forensics/results.csv is missing. Did you run the compiled analyzer?"

def test_results_content_and_accuracy():
    input_file = '/home/user/forensics/data/batch_42.csv'
    output_file = '/home/user/forensics/results.csv'

    assert os.path.isfile(input_file), f"Input file {input_file} is missing."
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    expected_scores = {}
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            id_val = row['ID']
            base = int(row['BaseScore'])
            events = int(row['EventCount'])
            time_w = int(row['TimeWindow'])

            # Compute expected score using floating point division
            score = (base * 0.6) + ((float(events) / float(time_w)) * 0.4)
            expected_scores[id_val] = score

    actual_scores = {}
    with open(output_file, 'r') as f:
        reader = csv.DictReader(f)
        assert 'ID' in reader.fieldnames and 'RiskScore' in reader.fieldnames, "results.csv must have headers 'ID' and 'RiskScore'"
        for row in reader:
            actual_scores[row['ID']] = float(row['RiskScore'])

    assert len(actual_scores) == len(expected_scores), f"Expected {len(expected_scores)} rows in results.csv, but found {len(actual_scores)}. The service might have crashed or hung."

    for id_val, expected_score in expected_scores.items():
        assert id_val in actual_scores, f"Event {id_val} is missing from results.csv. The parser might have stopped prematurely."
        actual_score = actual_scores[id_val]

        # Format expected score to 2 decimal places as C++ would with std::fixed and std::setprecision(2)
        expected_rounded = round(expected_score, 2)

        assert abs(actual_score - expected_rounded) <= 0.015, (
            f"Score for {id_val} is incorrect. "
            f"Expected ~{expected_rounded:.2f}, got {actual_score:.2f}. "
            "Check if the integer division bug was properly fixed."
        )