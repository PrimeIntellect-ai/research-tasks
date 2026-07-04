You are a Machine Learning Engineer preparing a curated dataset of biological sequence alignments to train a new foundation model. The data is generated from a simulation pipeline that sometimes produces non-reproducible or corrupted results due to floating-point reduction order issues and numerical instability.

You have two tasks to complete:

**Part 1: Adversarial Data Sanitizer**
You need to write a Bash script that acts as a strict filter for the training data files. 
Create the script at `/home/user/sanitize.sh`. It must take exactly one argument (the path to a data file) and use exit codes to accept or reject the file:
- Exit with code `0` if the file is CLEAN (valid).
- Exit with code `1` if the file is EVIL (corrupted/invalid).

Each data file is a text file with the following format:
```text
Total_Score: <float>
Alignment 1: Primer=<sequence> Target=<sequence> Score=<float>
Alignment 2: Primer=<sequence> Target=<sequence> Score=<float>
...
```

A file is considered EVIL (reject with exit code 1) if ANY of the following are true:
1. **Numerical Instability**: The sum of all individual `Score` values on the Alignment lines differs from the `Total_Score` on the first line by more than `0.001` (absolute difference). This indicates a floating-point reduction error during the simulation.
2. **Invalid Values**: Any of the scores (Total_Score or individual scores) are `NaN`, `Inf`, or `-Inf`.
3. **Primer Design Constraints**: Any of the `Primer` sequences have a length less than 15 characters or greater than 30 characters.

Otherwise, the file is CLEAN (accept with exit code 0). 
*Note: Your script will be tested against a hidden adversarial corpus of clean and evil files to ensure 100% accuracy.*

**Part 2: Visual Convergence Analysis**
A rendering of a long-running simulation is available at `/app/data/convergence_sim.mp4`. Due to numerical explosion, the simulation crashes at a specific point, which is visualized in the video by the entire frame suddenly dropping to completely black (brightness/luma drops to 0).
Use `ffmpeg` (which is pre-installed) to analyze the video and find the exact integer second where the video first turns completely black.
Write only this integer value (e.g., `42`) to a file named `/home/user/crash_time.txt`.

Ensure your bash script is executable (`chmod +x /home/user/sanitize.sh`). You can use standard Linux tools (awk, grep, bc, etc.) within your bash script.