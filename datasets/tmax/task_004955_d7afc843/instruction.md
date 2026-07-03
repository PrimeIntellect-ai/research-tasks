You are an IT support technician responding to an escalated ticket from the computer vision team. 

**Ticket Details:**
"Our motion analysis script `/home/user/analyze_motion.py` is failing. It analyzes a video feed located at `/app/sensor_feed.mp4` to track a target, applies calibration parameters from our local database `/home/user/calibration.db`, and computes a rolling variance of the X-coordinate of the tracked target over a window of 30 frames. 

However, we are seeing two major issues:
1. The rolling variance values are wildly inaccurate, sometimes even evaluating to negative numbers! We suspect this is due to a numerical instability or floating-point precision issue in how the variance is calculated.
2. The script seems to be using the wrong calibration offset. It should be fetching the 'active' configuration from the database, but it looks like it's grabbing an old decommissioned row.

Please fix the script so that it calculates the rolling variance accurately and uses the correct active calibration."

**Your Goal:**
1. Debug and repair `/home/user/analyze_motion.py`.
2. Fix the database query so it retrieves the row from the `configs` table where `is_active = 1`. The script adds the `offset_x` value from this row to the X-coordinate before calculating the variance.
3. Fix the numerical instability in the rolling variance calculation. The current naive implementation suffers from catastrophic cancellation because it operates in `float32` and the offset values are very large. You must implement a numerically stable approach (e.g., Welford's algorithm, or simply using high-precision double floats and proper centering).
4. Run your fixed script. It should produce an output file at `/home/user/variance_output.csv` with the headers `frame_idx,variance`.

The automated verifier will compare your `/home/user/variance_output.csv` against a ground-truth reference using Mean Squared Error (MSE).