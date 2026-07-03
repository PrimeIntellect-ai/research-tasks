# test_final_state.py
import os

def test_rolling_latency_output():
    """Test that the output CSV file is created and contains the correctly computed rolling aggregations."""
    output_path = "/home/user/rolling_latency.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did the script run successfully?"

    with open(output_path, 'r') as f:
        actual = f.read().strip()

    expected = """interval_ts,count,avg_lat,mavg_30s
1600000000,2,15.00,15.00
1600000010,0,0.00,15.00
1600000020,1,50.00,26.67
1600000030,2,150.00,116.67
1600000040,0,0.00,116.67
1600000050,0,0.00,150.00
1600000060,1,10.00,10.00"""

    actual_lines = actual.split('\n')
    expected_lines = expected.split('\n')

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in CSV, got {len(actual_lines)}. "
        f"Ensure all intervals from min to max are included, including empty ones."
    )

    for i, (act, exp) in enumerate(zip(actual_lines, expected_lines)):
        assert act.strip() == exp.strip(), (
            f"Mismatch on line {i+1} of {output_path}:\n"
            f"Expected: {exp}\n"
            f"Got:      {act}\n"
            f"Check your rolling aggregation logic and decimal formatting."
        )