You are an infrastructure engineer automating the provisioning and deployment pipeline for our high-throughput mailing list servers. We have a legacy, proprietary route compiler located at `/app/mlist_compiler`. This binary reads plain-text email routing rules and compiles them into an optimized binary database format required by our mailing list daemons. 

Currently, the compilation process is extremely slow because the binary is strictly single-threaded. However, the records it generates are completely independent, meaning the resulting binary output files can be safely concatenated together to form a fully valid database.

Your task is to write a deployment script at `/home/user/deploy.sh` that automates a staged rolling deployment and optimizes the compilation step.

The script must:
1. Accept exactly two arguments: `RELEASE_ID` (a string) and `INPUT_FILE` (the path to the raw text routes). Example usage: `/home/user/deploy.sh v202310 /home/user/incoming/routes_new.txt`
2. Create a new directory for the release at `/home/user/deployments/releases/<RELEASE_ID>`.
3. Process the `INPUT_FILE` using `/app/mlist_compiler` and output the final combined database to `/home/user/deployments/releases/<RELEASE_ID>/routes.db`.
   - Usage of the binary is: `/app/mlist_compiler <input_file> <output_db_file>`
   - **Performance requirement:** You must significantly speed up the compilation process using Bash scripting. You should chunk the input file, process the chunks in parallel with the compiler, and concatenate the outputs. 
4. Manage the deployment symlinks safely to enable rolling deployments:
   - If `/home/user/deployments/current` exists and is a symlink, re-point `/home/user/deployments/previous` to its target.
   - Point the `/home/user/deployments/current` symlink to the newly created release directory (`/home/user/deployments/releases/<RELEASE_ID>`).

**Constraints & Details:**
* The primary language must be Bash. Make sure `/home/user/deploy.sh` is executable.
* `/home/user/incoming/routes.txt` will contain around 100,000 lines of routing rules.
* You do not need to install any external tools; standard GNU coreutils (like `split`, `cat`, `wc`, `xargs`) are sufficient.
* The test environment has 4 CPU cores available.