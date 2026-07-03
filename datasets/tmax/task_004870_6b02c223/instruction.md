You are an engineer tasked with debugging a failing build pipeline in a legacy project. 

The project is located at `/home/user/project`. 
There is a build script at `/home/user/project/build.sh` that processes a list of graphical assets and compiles them using a proprietary binary compiler located at `/home/user/project/bin/asset_compiler`. 

The script queries a SQLite database (`/home/user/project/assets.db`) to find out which assets are marked as "active" (active=1), and then spins up background workers to compile them into the `/home/user/project/out/` directory.

However, the build is silently dropping some files, and the output directories are incomplete. Developers have noticed scattered error codes in the logs (which are dumped into `/home/user/project/logs/`), but because the workers run asynchronously, the logs are scrambled and the exact cause is hard to trace.

Your tasks are to:
1. Debug the `build.sh` script, the query results, and the worker logs to figure out why the build is failing for certain assets. You may need to inspect the `asset_compiler` binary's behavior to understand the error codes.
2. Identify the exact filename(s) of the active asset(s) that are failing to build. Write the exact original filename(s) to `/home/user/failing_assets.txt`, one per line.
3. Fix the underlying bug in the build script so that it properly handles all active assets without failing. Write your corrected script to `/home/user/project/build_fixed.sh`. Ensure it has execute permissions.
4. When `/home/user/project/build_fixed.sh` is run, it must successfully generate the compiled output files in `/home/user/project/out/` for *only* the active assets.

Constraints:
- Do not modify the `asset_compiler` binary or the `assets.db` database.
- Use Bash for your scripting.