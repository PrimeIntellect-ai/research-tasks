You are a developer debugging a failing build pipeline in our continuous integration system. Recently, the pipeline started failing because a proprietary build tool, the `manifest_compiler`, is sporadically crashing (Segfaulting) when processing certain generated JSON manifest files. 

You need to investigate this issue, determine the root cause, and implement a pre-flight validator to prevent the build system from feeding crash-inducing manifests to the compiler.

Here is what you have:
1. **The Compiler:** A stripped, proprietary binary located at `/app/bin/manifest_compiler`. It takes a single file path as an argument.
2. **Build Logs:** The pipeline consists of three microservices that transform the raw project definitions into the final JSON manifests. Their logs are scattered in `/home/user/logs/service_A.log`, `/home/user/logs/service_B.log`, and `/home/user/logs/service_C.log`. You will need to reconstruct the timeline across these services to identify the exact inputs that triggered the crash during the last failed build.
3. **Sample Data:** The raw inputs and generated manifests from the last build are located in `/home/user/build_artifacts/`. 

Your objectives:
1. **Analyze the Logs & Artifacts:** Reconstruct the timeline of the failed build from the logs. Identify which specific JSON manifest crashed the `manifest_compiler`. 
2. **Determine the Root Cause:** Use interactive debugging (`gdb`), strace, or black-box testing against `/app/bin/manifest_compiler` using the artifacts to figure out the exact data anomaly that causes the crash. Compare the transformations (diff analysis) between successful and failed manifests.
3. **Write a Validator:** Create a Python script at `/home/user/detector.py` that acts as a gatekeeper. 
    * It must accept a single command-line argument: the path to a JSON manifest.
    * It must parse the JSON and inspect it for the crash-inducing condition.
    * It must exit with code `0` if the manifest is safe (clean).
    * It must exit with code `1` if the manifest contains the vulnerability (evil) that would crash the compiler.

Ensure your Python script is robust, self-contained, and uses only standard library modules. An automated integration system will verify your script against a hidden corpus of hundreds of clean and evil manifests.