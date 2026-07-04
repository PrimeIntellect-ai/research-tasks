You are an open-source maintainer reviewing a pull request for a Python API project located in `/home/user/project`. 

A contributor has submitted a patch (`/home/user/pr.patch`) that adds a new numerical algorithm and exposes it via a new API endpoint. However, the CI pipeline failed when testing the patch due to an import resolution error.

Your tasks are:
1. Apply the patch `/home/user/pr.patch` to the repository at `/home/user/project`.
2. Run the test suite using `pytest /home/user/project/test_api.py`. You will notice it fails to start due to a circular import introduced by the patch.
3. Fix the circular dependency. You should extract the shared `logger` component into `/home/user/project/utils.py` and update the imports in `api.py` and `math_ops.py` to import `logger` from `utils.py` instead of creating a cycle.
4. Ensure that the test suite passes successfully.
5. Create a file `/home/user/resolution.txt` containing the exact names of the files you modified to fix the bug, one per line (e.g., `api.py`, `math_ops.py`, `utils.py`).

Make sure your changes don't break the existing functionality and properly resolve the graph of dependencies between the modules.