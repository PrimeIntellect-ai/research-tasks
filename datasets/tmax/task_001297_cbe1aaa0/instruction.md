You are a release manager preparing a deployment for a legacy C project. The project is located in `/home/user/project`. 

Currently, when you run `make` in that directory, the build fails with linker errors (`undefined reference`). This is because the static libraries are linked in the wrong order in the `Makefile`. 

There is a `deps.json` file in the directory that defines the dependency graph of the modules. For the GNU linker, if library A depends on library B, `-lA` must appear *before* `-lB` in the gcc command.

Your task is to:
1. Analyze `deps.json` to resolve the correct topological dependency order.
2. Fix the linker command in the `Makefile` (the `app:` target) so that the `app` executable builds successfully. Run `make` to compile it.
3. Write a Python integration test script at `/home/user/project/test_deploy.py`. This script must:
   - Execute the compiled `./app` binary.
   - Capture its standard output.
   - If the output exactly matches `"Result: 44\n"`, the script must write the string `DEPLOY_READY` to a file at `/home/user/project/status.log`.
   - **Crucially**, `status.log` must be encoded in `UTF-16LE` (Little Endian).
4. Set up a basic GitHub Actions CI pipeline file at `/home/user/project/.github/workflows/ci.yml`. The YAML file must be valid, define a workflow, and contain a job named `test` with a run step that executes `python3 test_deploy.py`.

Ensure that you have run your Python script so that `status.log` is generated and available for verification.