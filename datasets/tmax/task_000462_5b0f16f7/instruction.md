You are tasked with helping a developer organize a messy project containing several gRPC/Protobuf service definitions. The project uses a custom, highly simplified domain-specific language (DSL) to manage build configurations, and the developer needs you to write a Bash script that acts as an interpreter for this DSL.

Your objective is to write a Bash script at `/home/user/organizer.sh` that interprets a configuration file located at `/home/user/config.org`.

The DSL in `config.org` consists of three commands. Your Bash interpreter must process the file line-by-line, maintaining internal state, and executing the corresponding actions:

1. `SET_TARGET <absolute_directory_path>`
   - Instructs the interpreter to set the target output directory.
   - If the directory does not exist, the interpreter should create it.

2. `PARSE_DIR <absolute_directory_path>`
   - Instructs the interpreter to scan all `.proto` files in the specified directory.
   - It must read each `.proto` file to find dependencies. Dependencies are declared exactly in the format: `import "filename.proto";` (assume imports reference files in the same directory).
   - The interpreter must build a dependency graph and perform a topological sort to determine the build order. The order should go from files with NO dependencies (independent) to files that depend on others. If multiple files can be processed at the same step, break ties alphabetically by filename.

3. `EMIT_PLAN <absolute_file_path>`
   - Instructs the interpreter to output the computed topological order of `.proto` filenames (just the basenames, e.g., `user.proto`), one per line, into the specified file.
   - Additionally, it must copy the `.proto` files from the parsed directory to the directory specified by the most recent `SET_TARGET` command.
   - When copying, the interpreter must prepend exactly one line to the top of each copied file: `// ORDER: N`, where `N` is the 1-based index of that file in the topological sort.

**Constraints:**
- Your solution must be written entirely in Bash (`/home/user/organizer.sh`).
- Make sure the script is executable (`chmod +x`).
- The script should take exactly one argument: the path to the configuration file (e.g., `./organizer.sh /home/user/config.org`).

**Setup state:**
Assume `/home/user/raw_protos/` contains a set of `.proto` files with valid, acyclic dependencies.
Assume `/home/user/config.org` exists and contains valid DSL commands.

Execute your script against `/home/user/config.org` once it is complete so the output files are generated for verification.