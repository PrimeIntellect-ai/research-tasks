You have inherited an unfamiliar codebase for a mathematical simulation project located at `/home/user/diffusion_sim`. The previous developer left abruptly, leaving the project in a broken state. Your goal is to fix the pipeline so it correctly generates the output file `/home/user/diffusion_sim/output/final_series.npy`.

Here is the situation:
1. **Deleted File Recovery**: The primary script `run_sim.py` expects a configuration file named `model_config.json` in the root of the repository. The previous developer accidentally deleted it and committed the deletion before leaving. You must recover its contents from the Git history.
2. **Corrupted Input**: The simulation reads initial state data from `/home/user/diffusion_sim/data/initial_states.csv`. A sensor glitch corrupted a few rows in this 10,000-row file with malformed strings. You must investigate and handle/remove these corrupted inputs so the simulation doesn't crash.
3. **Missing Parameters**: The developer left a screenshot of some handwritten notes at `/app/handover_notes.png`. You need to read this image to find the correct values for the critical parameters `kappa` and `tau`, and hardcode them into `run_sim.py` where indicated.
4. **Statistical Anomaly**: Once the simulation runs, you will notice that the output values exhibit a massive statistical anomaly (values exploding to infinity or `NaN`). You will need to use an interactive debugger or print statements to inspect `math_core.py`. There is a clear numerical instability bug in the `step_forward` function caused by a division operation that lacks a small epsilon `1e-8` to prevent division by zero, or an off-by-one index. Identify and fix the bug so the simulation remains stable.

Your task is complete when `python run_sim.py` runs successfully and writes the result to `/home/user/diffusion_sim/output/final_series.npy`. An automated test will compute the Mean Squared Error (MSE) between your output and the true expected output. 

Requirements:
- Do not modify the number of iterations in the simulation.
- Ensure the final output is saved exactly at `/home/user/diffusion_sim/output/final_series.npy`.
- You may install any tools needed to read the image (e.g., `tesseract-ocr`).