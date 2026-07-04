# test_final_state.py

import os
import sys
import asyncio
import subprocess
import pytest

SERVICE_PATH = "/home/user/suspicious_service.py"
TEST_SCRIPT_PATH = "/home/user/regression_test.py"
PAYLOAD_PATH = "/home/user/payload.hex"

def test_regression_test_script():
    """Verify the regression test script exists, runs successfully, and prints PASS."""
    assert os.path.isfile(TEST_SCRIPT_PATH), f"Regression test script not found at {TEST_SCRIPT_PATH}"

    result = subprocess.run(
        [sys.executable, TEST_SCRIPT_PATH],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Regression test script failed with exit code {result.returncode}. Stderr: {result.stderr}"
    assert "PASS" in result.stdout, "Regression test script did not print 'PASS' to standard output."

@pytest.mark.asyncio
async def test_suspicious_service_fixes():
    """Verify the fixes applied to suspicious_service.py directly."""
    assert os.path.isfile(SERVICE_PATH), f"Service file not found at {SERVICE_PATH}"

    # Import the service module dynamically
    sys.path.insert(0, "/home/user")
    import suspicious_service

    # 1. Test format parsing (signedness) and convergence failure repair
    # Payload: ffffffff 01000000 00000000 -> a=-1, b=1, x0=0
    payload_bytes = bytes.fromhex("ffffffff0100000000000000")

    with pytest.raises(ValueError) as excinfo:
        await suspicious_service.handle_payload(payload_bytes)

    assert str(excinfo.value) == "Convergence failed", "Service did not raise ValueError('Convergence failed') on oscillation."

    # 2. Test cancellation handling
    # We will pass a payload that oscillates, but cancel it before 100 iterations (or just run it with a timeout)
    # Actually, we can just test if cancelling the task works and doesn't hang.
    async def run_and_cancel():
        task = asyncio.create_task(suspicious_service.handle_payload(payload_bytes))
        await asyncio.sleep(0.01) # let it start
        task.cancel()
        try:
            await asyncio.wait_for(task, timeout=0.5)
        except asyncio.CancelledError:
            return True
        except Exception:
            return False
        return False

    cancelled_properly = await run_and_cancel()
    assert cancelled_properly, "Task did not terminate properly upon cancellation (it may be swallowing CancelledError)."

    # 3. Test a converging input to ensure normal functionality works
    # a=0, b=-8, x0=2 => x^3 - 8 = 0 => root is 2
    # a=0 (00000000), b=-8 (f8ffffff), x0=2 (02000000)
    converging_payload = bytes.fromhex("00000000f8ffffff02000000")
    root = await suspicious_service.handle_payload(converging_payload)
    assert abs(root - 2.0) < 1e-4, f"Service failed to compute correct root for converging input. Got {root}, expected ~2.0"