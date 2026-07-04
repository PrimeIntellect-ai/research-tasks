# test_final_state.py

import os
import subprocess
import pandas as pd
import pytest
from PIL import Image

def test_recall_metric():
    pred_path = '/home/user/top_100_similar.csv'
    truth_path = '/app/.hidden/truth.csv'

    assert os.path.exists(pred_path), f"Output file missing: {pred_path}"

    try:
        pred_df = pd.read_csv(pred_path)
    except Exception as e:
        pytest.fail(f"Could not read {pred_path} as CSV: {e}")

    assert 'user_id' in pred_df.columns, "Column 'user_id' is missing from the output CSV."
    assert 'similarity_score' in pred_df.columns, "Column 'similarity_score' is missing from the output CSV."

    assert os.path.exists(truth_path), f"Truth file missing: {truth_path}"
    truth_df = pd.read_csv(truth_path)

    pred_users = set(pred_df['user_id'].head(100).values)
    truth_users = set(truth_df['user_id'].values)

    intersection = len(pred_users.intersection(truth_users))
    recall = intersection / 100.0

    assert recall >= 0.95, f"Recall@100 is {recall}, which is below the threshold of 0.95."

def test_plot_script_fixes():
    script_path = '/app/scripts/generate_plot.py'
    plot_path = '/home/user/pca_plot.png'

    assert os.path.exists(script_path), f"Plotting script missing: {script_path}"

    # Remove the plot if it exists to ensure we are testing the script's output
    if os.path.exists(plot_path):
        os.remove(plot_path)

    # Run the script
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to run. Stderr: {result.stderr}"

    assert os.path.exists(plot_path), f"Plot image was not created at {plot_path} after running the script."

    try:
        img = Image.open(plot_path).convert('RGB')
    except Exception as e:
        pytest.fail(f"Could not open {plot_path} as an image: {e}")

    # Check if the image is entirely white or a single color (blank)
    extrema = img.getextrema()
    is_blank = all(min_val == max_val for min_val, max_val in extrema)

    assert not is_blank, "The generated plot image is completely blank (solid color). The script fix likely failed (e.g., plt.show() is still called before plt.savefig())."