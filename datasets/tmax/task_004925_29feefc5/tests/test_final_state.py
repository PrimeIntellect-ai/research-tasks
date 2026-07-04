# test_final_state.py

import sys
import subprocess
import numpy as np
import pytest

def test_processor_accuracy():
    sys.path.insert(0, '/home/user/signal_port')
    try:
        from processor import process_signal
    except ImportError as e:
        pytest.fail(f"Failed to import process_signal from /home/user/signal_port/processor.py: {e}")

    np.random.seed(42)
    test_inputs = np.random.randint(-2000000000, 2000000000, size=50000, dtype=np.int32).tolist()

    try:
        agent_outputs = process_signal(test_inputs)
    except Exception as e:
        pytest.fail(f"process_signal raised an exception during execution: {e}")

    proc = subprocess.Popen(['/app/legacy_oracle'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    input_str = " ".join(map(str, test_inputs))
    oracle_stdout, _ = proc.communicate(input_str)
    oracle_outputs = [int(x) for x in oracle_stdout.split()]

    assert len(agent_outputs) == len(oracle_outputs), \
        f"Output lengths differ: agent returned {len(agent_outputs)} items, but oracle returned {len(oracle_outputs)}"

    matches = sum(1 for a, o in zip(agent_outputs, oracle_outputs) if a == o)
    accuracy = matches / len(oracle_outputs)

    assert accuracy >= 0.999, f"Accuracy too low. Expected >= 0.999, got {accuracy}"