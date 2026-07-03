You are a build engineer responsible for modernizing a company's artifact management pipeline. We are currently deprecating our old Node.js tooling in favor of a Python-based ecosystem.

Your task is to translate a legacy JavaScript hashing utility into Python, set up a local testing pipeline, and execute it to generate a manifest for our build artifacts.

Here are your detailed instructions:

1. **Code Translation (Algorithm)**:
   - There is a legacy Node.js script located at `/home/user/legacy/artifact_hasher.js`. It calculates a unique "Bundle Hash" for a given directory of files by sorting them alphabetically, computing their individual SHA256 hashes, concatenating those hex strings, and returning the SHA256 hash of the concatenated string.
   - Write a new Python tool at `/home/user/build_tools/artifact_hasher.py` that implements this exact same algorithm. 
   - The Python script must accept a directory path via the `--dir` argument (using `argparse`) and print *only* the final bundle hash hex string to standard output. Ignore subdirectories (only process files).

2. **Test Orchestration**:
   - Write a `pytest` test suite at `/home/user/build_tools/test_hasher.py`. 
   - This suite must contain at least one end-to-end test that creates a temporary directory, writes two dummy files to it, runs the hashing logic, and asserts the correct output.
   - You may install `pytest` using pip in your environment.

3. **CI/CD Pipeline Script**:
   - Create a bash script at `/home/user/ci_pipeline.sh`.
   - The script must use `set -e` to fail fast.
   - It must first run your `pytest` test suite: `python3 -m pytest /home/user/build_tools/test_hasher.py`.
   - If the tests pass, it must execute your Python utility against the `/home/user/artifacts` directory: `python3 /home/user/build_tools/artifact_hasher.py --dir /home/user/artifacts`.
   - It must capture the stdout of the utility and save the exact hex string into a file located at `/home/user/artifacts/bundle.manifest`.

Ensure all files have the correct permissions. Once you have written everything, run your pipeline script `/home/user/ci_pipeline.sh` so that the `bundle.manifest` is generated.