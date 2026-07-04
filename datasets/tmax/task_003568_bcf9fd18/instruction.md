You are a performance engineer tasked with debugging a critical logging pipeline. We process high-frequency performance metrics serialized as JSON, but our ingestion system has been crashing due to malformed payloads and precision loss anomalies.

We vendor a lightweight C JSON parser for this pipeline. The source code is located at `/app/vendored/cJSON`. However, a recent configuration change broke the build of this parser. 

Your task consists of two parts:

**Part 1: Fix the Vendored Package**
1. Navigate to `/app/vendored/cJSON`.
2. Determine why `make all` is failing or producing a misconfigured binary. There is an environment misconfiguration and a perturbation in the `Makefile` causing precision loss/compilation errors when linking math libraries. 
3. Fix the `Makefile` or environment so that `make all` and `make test` pass successfully. 

**Part 2: Create a Log Sanitizer**
After fixing the parser, you need to build a protective filter for our ingestion system. We have observed that "evil" performance logs often contain invalid UTF-8 encoding sequences, deeply nested structures, or extreme floating-point precision values that cause catastrophic failures in downstream aggregators. 

Write an executable script at `/home/user/filter.sh` (you may use bash, python, or any other tool you prefer, but it must be an executable shell script or have the correct shebang).
- The script must take exactly one argument: the absolute path to a JSON log file.
- The script must exit with status `0` if the file is a clean, well-formed performance log.
- The script must exit with status `1` if the file contains invalid encodings, broken serializations, or structural anomalies (i.e., it is "evil").

Ensure your script is robust. You can use standard Linux utilities (like `grep`, `iconv`, `jq`, `bc`, `python3`) inside your script to perform the delta debugging and isolation of bad metrics.