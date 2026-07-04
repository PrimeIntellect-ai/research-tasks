You are an engineer tasked with porting a dependency resolution tool to work inside a highly constrained, minimal Linux container build system. Since advanced package managers and languages like Python or Perl are not available in the bootstrap phase, you must implement the resolution logic using pure Bash and standard `coreutils`.

You have been provided with two CSV manifest files representing available statically compiled tools across different repositories:
- `/home/user/manifests/repo_main.csv`
- `/home/user/manifests/repo_alt.csv`

The format of these manifests is: `tool_name,version,size_in_bytes,source_repo`

You also have a requirements file:
- `/home/user/requirements.txt`

The format of the requirements file is: `tool_name,min_version`

Your task is to write a Bash script at `/home/user/resolve_deps.sh` that performs the following:
1. Reads the required tools and their minimum semantic versions from `requirements.txt`.
2. Searches across all provided manifest CSVs for versions of the tool that satisfy the requirement (i.e., available version `>=` minimum required version according to semantic versioning rules).
3. From the valid candidates for each required tool, selects the one with the **smallest `size_in_bytes`**. If there is a tie in size, select the one with the highest semantic version.
4. Calculates the total size in bytes of all selected tools.
5. Outputs the final selection to `/home/user/install_plan.txt`.

The output file `/home/user/install_plan.txt` must be sorted alphabetically by `tool_name` and perfectly formatted as follows:
```
tool_name,selected_version,size_in_bytes,source_repo
...
TOTAL_SIZE,total_bytes
```

For example, if the script selects `curl` from `repo_alt` and `wget` from `repo_main`, the output must look like:
```
curl,7.84.0,1950,repo_alt
wget,1.20.1,1500,repo_main
TOTAL_SIZE,3450
```

Constraints:
- You may only use Bash built-ins and standard POSIX/coreutils commands (e.g., `awk`, `sed`, `grep`, `sort`, `join`). Note that `sort -V` is highly useful for semantic version comparison.
- Make sure `/home/user/resolve_deps.sh` is executable and runs successfully to produce the output file.