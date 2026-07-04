We are migrating our CI build servers from Python 2 to Python 3. During this transition, our environment is unstable and we frequently encounter nodes where neither Python 2 nor Python 3 is reliably available in the initial provisioning phase. 

Because of this, our initial dependency bootstrapping script—which was written in Python 2 and handled pulling down our internal build plugins—is failing. It was also suffering from a bug similar to Node.js npm peer dependency conflicts, where it would pick versions that didn't satisfy all constraints.

We need you to rewrite this dependency resolver entirely in **Bash** using standard tools (like `jq`, `awk`, `grep`, `sed`, `sort`, `sha256sum`).

Your objective is to write a script at `/home/user/project/resolver.sh` that does the following:

1. **Structured Data Parsing & Schema Migration:** 
   Read direct dependencies from `/home/user/project/app.json`. The JSON format is:
   `{"dependencies": {"plugin_name": ">=version"}}`.
   Also read the plugin registry from `/home/user/project/registry.csv`. The CSV has no header and the format is:
   `PluginName,Version,Requires,Sha256`
   (Where `Requires` is either `NONE` or a single requirement like `OtherPlugin>=Version`).

2. **Semantic Version Comparison:**
   For each dependency in `app.json`, and recursively for any `Requires` specified in the registry, you must determine the **highest available version** in `registry.csv` that satisfies the `>=` constraints.
   * If `pluginA` is required as `>=1.0.0` by `app.json` and `>=1.2.0` by `pluginB`, the resolved version must be the highest version in the registry that is `>=1.2.0`. 
   * Use `sort -V` for semantic version sorting.

3. **Checksum Verification:**
   Once you've identified the highest valid version for a plugin, verify its tarball's SHA256 checksum. The tarballs are located in `/home/user/project/downloads/` and named `[PluginName]-[Version].tar.gz`.
   * Compare the calculated checksum of the tarball with the `Sha256` field in `registry.csv`.
   * If the checksum does not match, that version is considered corrupt and you must fall back to the next highest version that satisfies the constraints and has a valid checksum.

4. **Output Lockfile:**
   Generate a lockfile at `/home/user/project/lockfile.csv` containing the final resolved list of plugins. 
   The format must be exactly: `PluginName,ResolvedVersion,TarballSha256`
   The entries in the lockfile must be sorted alphabetically by `PluginName`.

**Files provided in the environment (which you can assume exist):**
- `/home/user/project/app.json`
- `/home/user/project/registry.csv`
- `/home/user/project/downloads/*.tar.gz`

**Constraints:**
- You must use Bash only (no Python, Perl, Ruby, etc.).
- Your script must be executable (`chmod +x /home/user/project/resolver.sh`).
- Execute your script to generate the `lockfile.csv` so it can be verified.