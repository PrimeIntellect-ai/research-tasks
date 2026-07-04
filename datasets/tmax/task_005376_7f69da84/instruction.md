You are a database administrator tasked with optimizing and securing NoSQL aggregation pipelines. Your company has an older, proprietary C++ tool (`/app/agg_oracle`) that validates aggregation pipelines before they run on the production database. However, this legacy binary is slow, cannot handle concurrent requests, and its source code was lost.

Your task is to write a modern, high-performance replacement in Rust.

**Task Requirements:**
1. Create a Rust project in `/home/user/pipeline_guard`.
2. Your Rust program must compile to a binary located at `/home/user/pipeline_guard/target/release/pipeline_guard`.
3. The binary must read a MongoDB-style aggregation pipeline (a JSON array of objects representing stages) from **standard input**.
4. The binary must exit with status `0` if the pipeline is valid, and exit with status `1` (or any non-zero) if it is invalid.

**Validation Rules (Schema & Pipeline Rules):**
You must implement a filter that perfectly matches the behavior of the legacy `/app/agg_oracle`. Through documentation and DBA folklore, we know the tool enforces these NoSQL aggregation rules:
- **Output Schema Validation:** The final stage of the pipeline MUST be a `$project` stage. The keys explicitly included (set to `1` or `true`) in this final `$project` stage must exactly match the keys defined in `/home/user/target_schema.json`. (Assume no nested fields in the projection for simplicity).
- **Schema Relationship Mapping & Cost:** The pipeline must contain no more than two `$lookup` stages (to prevent excessive JOIN-like costs).
- **Aggregation Limits:** If a `$group` stage is present, there MUST be at least one `$match` stage occurring *before* it in the pipeline array.
- **Oracle Quirks:** The `/app/agg_oracle` also rejects any pipeline where a `$unwind` stage directly follows a `$lookup` stage without a `$match` or `$project` in between. You must enforce this quirk.

**Resources Given:**
- `/app/agg_oracle`: A stripped, compiled binary of the legacy tool. You can execute it by passing the path to a JSON file as its first argument (e.g., `/app/agg_oracle pipeline.json`) to observe its exit codes and reverse-engineer any edge cases.
- `/home/user/target_schema.json`: A JSON array of strings representing the exact fields required in the final projection.
- `/home/user/corpora/clean/`: A directory containing 50 valid pipeline JSON files. Your tool MUST accept all of these (exit 0).
- `/home/user/corpora/evil/`: A directory containing 50 invalid/malicious pipeline JSON files. Your tool MUST reject all of these (exit 1).

Build your Rust application, test it against the corpora, and ensure the release binary is compiled and ready for automated testing.