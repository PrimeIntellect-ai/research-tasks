You are an open-source maintainer reviewing a broken Pull Request (PR) for a lightweight Bash-based microservice. The contributor attempted to add a new schema migration endpoint but their tests are failing. 

The application code is located in `/home/user/app`.

Here are the issues with the PR that you need to fix:

1. **Broken URL Parameter Parsing:** The service uses `/home/user/app/router.sh` to route requests. The contributor added a `/api/migrate` route that requires a `target` query parameter (e.g., `/api/migrate?target=5`). However, their parameter parsing logic is flawed and assumes `target` is always the first parameter in the query string.
2. **Missing Test Fixtures:** The migration route checks for the existence of a base mock schema file at `/home/user/app/fixtures/schema_v1.json`, but the contributor forgot to commit this directory and file.
3. **Failing Tests:** There is a property-based test script at `/home/user/app/test.sh` that generates dozens of random URLs with randomized parameter orderings to test the router. It is currently failing because of the issues above.

Your task:
1. Fix the bug in `/home/user/app/router.sh` so that it correctly extracts the `target` parameter regardless of its position in the query string (e.g., it must work for `?foo=bar&target=10&baz=qux`).
2. Create the missing mock setup: a directory `/home/user/app/fixtures` and a file inside it named `schema_v1.json` containing exactly the JSON: `{"version": 1}`.
3. Ensure that running `/home/user/app/test.sh` completes successfully and prints "All tests passed."
4. Save the Git-compatible diff of your changes to `router.sh` into `/home/user/router.patch` using the `diff -u` command (compare the original broken script with your fixed version, e.g., by backing up the original first). 

Do not modify `test.sh`. All your work should be done in the `/home/user` environment.