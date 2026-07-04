# test_final_state.py
import os
import pandas as pd
import numpy as np
from PIL import Image

def test_predictions_mse():
    preds_path = '/home/user/predictions.csv'
    test_path = '/home/user/test.csv'

    assert os.path.exists(preds_path), f"Predictions file not found at {preds_path}"

    test_df = pd.read_csv(test_path)
    preds_df = pd.read_csv(preds_path)

    assert 'id' in preds_df.columns, "Predictions missing 'id' column"
    assert 'prediction' in preds_df.columns, "Predictions missing 'prediction' column"

    # Compute true values
    true_vals = np.sin(test_df['featureA']) * 2.0 + np.cos(test_df['featureB']) * 3.0 + test_df['featureA'] * test_df['featureB']

    # Merge to align IDs
    merged = pd.merge(test_df[['id']], preds_df, on='id', how='left')

    assert not merged['prediction'].isna().any(), "Predictions contain missing values for some IDs"

    mse = np.mean((merged['prediction'] - true_vals)**2)

    assert mse < 0.05, f"MSE is {mse:.5f}, which is not < 0.05"

def test_plot_png_not_blank():
    plot_path = '/home/user/plot.png'
    assert os.path.exists(plot_path), f"Plot not found at {plot_path}"

    img = Image.open(plot_path).convert('RGB')
    extrema = img.getextrema()

    # extrema is a tuple of (min, max) for each band: ((Rmin, Rmax), (Gmin, Gmax), (Bmin, Bmax))
    # If min == max for all bands, the image is a single solid color (i.e. blank)
    is_solid = all(vmin == vmax for vmin, vmax in extrema)
    assert not is_solid, "The plot image appears to be completely blank (solid color). The plot script is likely still clearing the figure before saving."