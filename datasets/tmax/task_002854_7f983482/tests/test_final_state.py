# test_final_state.py

import os
import json
import subprocess
import sys
from decimal import Decimal

def test_solution_json_correctness():
    """Verify that solution.json has the correct structure and values."""
    solution_path = "/home/user/solution.json"
    assert os.path.exists(solution_path), f"{solution_path} does not exist."

    with open(solution_path, "r") as f:
        try:
            sol = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{solution_path} contains invalid JSON."

    assert "crash_tx_id" in sol, "solution.json missing 'crash_tx_id' key."
    assert "precise_tax_value" in sol, "solution.json missing 'precise_tax_value' key."

    # The expected TX ID is derived from checking the sysdump.bin or transactions.txt
    expected_tx_id = "TX-8374-ERR"
    assert sol["crash_tx_id"] == expected_tx_id, f"Incorrect crash_tx_id: {sol['crash_tx_id']}."

    # The expected tax value is derived from the large float value * 0.05
    expected_tax = str(Decimal('9007199254740995.05') * Decimal('0.05'))
    assert sol["precise_tax_value"] == expected_tax, f"Incorrect precise_tax_value: {sol['precise_tax_value']}."

def test_processor_fixes():
    """Verify that processor.py has been fixed to handle trailing commas and precision loss."""
    processor_path = "/home/user/processor.py"
    assert os.path.exists(processor_path), f"{processor_path} does not exist."

    # Add /home/user to sys.path to import processor
    sys.path.insert(0, "/home/user")
    try:
        import processor
    except ImportError:
        assert False, "Failed to import processor.py."

    assert hasattr(processor, "process_tx"), "processor.py missing process_tx function."

    # Test with the exact raw line from transactions.txt
    raw_line = 'TX-8374-ERR|{"amount": 9007199254740995.05, "currency": "USD", }'

    try:
        result = processor.process_tx(raw_line)
    except Exception as e:
        assert False, f"process_tx failed to handle the edge-case line: {e}"

    assert result is not None, "process_tx returned None for a valid transaction."
    assert len(result) == 3, f"process_tx should return a tuple of length 3, got {len(result)}."

    tx_id, amount, tax = result
    assert tx_id == "TX-8374-ERR", f"process_tx returned incorrect tx_id: {tx_id}."

    # Check that Decimal was used to preserve precision
    assert isinstance(amount, Decimal), f"Amount should be a Decimal, got {type(amount)}."
    assert isinstance(tax, Decimal), f"Tax should be a Decimal, got {type(tax)}."

    expected_amount = Decimal('9007199254740995.05')
    expected_tax = expected_amount * Decimal('0.05')

    assert amount == expected_amount, f"process_tx returned incorrect amount: {amount}."
    assert tax == expected_tax, f"process_tx returned incorrect tax: {tax}."

def test_mre_script():
    """Verify that mre.py exists and runs successfully."""
    mre_path = "/home/user/mre.py"
    assert os.path.exists(mre_path), f"{mre_path} does not exist."

    # Run the MRE script
    try:
        result = subprocess.run(
            [sys.executable, mre_path],
            capture_output=True,
            text=True,
            check=True,
            cwd="/home/user"
        )
    except subprocess.CalledProcessError as e:
        assert False, f"mre.py failed to execute. Stderr: {e.stderr}"

    output = result.stdout.strip()
    assert "TX-8374-ERR" in output, "mre.py output does not contain the expected TX ID."
    assert "450359962737049.7525" in output, "mre.py output does not contain the precise tax value."