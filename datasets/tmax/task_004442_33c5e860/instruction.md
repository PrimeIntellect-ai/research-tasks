You are tasked with building a concurrent configuration diffing and archiving pipeline. 

A recent system update generated thousands of new configuration files located in `/home/user/new_configs/`. The previous versions of these configurations are stored in a SquashFS image at `/home/user/old_configs.sqsh`. 

We have a proprietary, compiled binary utility located at `/app/patch_gen` which generates specialized binary patches between an old config and a new config file. 

Your objectives are as follows:
1. **Mount** the old configuration archive `old_configs.sqsh` as a read-only filesystem at `/home/user/mnt_old/`.
2. **Search** for all `.conf` files in `/home/user/new_configs/` that contain the string `NEEDS_UPDATE=true` in their metadata header (first 5 lines).
3. **Transform** the content of these target `.conf` files: before generating a patch, you must redact any sensitive keys. Specifically, use text transformation tools (like `sed`, `awk`, or Python) to find any line starting with `API_KEY=` or `DB_PASS=` and replace the value with `REDACTED` (e.g., `API_KEY=12345` becomes `API_KEY=REDACTED`). Do not overwrite the original files in `new_configs`; store the redacted versions in a temporary workspace.
4. **Generate Patches**: Write a Python script to process all the identified and redacted `.conf` files *concurrently*. For each file, invoke the `/app/patch_gen` binary to diff the old version (from the mounted SquashFS) and the new redacted version. The binary usage is roughly `patch_gen <old_file> <new_file> <output_patch_file>`.
   *Note: `/app/patch_gen` is a stripped binary. You may need to inspect it to see if there are any undocumented flags that produce smaller, optimized patch files. Bandwidth is highly restricted, so your output patches must be as small as possible.*
5. **Manifest Generation**: As your concurrent Python workers generate patches, they must append the file path and the patch size to a single shared manifest file at `/home/user/patch_manifest.txt`. You **must** use POSIX file locking (e.g., `fcntl` in Python) to prevent race conditions during concurrent writes.
6. **Archive**: Once all patches are generated, compress the resulting patch files and the manifest into a single archive at `/home/user/update.tar.gz`.

Your final evaluation will be based on the successful execution of the entire pipeline, the absence of race conditions in your manifest, the correctness of the redactions, and crucially, a **metric threshold on the final archive size**. If you do not utilize the binary optimally, your archive will exceed the strict size limits.