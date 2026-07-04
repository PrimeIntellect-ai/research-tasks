You are a security researcher analyzing a suspicious quantitative trading binary that has been injected with a logic bomb. The binary processes numerical payload sequences. We have captured a sandbox execution of this binary, as well as a partial Python decompilation of its core mathematical engine.

Your objective is to build a payload sanitization tool that perfectly distinguishes between benign ("clean") payloads and malicious ("evil") payloads designed to trigger convergence failures and crash the trading system.

**Stage 1: Setup & Dependency Resolution**
Navigate to `/home/user/analysis_env`. You will find a `requirements.txt` containing conflicting versions of `numpy`, `scipy`, and `pandas` alongside an older analysis library. Resolve the dependency conflicts and install the environment so you can run the provided scripts.

**Stage 2: Video Extraction**
The binary relies on a proprietary 3-vector initialization seed. We do not have the binary itself, but we have a screen recording of its debug output during startup located at `/app/sandbox_run.mp4`. 
Use `ffmpeg` to extract the frames and locate the terminal output displaying the initialization vector `[v1, v2, v3]`. You will need these constants for your analysis.

**Stage 3: Algorithm Comprehension & Repair**
In `/home/user/analysis/decompiled_logic.py`, you will find the decompiled root-finding algorithm the binary uses to evaluate payloads. It currently suffers from a convergence failure (oscillation/division by zero) even on some benign inputs due to numerical instability in its Newton-Raphson implementation. Read the codebase, diagnose the mathematical flaw, and repair the convergence logic so it correctly reaches a stable root for benign data.

**Stage 4: Adversarial Classifier**
Write a Python script `/home/user/analysis/detector.py` that takes a directory path as a command-line argument:
`python3 /home/user/analysis/detector.py <path_to_corpus>`

The script must:
1. Initialize the repaired `decompiled_logic.py` using the 3-vector extracted from the video.
2. Iterate through all `.dat` files in the provided `<path_to_corpus>`.
3. Evaluate each payload. Clean payloads will converge to a root > 0. Evil payloads (the logic bomb triggers) will diverge or converge to a root <= 0.
4. Output a JSON file at `/home/user/analysis/verdict.json` with the exact format:
```json
{
  "payload1.dat": "clean",
  "payload2.dat": "evil"
}
```

An automated test suite will run your script against two hidden corpora to verify its accuracy. It must achieve perfect classification to pass.