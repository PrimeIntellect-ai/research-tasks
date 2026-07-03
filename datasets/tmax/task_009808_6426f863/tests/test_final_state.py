# test_final_state.py
import os
import csv
import math

def test_ci_file_content():
    """Verify that the calculated CI matches the expected deterministic output."""
    users_file = '/home/user/users.csv'
    transactions_file = '/home/user/transactions.csv'
    ci_file = '/home/user/ci.txt'

    assert os.path.exists(users_file), f"Missing {users_file}"
    assert os.path.exists(transactions_file), f"Missing {transactions_file}"
    assert os.path.exists(ci_file), f"Missing {ci_file} - did your C program run and generate it?"

    # Read and join data
    users = {}
    with open(users_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            users[row['user_id']] = row['group']

    data = []
    with open(transactions_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = row['user_id']
            if uid in users:
                data.append((int(uid), users[uid], float(row['amount'])))

    # Sort by user_id to ensure deterministic order matching the expected C implementation
    data.sort(key=lambda x: x[0])
    data = [(x[1], x[2]) for x in data]
    N = len(data)

    # Custom PRNG matching the C implementation
    state = 42
    def xorshift32():
        nonlocal state
        state ^= (state << 13) & 0xFFFFFFFF
        state ^= (state >> 17) & 0xFFFFFFFF
        state ^= (state << 5) & 0xFFFFFFFF
        return state

    diffs = []
    for _ in range(10000):
        # Draw N indices
        indices = [xorshift32() % N for _ in range(N)]
        sample = [data[i] for i in indices]

        amounts = [x[1] for x in sample]
        mean_amt = sum(amounts) / N
        var_amt = sum((x - mean_amt)**2 for x in amounts) / N
        std_amt = math.sqrt(var_amt)

        if std_amt == 0:
            std_amt = 1e-9

        sum_A = 0.0
        count_A = 0
        sum_B = 0.0
        count_B = 0

        for grp, amt in sample:
            z = (amt - mean_amt) / std_amt
            if grp == 'A':
                sum_A += z
                count_A += 1
            else:
                sum_B += z
                count_B += 1

        mean_z_A = sum_A / count_A if count_A > 0 else 0.0
        mean_z_B = sum_B / count_B if count_B > 0 else 0.0

        diffs.append(mean_z_B - mean_z_A)

    # Calculate percentiles
    diffs.sort()
    lower = diffs[250]
    upper = diffs[9749]

    expected_content = f"{lower:.4f},{upper:.4f}"

    with open(ci_file, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The contents of {ci_file} do not match the expected values.\n"
        f"Expected: '{expected_content}'\n"
        f"Actual:   '{actual_content}'\n"
        "Ensure you are using the correct PRNG, standardizing *within* the bootstrap loop, "
        "and formatting the output exactly as requested."
    )