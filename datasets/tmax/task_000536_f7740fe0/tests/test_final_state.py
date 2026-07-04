# test_final_state.py

import os
import csv

def test_pca_plot_exists():
    plot_file = '/home/user/pca_plot.png'
    assert os.path.exists(plot_file), f"The plot file {plot_file} does not exist."
    assert os.path.isfile(plot_file), f"{plot_file} is not a file."
    assert os.path.getsize(plot_file) > 0, f"The plot file {plot_file} is empty."

def test_output_csv_exists_and_format():
    output_file = '/home/user/output.csv'
    assert os.path.exists(output_file), f"The output file {output_file} does not exist."
    assert os.path.isfile(output_file), f"{output_file} is not a file."

    with open(output_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['PC1', 'PC2'], f"CSV header is incorrect. Expected ['PC1', 'PC2'], got {header}"

        rows = list(reader)
        assert len(rows) == 50, f"Expected 50 data rows in CSV, got {len(rows)}"

        # Check that values are floats and rounded to 4 decimal places (or at least valid numbers)
        for i, row in enumerate(rows):
            assert len(row) == 2, f"Row {i+1} does not have exactly 2 columns: {row}"
            try:
                pc1 = float(row[0])
                pc2 = float(row[1])
            except ValueError:
                assert False, f"Row {i+1} contains non-float values: {row}"

        # Check first row value to ensure correct imputation and PCA state
        first_row_pc1 = float(rows[0][0])
        assert abs(first_row_pc1 - (-0.4137)) < 0.05, f"PC1 value in first row is incorrect. Expected ~-0.4137, got {first_row_pc1}"

def test_script_modified_for_agg():
    script_file = '/home/user/etl_pipeline.py'
    assert os.path.exists(script_file), f"Script file {script_file} is missing."

    with open(script_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'Agg' in content or 'savefig' in content, "The script does not appear to use the Agg backend or savefig."
    assert 'plt.show()' not in content or content.startswith('#') or '#' in content.split('plt.show()')[0] or 'show()' not in content, "The script still contains an active plt.show() which will crash in a headless environment."