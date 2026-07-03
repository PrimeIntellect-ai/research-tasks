# test_final_state.py

import os
import re
import subprocess
import pytest

def test_processor_exists():
    assert os.path.isfile("/home/user/processor.cpp"), "/home/user/processor.cpp is missing"
    assert os.path.isfile("/home/user/processor"), "/home/user/processor executable is missing"
    assert os.access("/home/user/processor", os.X_OK), "/home/user/processor is not executable"

def test_pipeline_script_exists():
    assert os.path.isfile("/home/user/run_pipeline.sh"), "/home/user/run_pipeline.sh is missing"
    assert os.access("/home/user/run_pipeline.sh", os.X_OK), "/home/user/run_pipeline.sh is not executable"

def test_processed_logs_content():
    expected_content = """timestamp_sec,masked_user_id,action,value
100,MASKED_100,LOGIN,1
108,MASKED_100,CLICK,5
115,MASKED_200,LOGIN,1
116,MASKED_200,LOGOUT,1
130,MASKED_300,LOGIN,1
140,MASKED_400,LOGIN,1
150,MASKED_500,LOGIN,1
160,MASKED_600,LOGIN,1
170,MASKED_700,LOGIN,1"""

    assert os.path.isfile("/home/user/processed_logs.csv"), "/home/user/processed_logs.csv is missing"

    with open("/home/user/processed_logs.csv", "r") as f:
        content = f.read().strip()

    assert content == expected_content, "/home/user/processed_logs.csv content does not match expected output"

def test_pipeline_log():
    assert os.path.isfile("/home/user/pipeline.log"), "/home/user/pipeline.log is missing"
    with open("/home/user/pipeline.log", "r") as f:
        content = f.read()
    assert "SUCCESS" in content, "/home/user/pipeline.log does not contain SUCCESS"

def test_crontab_schedule():
    assert os.path.isfile("/home/user/crontab.txt"), "/home/user/crontab.txt is missing"
    with open("/home/user/crontab.txt", "r") as f:
        content = f.read().strip()

    # Check for every 15 minutes schedule (*/15 * * * * or 0,15,30,45 * * * *)
    match = re.search(r'^(\*/15|0,15,30,45)\s+\*\s+\*\s+\*\s+\*\s+/home/user/run_pipeline\.sh$', content, re.MULTILINE)
    assert match is not None, "/home/user/crontab.txt does not have the correct every-15-min schedule for /home/user/run_pipeline.sh"

def test_quality_gate_logic(tmp_path):
    # Create a mock input with >20% duplicates
    mock_input = tmp_path / "mock_log.csv"
    mock_input.write_text("""timestamp_ms,user_id,action,value
100000,U100,LOGIN,1
101000,U100,LOGIN,1
102000,U100,LOGIN,1
103000,U100,LOGIN,1
""")
    mock_output = tmp_path / "mock_output.csv"

    # Run the processor
    result = subprocess.run(
        ["/home/user/processor", str(mock_input), "-o", str(mock_output)],
        capture_output=True,
        text=True
    )

    # Drop rate is 3/4 = 75% (>20%), so it should fail with exit code 2
    assert result.returncode == 2, "Processor did not exit with code 2 when drop rate > 20%"
    assert not mock_output.exists(), "Processor generated output file even when quality gate failed"