You are a developer tasked with diagnosing an intermittent regression in a Python-based query engine.

The repository is located at `/home/user/data_engine`. It contains approximately 200 commits. 
The latest commit (`HEAD`, also tagged as `v2.0`) has a known issue where `python test_query.py` occasionally fails and exits with a non-zero status. The initial release, tagged as `v1.0`, is completely stable and passes the test 100% of the time.

Your investigation has revealed the following:
1. The bug causes a query result to occasionally return empty, leading to a build/test failure.
2. The failure is intermittent—it fails roughly 30-50% of the time on the affected commits.
3. You need to perform a root cause analysis using bisection to find the *first bad commit* that introduced this intermittent failure.

Your task:
1. Use `git bisect` (or a custom bisection approach) to find the exact commit that introduced the bug. Keep in mind that a single successful run of `python test_query.py` does NOT guarantee the commit is good, due to the intermittent nature of the bug. You may need to wrap the test execution to run it multiple times per commit.
2. Once you have identified the precise 40-character SHA hash of the first bad commit, save this hash to a file located at `/home/user/bad_commit_hash.txt`.

The file `/home/user/bad_commit_hash.txt` should contain ONLY the 40-character git commit hash (and an optional newline). No other text.