# test_final_state.py

import os
import subprocess
import sys

def test_output_parquet_exists_and_schema():
    """Verify that the output parquet file exists and has the correct int64 schema."""
    parquet_path = '/home/user/output.parquet'
    assert os.path.exists(parquet_path), f"Output parquet file is missing: {parquet_path}"

    # We use subprocess to run pandas so we don't import third-party libraries directly in the test
    check_script = f"""
import pandas as pd
import sys

try:
    df = pd.read_parquet('{parquet_path}')
except Exception as e:
    print(f"Failed to read parquet file: {{e}}")
    sys.exit(1)

expected_columns = ['user_id', 'activity_score', 'feat1', 'feat2', 'feat3']
for col in expected_columns:
    if col not in df.columns:
        print(f"Missing column: {{col}}")
        sys.exit(1)
    if str(df[col].dtype) != 'int64':
        print(f"Column {{col}} has incorrect type: {{df[col].dtype}} (expected int64)")
        sys.exit(1)

# Verify that missing values were filled with 0 (user 104)
user_104 = df[df['user_id'] == 104]
if not user_104.empty:
    if user_104.iloc[0]['feat1'] != 0:
        print("Missing features for user 104 were not filled with 0.")
        sys.exit(1)

sys.exit(0)
"""
    result = subprocess.run([sys.executable, "-c", check_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Parquet validation failed:\n{result.stdout.strip()}\n{result.stderr.strip()}"

def test_similar_users_txt():
    """Verify that the similar_users.txt file exists and contains the correct users."""
    txt_path = '/home/user/similar_users.txt'
    assert os.path.exists(txt_path), f"Output file missing: {txt_path}"

    with open(txt_path, 'r') as f:
        content = f.read().strip()

    assert content, "The similar_users.txt file is empty."

    users = [u.strip() for u in content.split(',') if u.strip()]
    assert len(users) == 3, f"Expected exactly 3 similar users, but found {len(users)}: {users}"

    expected_users = {'101', '103', '105'}
    actual_users = set(users)
    assert actual_users == expected_users, f"Expected similar users {expected_users}, but got {actual_users}"