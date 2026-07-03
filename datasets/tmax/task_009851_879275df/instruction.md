You are an engineer setting up a build and CI system for a new Python project called `polybuild` located in `/home/user/polybuild`. The project is intended to replace an old C library with a pure Python implementation, but the migration is incomplete. 

Your tasks are as follows:

1. **Code Translation & Data Structure Design**:
   In `/home/user/polybuild/legacy/ring_buffer.c`, there is a C implementation of a ring buffer (circular queue) that overwrites the oldest data when full. 
   Translate this data structure into a Python class named `RingBuffer` and place it in `/home/user/polybuild/src/polybuild/ring_buffer.py`. 
   The Python class must have the following methods:
   - `__init__(self, size: int)`
   - `push(self, data: int) -> None` (overwrites oldest if full)
   - `pop(self) -> int` (raises `IndexError("Buffer is empty")` if empty)

2. **Fix the Build System**:
   The `/home/user/polybuild/pyproject.toml` file is currently broken and incomplete. Fix it so that it correctly defines a standard `setuptools` build system and packages the `polybuild` module located in the `src/` directory. Ensure the package name is `polybuild` and the version is `0.1.0`.

3. **CI/CD Pipeline & Test Orchestration**:
   Create a bash script at `/home/user/polybuild/ci_pipeline.sh` that performs the following end-to-end pipeline steps:
   - Activates a virtual environment (you may create one locally in `/home/user/polybuild/venv` if it doesn't exist, or just install directly if you prefer, but ensure isolation isn't strictly necessary if it's the only package, but standard practices apply).
   - Installs the `polybuild` package from the local source directory using `pip`.
   - Runs a Python command to test the `RingBuffer`. Specifically, it must test that pushing 3 items into a buffer of size 2, then popping once, returns the second pushed item (since the first was overwritten).
   - If the build, installation, and test all succeed (exit code 0), the bash script must write the exact string `CI_SUCCESS: polybuild pipeline passed` to `/home/user/polybuild/ci_status.log`. If any step fails, it should write `CI_FAILURE` to the log and exit.

Make sure the bash script is executable. You do not need to run the bash script yourself, but you must ensure all files are correctly written and configured.