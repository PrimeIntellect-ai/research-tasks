# test_final_state.py

import os
import glob
import json
import pytest

def test_cython_extension_built():
    """
    Verify that the Cython aggregator was successfully built in-place.
    """
    base_dir = "/home/user/pipeline"
    # Cython builds typically produce files like fast_agg.cpython-38-x86_64-linux-gnu.so
    so_files = glob.glob(os.path.join(base_dir, "fast_agg*.so"))
    assert len(so_files) > 0, "Cython extension 'fast_agg' shared object (.so) file was not found in /home/user/pipeline/. Did you run setup.py build_ext --inplace?"

def test_faulty_sensor_identified():
    """
    Verify that the student correctly identified the faulty sensor from the log timeline.
    """
    faulty_sensor_file = "/home/user/pipeline/faulty_sensor.txt"
    assert os.path.exists(faulty_sensor_file), f"File missing: {faulty_sensor_file}"

    with open(faulty_sensor_file, "r") as f:
        content = f.read().strip()

    assert content == "SEN-8842", f"Incorrect faulty sensor ID. Expected 'SEN-8842', but got '{content}'."

def test_pipeline_output_generated():
    """
    Verify that the pipeline ran successfully and generated the valid JSON output,
    which implies the floating-point precision bug in processor.py was fixed.
    """
    output_file = "/home/user/pipeline/output/final_metrics.json"
    assert os.path.exists(output_file), f"Output file missing: {output_file}. The pipeline may have crashed or not been run."

    with open(output_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_file} does not contain valid JSON.")

    assert "SEN-1001" in data, "Key 'SEN-1001' is missing from the final JSON output."
    assert "SEN-8842" in data, "Key 'SEN-8842' is missing from the final JSON output. The precision bug might still be present."

    # Check that the metric was computed successfully as a float
    val_8842 = data["SEN-8842"]
    assert isinstance(val_8842, float) or isinstance(val_8842, int), f"Metric for SEN-8842 should be a number, got {type(val_8842)}"
    assert val_8842 > 0, "Metric for SEN-8842 is invalid. The variance computation may still be failing or returning zero."