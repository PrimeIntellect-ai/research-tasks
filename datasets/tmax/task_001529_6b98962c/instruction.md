You are a platform engineer responsible for maintaining our CI/CD pipelines. We have a Python utility in our pipeline that evaluates incoming deployment webhooks and determines if dependent services require a schema migration. The project is located in `/home/user/pipeline`.

Currently, the utility is failing its end-to-end orchestration tests. There are a few bugs in `/home/user/pipeline/version_checker.py` related to semantic version comparison, URL parameter parsing, and our custom dependency graph data structure.

Here is how the system is supposed to work:
1. The script reads a list of webhook URLs from `webhooks.txt`. Each URL is formatted like `http://ci.internal/deploy?service=<name>&version=<semver>`.
2. The script extracts the `service` and `version` (formatted as `X.Y.Z`).
3. It compares the new version against the current version stored in `registry.json`.
4. Using our custom `DependencyGraph` data structure, it checks all services that *depend* on the updated service.
5. **Schema Migration Rule:** A dependent service requires a schema migration if the updated service introduces a **Major** version bump (New Major > Old Major), OR if the updated service introduces a **Minor** version bump of **more than 2** (New Minor - Old Minor > 2). Patch version bumps never trigger schema migrations.
6. The script must output the names of all dependent services that require a schema migration to `/home/user/pipeline/migration_plan.txt`, sorted alphabetically, one service per line.

The current implementation has the following issues:
- The URL parameter parsing is poorly implemented and fails to correctly extract the version from the query string.
- The semantic version comparison incorrectly compares versions as strings (e.g., "10" is evaluated as less than "2"), causing mathematical errors in calculating the version diffs.
- The Makefile is set up to run `make test` which checks if `migration_plan.txt` is correct, but it currently fails.

Your task:
1. Fix the bugs in `/home/user/pipeline/version_checker.py`.
2. Run `make test` in `/home/user/pipeline` to ensure your fixes are correct.
3. Ensure the final `/home/user/pipeline/migration_plan.txt` is successfully generated and correct.