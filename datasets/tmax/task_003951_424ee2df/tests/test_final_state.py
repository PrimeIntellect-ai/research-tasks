# test_final_state.py
import os
import pandas as pd

def compute_reference(fasta_path):
    alpha = 0.62
    beta = 1.15
    gamma = 0.04

    with open(fasta_path, 'r') as f:
        lines = f.read().splitlines()

    results = {}
    current_id = None
    for line in lines:
        if line.startswith('>'):
            current_id = line[1:].strip()
        else:
            primer = line[:20]
            if len(primer) < 20: continue

            g_c_count = primer.count('G') + primer.count('C')
            a_t_count = primer.count('A') + primer.count('T')
            gc_content = g_c_count / 20.0
            tm = 4 * g_c_count + 2 * a_t_count

            max_homo = 1
            current_homo = 1
            for i in range(1, 20):
                if primer[i] == primer[i-1]:
                    current_homo += 1
                    max_homo = max(max_homo, current_homo)
                else:
                    current_homo = 1

            score = (alpha * gc_content) + (beta * (tm / 100.0)) - (gamma * max_homo)
            results[current_id] = score
    return results

def test_final_state():
    output_csv = '/home/user/output/primer_scores.csv'
    fasta_path = '/home/user/data/targets.fasta'

    assert os.path.exists(output_csv), f"Output file not found at {output_csv}"

    try:
        df = pd.read_csv(output_csv)
    except Exception as e:
        assert False, f"Failed to parse CSV at {output_csv}: {e}"

    expected_columns = ['SequenceID', 'Primer20', 'Score']
    for col in expected_columns:
        assert col in df.columns, f"Missing column '{col}' in output CSV. Found columns: {list(df.columns)}"

    ref = compute_reference(fasta_path)
    assert len(df) == len(ref), f"Expected {len(ref)} rows, but got {len(df)}."

    mse = 0.0
    for _, row in df.iterrows():
        sid = str(row['SequenceID'])
        val = float(row['Score'])
        assert sid in ref, f"Sequence ID '{sid}' not found in reference."
        expected = ref[sid]
        mse += (val - expected)**2

    mse /= len(df)

    threshold = 1e-8
    assert mse <= threshold, f"MSE {mse} exceeds threshold {threshold}. The calculated scores do not match the expected formula."