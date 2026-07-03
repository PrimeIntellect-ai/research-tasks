You are tasked with building a toolset for an artifact manager curating a local binary repository. The repository is actively being read by other processes, so you must carefully handle file updates to prevent read failures.

Your objective is to build a Rust tool that processes package metadata, safely updates it, and packages the curated releases.

**Initial State:**
You have a repository located at `/home/user/artifacts`. It contains a nested directory structure representing packages and their versions (e.g., `/home/user/artifacts/<package_name>/<version>/`).
Inside each version directory, there are two files:
1. `bin.dat`: A mock binary file.
2. `meta.json`: A JSON file containing metadata. Format: `{"name": "...", "version": "...", "status": "..."}`.

**Step 1: Rust Metadata Curator**
Create a Rust project in `/home/user/curator`. Write a Rust program that:
1. Recursively traverses `/home/user/artifacts` to find all `meta.json` files.
2. Parses each `meta.json` file.
3. If the `status` field is exactly `"testing"`, update it to `"stable"`, and add a new field `"curated_at"` with the integer value `1700000000`. If the status is not `"testing"`, leave it unchanged.
4. **Safety Requirement:** You must write the updated JSON back to disk *atomically* to avoid race conditions with background readers. Do this by writing to `meta.json.tmp` in the same directory, and then atomically renaming it to `meta.json`.
5. After processing all files, the Rust program must generate a CSV file at `/home/user/curated_summary.csv` listing all packages that are currently `"stable"` (including those that were already stable and those you just updated).
   The CSV format must be exactly: `name,version,status` (with a header row).

**Step 2: Archive Creation**
Using standard Linux utilities, read the output of your Rust tool (or search the directory directly) and create a compressed tarball at `/home/user/stable_artifacts.tar.gz` containing only the `bin.dat` and `meta.json` files (with their directory structure preserved relative to `/home/user/artifacts/`) of all packages that have a `"stable"` status. 
*Note: Run the tar command from inside `/home/user/artifacts/` so the paths inside the archive start with the package names (e.g., `alpha/1.0/bin.dat`).*

**Step 3: Text Transformation**
Using `awk`, `sed`, or similar standard shell text processing tools, process `/home/user/curated_summary.csv` to generate a plain text list of the stable packages in the format `Package: <name> v<version>` (one per line, ignoring the header). Save this output to `/home/user/release_list.txt`.

Ensure your Rust code compiles and runs successfully, and perform the necessary shell steps to generate the archive and text file.