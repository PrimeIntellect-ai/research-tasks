You are an open-source maintainer reviewing a Pull Request (PR) for a custom build orchestration tool called `dep-graph-parser`. 

The tool is written in C and uses a state machine to parse a custom dependency graph format (`.deps`). 
Recently, a contributor submitted a patch (`/home/user/pr_123.patch`) to add a "Rate Limiting" feature. This feature allows targets to specify a maximum concurrent job limit using parentheses, like this:
`target_name(limit): dep1 dep2;`

However, the contributor noted that their patch is broken. While it successfully compiles, parsing a target with a rate limit results in corrupted target names or parsing failures. 

Your task:
1. Navigate to `/home/user/project/` and apply the patch file `/home/user/pr_123.patch` to `parser.c`.
2. Analyze the state machine in `parser.c` and fix the bug introduced by the PR. The parser must correctly extract the target name, the limit (if provided), and the dependencies. If no limit is provided, the limit defaults to `0`.
3. Create a test file at `/home/user/project/tests/pr_test.deps` with the following exact content:
```
web_server(10): db_client auth_module;
db_client(5): network_lib;
auth_module: crypto_lib;
```
4. Build the project using the provided `Makefile` in `/home/user/project/`.
5. Run the compiled parser against your new test file and redirect the output to `/home/user/verification.log`.
   Command to run: `./parser tests/pr_test.deps > /home/user/verification.log`

The expected correct output in `/home/user/verification.log` for the test file should be exactly:
```
Target: web_server, Limit: 10, Deps: db_client auth_module
Target: db_client, Limit: 5, Deps: network_lib
Target: auth_module, Limit: 0, Deps: crypto_lib
```

Fix the C code, build it, and generate the verification log.