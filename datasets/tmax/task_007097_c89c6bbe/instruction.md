You are an artifact manager tasked with curating a binary repository's metadata. Our legacy system exports dependency graphs into a messy log file, and we suspect that recent build timeouts are caused by circular dependencies (infinite loops) in the artifact requirements.

Your task is to analyze the exported log file, find all artifacts that are part of a circular dependency loop, and output them in a structured format.

Here is the setup:
- The raw export is located at `/home/user/raw_exports.log`.
- The file contains various log lines. Artifact dependency records are on lines starting with `INFO: [ARTIFACT]`.
- The format of these lines is: `INFO: [ARTIFACT] name=<artifact_name> v=<version> ; requires=<dependency1>,<dependency2>,...`
- If an artifact has no dependencies, the requires field will be `NONE`.
- A circular dependency occurs when an artifact eventually requires itself through a chain of dependencies (e.g., A -> B -> C -> A). Any artifact that is a member of such a cycle is considered "in a loop". Artifacts that merely point to a loop but are not part of the cycle itself should NOT be included.

Write a Python script (or use bash text-processing tools combined with Python) to parse this log file and identify the loops. 
Save the final result to `/home/user/loop_artifacts.json`. 

The output file `/home/user/loop_artifacts.json` MUST be a strictly formatted JSON array containing the string names of all artifacts involved in any circular loop, sorted alphabetically.

Example output format for `/home/user/loop_artifacts.json`:
```json
[
  "artifact-A",
  "artifact-C"
]
```