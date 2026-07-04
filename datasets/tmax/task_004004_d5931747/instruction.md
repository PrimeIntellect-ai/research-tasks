You have just inherited an unfamiliar legacy data processing codebase located in `/home/user/legacy_pipeline`. 

The pipeline relies on a fast, compiled data-crunching executable located at `/app/core_engine` (this is a stripped binary without debug symbols). This binary accepts JSON files containing arrays of numerical coordinates and performs spatial calculations.

Unfortunately, the system is currently broken in two ways:

1. **Compilation/Linker Error:** The pipeline uses a helper C-extension compiled via a bash script `/home/user/legacy_pipeline/build_helper.sh`. When you run this script, it fails with a linker error. You must interpret the error, modify the build script or source, and successfully compile `helper.so`.
2. **Data Processing Vulnerability (Precision & Crashes):** The `core_engine` binary is notoriously unstable. It silently loses precision or outright segfaults when fed certain extreme floating-point values or malformed numeric inputs. The previous developer started writing a Python pre-filter but abandoned it.

Your objective is to fix the build step and then complete the Python pre-filter. 

**Requirements for the Pre-Filter:**
* You must implement `/home/user/legacy_pipeline/validator.py`.
* The script will be invoked as: `python3 /home/user/legacy_pipeline/validator.py <path_to_json_file>`
* The script must read the JSON file and analyze the numeric values inside the `"coordinates"` array.
* If the file is perfectly safe to pass to `/app/core_engine` without causing a crash or precision overflow, the script MUST exit with status code `0`.
* If the file contains inputs that trigger the binary's bugs (e.g., precision vulnerabilities, out-of-bounds floats, NaNs), the script MUST exit with status code `1` (or any non-zero code).

You will need to use delta debugging on a few crashing examples you generate to black-box reverse engineer the exact numerical constraints of `/app/core_engine`. 

To succeed, your `validator.py` must perfectly distinguish between clean data and malicious/crashing data.