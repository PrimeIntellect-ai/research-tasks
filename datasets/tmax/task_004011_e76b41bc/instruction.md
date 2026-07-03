You are a mobile build engineer maintaining a CI/CD pipeline. The pipeline currently orchestrates a polyglot build process (handling C++ and Python components), but it is failing because a recent commit introduced a circular import in our Python build scripts.

A colleague has prepared a patch to resolve the circular dependency, located at `/home/user/fix_circular.patch`. 

Your task is to:
1. Apply the patch to the files in the `/home/user/build_scripts/` directory.
2. The CI/CD pipeline requires a strict verification step before building. You must write a Python script at `/home/user/ci_checksum.py` that calculates the SHA256 checksums of all `.py` files inside `/home/user/build_scripts/` (after the patch is applied).
3. Your Python script must output these checksums into a JSON file located at `/home/user/build_scripts/manifest.json`.
4. The JSON file must be a single flat dictionary where the keys are the exact filenames (e.g., `"android_build.py"`) and the values are their corresponding lowercase SHA256 hex digests.
5. Execute your Python script so that `/home/user/build_scripts/manifest.json` is generated.

Do not remove any files, and ensure the patch is applied cleanly.