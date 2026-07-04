You are tasked with building a high-performance configuration validation pipeline for a massive network infrastructure. We have a daily dump of device configurations, but some of them are corrupted, outdated, or maliciously modified. 

You must write a Bash script at `/home/user/process_configs.sh` that acts as a robust configuration filter and grouper. 

The script must take two arguments:
1. `<input_dir>`: A directory containing thousands of configuration files.
2. `<output_dir>`: The destination directory for valid configurations.

### Processing Requirements
Your script must process the files in the input directory **in parallel** (using standard Bash tools like `xargs -P`, `&` backgrounding, or `parallel`) to handle large volumes efficiently. For each file, it must pass a series of validation checkpoints:

**Validation Gate 1: Proprietary Header**
Every valid configuration file begins with a proprietary binary header. We have provided a legacy validation tool at `/app/legacy_sig_check` (a stripped binary) that verifies this header. However, `legacy_sig_check` is notorious for being resource-intensive. You may either use it as a black-box oracle within your script or reverse-engineer it (using `xxd`, `strings`, `objdump`, etc.) to implement an equivalent check using pure Bash/Coreutils for significantly faster processing.

**Validation Gate 2: Security Policy**
After the 16-byte binary header, the file contains plaintext configuration lines. The config must strictly adhere to the following policies:
- Must contain exactly one `hostname <name>` directive, where `<name>` is an alphanumeric string (hyphens allowed).
- Must NOT contain any line with the exact string `password 7 ` (which indicates prohibited weak encryption).
- Must contain a `DeviceType: <type>` directive.

**Sorting and Grouping**
For configurations that pass both validation gates, extract the device type from the `DeviceType: <type>` line. Copy the valid configuration file into the output directory, grouped into subdirectories by their device type. For example, if a valid file `rtr1.conf` has `DeviceType: core-router`, it should be copied to `<output_dir>/core-router/rtr1.conf`.

Your script must be fully executable and handle files safely. It will be tested against automated verification corpora that will run your script and evaluate the contents of the output directory. Do not leave any temporary files behind.