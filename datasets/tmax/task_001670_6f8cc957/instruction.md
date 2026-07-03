You are a security researcher analyzing the source code of a suspicious Python tool recovered from a compromised machine. You have extracted the repository to `/home/user/suspicious_tool`. 

The malware author has made several changes over time, and the current state of the repository has a broken Python dependency configuration that prevents the environment from building. Furthermore, the author seems to have realized they accidentally leaked their Command & Control (C2) authentication token in an earlier commit and subsequently removed it from the code.

Your objectives are:

1. **Resolve Dependency Conflicts**: The `requirements.txt` file in `/home/user/suspicious_tool` currently contains conflicting version requirements. Fix the `requirements.txt` file so that `pip install -r requirements.txt` succeeds without errors. (Do not remove the packages, just adjust the versions to be compatible. You can upgrade or downgrade them as needed).
2. **Git Forensics**: Dig through the git history of the repository to recover the original C2 authentication token that was hardcoded in a previous commit.
3. **Construct a Regression Test**: Create a Python test file at `/home/user/test_c2_auth.py`. This file must:
   - Use the `pytest` framework.
   - Import the `check_c2_auth` function from `malware` (which is located in the `suspicious_tool` directory).
   - Contain a test function that asserts `check_c2_auth(token)` returns `True` when provided with the recovered secret token.

Ensure that running `pytest /home/user/test_c2_auth.py` (with the `suspicious_tool` directory in your PYTHONPATH) successfully executes and passes the test.