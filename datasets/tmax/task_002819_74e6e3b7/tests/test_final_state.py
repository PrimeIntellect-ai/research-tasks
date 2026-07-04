# test_final_state.py
import subprocess
import time
import re
import os
import signal

def test_variance_mse():
    # Ensure no previous instances are running from manual testing
    subprocess.run(['pkill', '-f', 'sensor_sim.py'])
    subprocess.run(['pkill', '-f', 'aggregator.py'])

    # Start services
    process = subprocess.Popen(['bash', '/home/user/app/start_services.sh'], preexec_fn=os.setsid)
    try:
        # Wait 5 seconds for the aggregator to consume the stream and process batches
        time.sleep(5)

        # Run the end-to-end test script
        result = subprocess.run(['python3', '/home/user/app/run_e2e_test.py'], capture_output=True, text=True)
        output = result.stdout + result.stderr

        # Extract the Mean Squared Error (MSE) metric
        match = re.search(r"MSE:\s+([0-9\.eE+-]+)", output)
        assert match is not None, f"Could not find MSE in the output of run_e2e_test.py. Script output:\n{output}"

        mse = float(match.group(1))

        # Assert against the metric threshold
        assert mse <= 1e-6, f"MSE is {mse}, which is greater than the threshold of 1e-6. The variance calculation is still numerically unstable or incorrect."
    finally:
        # Clean up background processes
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        except Exception:
            pass
        subprocess.run(['pkill', '-f', 'sensor_sim.py'])
        subprocess.run(['pkill', '-f', 'aggregator.py'])