You are tasked with building a deterministic Bayesian updating pipeline that processes video telemetry and environmental data to predict chemical reaction activity.

We have a top-down video of a reaction vat, `/app/reaction.mp4`, and a corresponding environmental log, `/app/conditions.csv`.

Your objectives are:
1. **Video ETL Pipeline:**
   - Extract frames from `/app/reaction.mp4` at exactly 1 frame per second. Use the following command to ensure deterministic extraction:
     `mkdir -p /tmp/frames && ffmpeg -i /app/reaction.mp4 -r 1 -f image2 /tmp/frames/frame_%04d.png`
   - For each extracted frame (starting with `frame_0001.png` corresponding to second `0`), open it using Python's `PIL.Image`.
   - Extract the red channel.
   - Calculate the sum of the pixel values in the center 10x10 region (pixels `x: 100 to 109`, `y: 100 to 109`, assuming the video is at least 200x200).
   - If the sum is strictly greater than `12000`, the reaction is considered "active" (value `1`). Otherwise, "inactive" (value `0`).

2. **Data Joining:**
   - Read `/app/conditions.csv` which has headers `second,temperature`.
   - Join your active/inactive observations with this CSV based on the `second` (where `frame_0001.png` is second `0`, `frame_0002.png` is second `1`, etc.).

3. **Bayesian Inference Modeling:**
   - We model the probability of the reaction being active, $\theta$, using a Beta-Bernoulli conjugate model.
   - We stratify the model into two regimes based on temperature:
     - **High Temperature Regime:** temperature >= 20.0
     - **Low Temperature Regime:** temperature < 20.0
   - Start with a uniform prior $Beta(\alpha=1, \beta=1)$ for both regimes.
   - Perform an exact Bayesian update using your joined historical observations to compute the posterior parameters ($\alpha_{H}, \beta_{H}$) and ($\alpha_{L}, \beta_{L}$).

4. **Predictive Fuzz Target:**
   - Create a Python script at `/home/user/update_model.py`.
   - This script must read a single line of JSON from standard input, representing a new batch of streaming observations.
     Example input: `{"temp": 22.1, "obs": [1, 1, 0]}`
   - The script must:
     1. Determine the correct regime (High or Low) based on the input `temp`.
     2. Use the historical posterior for that regime (which you computed in step 3) as the *new prior*.
     3. Perform a Bayesian update using the array of `obs` (where 1 is active, 0 is inactive).
     4. Output a single JSON string to standard output with the final posterior parameters.
     Example output: `{"alpha": 17, "beta": 5}`
   - Your script must be robust, fast, and deterministic, as it will be rigorously tested against an exact oracle via randomized fuzzing.

Ensure your code handles numerical precision correctly (integers for Beta parameters) and matches the expected JSON formatting exactly.