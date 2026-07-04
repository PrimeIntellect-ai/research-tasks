You are a build engineer debugging a failed build pipeline for a system project. The build tool is written in Python. 

Your workspace is located at `/home/user/build_env`.

Currently, the custom build script (`build.py`) fails with a linking error. You need to fix the build tool and determine the correct link order for the project's artifacts.

Here are your tasks:
1. Apply the patch `/home/user/build_env/fix_linker.patch` to `/home/user/build_env/build.py`. This patch adds the missing `--link-order` argument to the build script, which allows it to accept a pre-computed build sequence.
2. The file `/home/user/build_env/deps.json` contains a dictionary where each key is a module name, and the value is a list of modules it depends on. This graph currently contains a circular dependency that must be resolved.
3. Write a Python script to parse `deps.json` and resolve the constraints:
   - **Schema transformation**: Any module whose name ends with `_stub` is a mock. Mocks do not actually depend on anything in the final build. You must dynamically clear the dependency list for any module ending in `_stub` (e.g., if `"lib_stub": ["libA"]` exists, change it to `"lib_stub": []`).
   - **Constraint satisfaction (Topological Sort)**: Calculate the valid build order where every module appears strictly *after* all of its dependencies. 
   - **Tie-breaking**: Whenever multiple modules are ready to be built (i.e., all their dependencies have been built), always pick the module that comes first alphabetically.
4. Save the computed build sequence to `/home/user/build_env/link_order.txt`, with one module name per line.
5. Run the patched build script using your computed link order:
   `python3 /home/user/build_env/build.py --link-order /home/user/build_env/link_order.txt`

If successful, the build script will generate the final artifact at `/home/user/build_env/build_artifact.bin`.