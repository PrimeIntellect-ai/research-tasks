You are tasked with building a configuration validator for an ETL pipeline. Our configuration manager tracks changes to settings files, but recently, an ETL job retry mechanism has started producing malformed configuration artifacts with duplicate keys within the same configuration section.

We use a proprietary package called `confparser` to reshape our wide-format configuration files into a long-format JSON stream (JSON Lines). 
The source for this package is vendored at `/app/confparser-1.0.0/`. However, the package has a known issue and is failing to run properly out of the box due to a deliberate perturbation in its source code that was accidentally committed. 

Your objectives are:
1. **Fix the vendored package**: Locate the syntax error or missing import in `/app/confparser-1.0.0/confparser.py` and fix it so it can successfully reshape wide config files into JSON lines. The script should output lines like: `{"section": "database", "key": "host", "value": "localhost"}`.
2. **Create the detector pipeline**: Write a Bash script at `/home/user/detector.sh` that takes a single file path as an argument.
3. **Orchestrate the stages**: Inside your script, run the fixed `confparser.py` on the provided input file. Then, using standard bash tools (like `jq`, `awk`, `sort`, `uniq`), parse the JSON lines to detect if there are any duplicate keys within the SAME section.
4. **Output format and exit codes**: 
   - If the file is **clean** (no section/key duplicates), the script MUST exit with code `0`.
   - If the file is **evil/malformed** (contains duplicate keys within the same section), the script MUST exit with code `1`.

Constraints:
- You must write the solution entirely using Bash and standard CLI utilities (coreutils, jq, awk, etc.).
- Ensure your `detector.sh` is executable (`chmod +x`).
- Do not rely on internet access; everything you need is already in the environment.