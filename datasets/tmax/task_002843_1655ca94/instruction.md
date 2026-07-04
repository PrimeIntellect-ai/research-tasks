You are a support engineer tasked with collecting diagnostics from a customer's system. The customer relies on a proprietary log parsing tool located at `/app/telemetry_parser` (a stripped binary) to process telemetry data. However, the system is currently in a broken state, and the parser is failing. 

Your objectives are to fix the environment, compile a necessary plugin, and write an optimized Bash wrapper script.

**Step 1: Fix the Crashing Binary**
Whenever `/app/telemetry_parser` is run, it currently crashes with a Segmentation Fault. 
- Enable core dumps and run the binary to generate a core dump.
- Analyze the core dump to determine the root cause. You will find it is trying to access a specific configuration file in a directory that doesn't exist.
- Repair this environment misconfiguration so the binary runs without crashing (it will output "Config loaded" when successful).

**Step 2: Compile the Missing Plugin**
The binary requires a plugin to process the data correctly. The source code for this plugin is provided at `/home/user/plugin/parser_plugin.c`.
- Attempt to compile this plugin into a shared object `/home/user/plugin/parser_plugin.so`.
- You will encounter compiler/linker errors. Interpret and fix these errors (you may need to modify the compilation command to include the correct flags, such as `-fPIC` and linking the math library `-lm`).
- Once compiled, the binary must be told to load it via the `PLUGIN_PATH` environment variable.

**Step 3: Write the Optimized Wrapper**
Write a Bash script at `/home/user/run_diagnostics.sh` that processes all `.dat` files in the `/app/data/` directory using the `/app/telemetry_parser`.
- The script must take the data directory as its first argument (e.g., `./run_diagnostics.sh /app/data`).
- For each file, the script must execute: `PLUGIN_PATH=/home/user/plugin/parser_plugin.so /app/telemetry_parser <file_path>`
- **Performance Requirement:** There are 1000 files. Processing them sequentially will take too long. You must use Bash job control, `xargs`, or `parallel` to process the files concurrently. Your script must finish executing in under 5.0 seconds. 
- Make sure `/home/user/run_diagnostics.sh` is executable.

Your final deliverable is the properly configured environment, the compiled `.so` file, and the `/home/user/run_diagnostics.sh` script.