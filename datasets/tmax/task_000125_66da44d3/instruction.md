You are tasked with migrating a legacy numerical state machine. The original implementation was written in Python 2, but we need to port the logic to a pure Bash script for our new lightweight build system.

Unfortunately, the original source code we recovered, `/app/legacy/machine.py`, is incomplete—the initial seed value `INIT_VAL` was stored in a separate configuration file that has been lost. However, the original developer left behind a screen recording of a test run at `/app/legacy/demo.mp4`. In the first few seconds of this video, the terminal output clearly prints the `INIT_VAL` that was used.

Your objectives are:
1. **Analyze the Video**: Use `ffmpeg` and OCR tools (like `tesseract`, which is installed in the environment) to extract frames from `/app/legacy/demo.mp4` and identify the integer value of `INIT_VAL`.
2. **Understand the State Machine**: Review `/app/legacy/machine.py` to understand how the state machine processes input strings and mutates the numerical value.
3. **Implement in Bash**: Create a standalone Bash script at `/home/user/machine.sh`. 
   - It must take exactly one argument: a string of characters (e.g., `AABBCCA`).
   - It must initialize the value using the `INIT_VAL` you extracted.
   - It must perfectly replicate the state transitions and numerical operations of the Python 2 script.
   - It must print the final numerical value to standard output (and nothing else).
   - Ensure the script is executable (`chmod +x`).

An automated verifier will strictly test your `/home/user/machine.sh` against a hidden reference oracle using hundreds of random input strings to ensure bit-exact equivalence. Every state transition and modulo arithmetic operation must be perfectly faithful to the original logic.