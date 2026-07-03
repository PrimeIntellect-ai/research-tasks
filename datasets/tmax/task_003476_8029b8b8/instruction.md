You are a mobile build engineer maintaining a lightweight CI/CD pipeline. To minimize container footprints, your team is removing Python from the build environment. 

We have a legacy Python script, `/home/user/pipeline/topo.py`, which performs a topological sort on our C project's build dependency graph (`/home/user/pipeline/deps.txt`). The output is used by our Makefile to determine the correct object file linking order. Without the correct order, the project fails to link due to missing symbols.

Your task:
1. Translate the graph traversal and topological sort logic from `/home/user/pipeline/topo.py` into a pure Bash script named `/home/user/pipeline/topo.sh`. Standard utilities like `awk`, `sed`, or `grep` are permitted, but you cannot use Python, Perl, or other higher-level scripting languages.
2. The output format of `topo.sh` must exactly match `topo.py` (a single line of space-separated module names in the correct linking order).
3. Make sure `/home/user/pipeline/topo.sh` is executable.
4. Run `make test` in the `/home/user/pipeline/` directory. This will use your new `topo.sh` script to resolve the build dependency order, compile the mock C project, and write the execution output to `/home/user/pipeline/test_results.log`.

Do not modify the `Makefile`, the `.c` files, or `deps.txt`. Your objective is complete when `/home/user/pipeline/test_results.log` is successfully generated and contains the correct execution output.