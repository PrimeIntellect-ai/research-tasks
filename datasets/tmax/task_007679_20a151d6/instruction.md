You are an open-source maintainer reviewing a broken PR for your Python project's dependency resolution module.

A contributor submitted a patch to add circular dependency detection to your Directed Acyclic Graph (DAG) resolver. However, their email client heavily mangled the file. The patch was saved to your server at `/home/user/pr_submission.b64`.

It appears the file is Base64-encoded. Furthermore, the decoded bytes represent text encoded in **UTF-16LE**, not standard UTF-8.

Your tasks are to:
1. Decode `/home/user/pr_submission.b64` from Base64.
2. Convert the resulting decoded bytes from UTF-16LE to standard UTF-8. Save this as a valid patch file.
3. Apply the patch to `/home/user/project/dag.py`.
4. Install `pytest` and run the tests in `/home/user/project/test_dag.py`. You will notice that the test suite fails.
5. Analyze the modified `dag.py`. The contributor introduced a bug in their graph traversal logic. Specifically, their depth-first search (DFS) algorithm incorrectly flags legitimate diamond-shaped dependency graphs as circular dependencies because it fails to properly manage the recursion stack state. Fix this bug in `dag.py`.
6. Run `pytest /home/user/project/test_dag.py` again to ensure all tests pass.
7. Once all tests pass, create a file at `/home/user/success.log` containing exactly the string: `ALL TESTS PASSED`.

Constraints & Guidelines:
- The project files are located in `/home/user/project`.
- Do not modify `test_dag.py`. You must only modify `dag.py`.
- Do not bypass the testing process; your final fix must pass the provided test suite.