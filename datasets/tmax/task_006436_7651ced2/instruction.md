You are a build engineer working on a web security artifact management tool called `sec_artifact`. The package handles cryptographic checksums of web application artifacts. The project is currently broken, and you need to fix the build system, write a schema migration, and successfully verify a set of artifacts.

The source code is located at `/home/user/sec_artifact` (which has been scaffolded for you).

Your objectives are:

1. **Fix the Package Build (`setup.py`)**: 
   The `setup.py` file has two issues:
   - A naive version comparison bug that prevents it from installing on Python 3.10+ (it does a raw string comparison like `if python_version < "3.8"` which fails for "3.10"). Update it to correctly parse and compare semantic versions using the `packaging.version` module.
   - The package relies on a C-extension for fast hash verification (`verifier.c`), but `setup.py` is not configured to build it. Add the necessary `setuptools.Extension` configuration so that `pip install .` successfully compiles the C module as `sec_artifact.verifier`.

2. **Migrate the Artifact Database (Schema Migration)**:
   There is an old JSON artifact database at `/home/user/artifacts_v1.json`. 
   Write a Python script at `/home/user/migrate.py` that reads this file and writes a new file `/home/user/artifacts_v2.json` with the following structural transformations:
   - `version` (string "1.0") becomes `schema_version` (string "2.0").
   - The `items` array is renamed to `artifacts`.
   - Inside each array element: 
     - `id` is renamed to `identifier`.
     - `checksum` and `type` are merged into fields `hash_value` and `hash_type`.
   For example, `{"id": "app1", "checksum": "abc", "type": "md5"}` becomes `{"identifier": "app1", "hash_value": "abc", "hash_type": "md5"}`.

3. **Verify the FFI and Migration**:
   Once the package is installed and the JSON is migrated, run the provided CLI tool against the new database:
   `sec_artifact check /home/user/artifacts_v2.json > /home/user/verification.log`

Ensure all files exist precisely at the requested paths and that `/home/user/verification.log` contains the final output of the CLI tool.