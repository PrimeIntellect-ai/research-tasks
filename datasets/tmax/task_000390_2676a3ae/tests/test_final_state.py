# test_final_state.py
import os
import difflib

def test_decoded_output_accuracy():
    truth_text = "OPTICAL_SYNC_ESTABLISHED: Hello minimal container environment! The state machine works."
    output_file = "/home/user/decoded_output.txt"

    assert os.path.exists(output_file), f"Output file {output_file} does not exist. The agent failed to create the decoded output."

    with open(output_file, "r") as f:
        agent_text = f.read().strip()

    ratio = difflib.SequenceMatcher(None, truth_text, agent_text).ratio()

    assert ratio >= 0.95, f"Accuracy metric failed. Expected ratio >= 0.95, got {ratio:.4f}. Agent text: {agent_text!r}"