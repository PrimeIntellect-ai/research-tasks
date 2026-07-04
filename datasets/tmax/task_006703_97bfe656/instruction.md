You are an IT Support Technician acting on a high-priority ticket from the Mathematical Modeling Team. Their data transformation pipeline is broken, and they need it fixed immediately. 

Ticket Details:
"Our Python data transformation pipeline crashed overnight. It left a raw memory dump file, and now we can't even get the environment to build due to dependency conflicts. Even when we force-installed packages previously, the output matrix didn't match our expected baseline. We need someone to debug this end-to-end."

Here are the specific tasks you need to complete to resolve this ticket:

1. **Memory Dump Analysis:**
   The modeling script crashed and dumped memory to `/home/user/crash.dmp`. Deep inside this binary file is the critical math configuration string that was in memory at the time of the crash. 
   - Extract the scaling factor from the dump. You are looking for a string in the format: `CONFIG_SCALE_FACTOR=<number>`.

2. **Dependency Conflict Resolution:**
   The team's Python environment dependencies are listed in `/home/user/pipeline/requirements.txt`. 
   - Currently, `pip install -r /home/user/pipeline/requirements.txt` fails because of a version conflict between `scipy` and `numpy`.
   - The team requires `scipy==1.7.3`. You must find and set a compatible `numpy` version (e.g., downgrading numpy so it works with this older scipy without compilation errors or PIP solver failures) in the `requirements.txt` file.
   - Create a virtual environment at `/home/user/math_env` and install the fixed requirements successfully.

3. **Data Transformation Diff Analysis & Code Fixing:**
   - The pipeline script is located at `/home/user/pipeline/transform.py`.
   - Update the script to use the `CONFIG_SCALE_FACTOR` you extracted from the memory dump.
   - Run the script using your virtual environment. It will read `/home/user/pipeline/input.csv` and generate an output.
   - Compare the output to `/home/user/pipeline/expected_output.csv`. The current math logic in `transform.py` is applying operations in the wrong order or using the wrong operations, resulting in a mathematical diff.
   - Debug and modify `transform.py` so that its output exactly matches `expected_output.csv`.
   - Save the corrected script output to `/home/user/pipeline/final_output.csv`.

4. **Resolution Logging:**
   Create a file at `/home/user/ticket_resolution.log` with exactly two lines:
   - Line 1: The exact `CONFIG_SCALE_FACTOR` value extracted from the memory dump (just the number).
   - Line 2: The exact `numpy` version you specified in `requirements.txt` to resolve the conflict.

Ensure all files are created in the exact locations specified. You have full access to the terminal to use bash commands, python, and standard debugging tools.