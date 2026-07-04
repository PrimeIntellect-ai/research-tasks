You are investigating a regression in a legacy codebase located at `/home/user/regression_repo`. 

The team has reported that running `make test` recently started leaking background processes. Specifically, a background server listening on TCP port 8080 is no longer properly shut down after the test completes. This causes subsequent tests and deployments to fail due to port conflicts ("Address already in use").

We know the following:
1. The repository was working perfectly at the tag `v1.0`. At that commit, `make test` starts the service, tests it, and completely cleans up the background process listening on port 8080.
2. Sometime between `v1.0` and the current `HEAD`, a commit introduced a bug that prevents the process from being terminated at the end of `make test`.
3. If you run `make test` on a "bad" commit, the port remains bound after the command exits.

Your task is to identify the exact commit that introduced this regression.
Because a "bad" commit leaves the port bound, testing the *next* commit in a bisect process will falsely fail unless you ensure the port is freed before each test run. 

Write a bash script to automate this testing, and use `git bisect` to find the culprit. Once you have identified the first bad commit, save its full 40-character commit hash to the file `/home/user/leak_commit.txt`.

Ensure your automated bisect process cleans up port 8080 between tests so that "good" commits aren't falsely flagged as "bad" due to leftover processes from a previous step!