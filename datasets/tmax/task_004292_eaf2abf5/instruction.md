You are an engineer setting up a polyglot build system from scratch. Our build infrastructure uses a predictive cost model to estimate the compilation time of 30 different language modules (e.g., C++, Rust, Python, Go) before parallelizing the tasks. 

We are currently migrating our build manifests from a v1 schema to a v2 schema. As part of this migration, you need to write a Python CLI tool that deserializes the v1 manifest, applies a numerical estimation algorithm using weights recovered from a legacy data asset, and serializes the output into the new v2 schema.

The legacy data asset is a video file located at `/app/module_weights.mp4`. This video is exactly 30 frames long. Each frame is a solid color. The exact numerical weight for module $i$ (where $i$ is from 0 to 29) is exactly the value of the Red (R) channel (from 0 to 255) in frame $i$.

Your task:
1. Extract the frames from `/app/module_weights.mp4` and determine the 30 integer weights.
2. Write a Python script at `/home/user/migrate_and_estimate.py`.
3. The script must accept a single command-line argument: a JSON string representing the v1 build manifest.
   * v1 Schema format: `{"schema_version": 1, "modules": [{"id": 0, "size": 150}, {"id": 1, "size": 42}, ...]}` (It will always contain exactly 30 modules, with IDs 0 to 29 in order).
4. The script must calculate the estimated build cost as the dot product of the module sizes and the extracted video weights (i.e., `sum(size[i] * weight[i])`).
5. The script must print to standard output ONLY a JSON string representing the v2 schema with the calculated cost.
   * v2 Schema format: `{"schema_version": 2, "build_cost": <calculated_integer_cost>}`

Ensure your script is perfectly deterministic and only prints the final v2 JSON string to stdout. Do not print any debug information to stdout (you may use stderr if needed). Make sure the script has execution permissions (`chmod +x`).