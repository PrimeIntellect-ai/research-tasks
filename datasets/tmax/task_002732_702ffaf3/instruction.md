You are an MLOps engineer responsible for maintaining a lightweight, high-performance data processing and inference pipeline written in C. We use a vendored version of the `cJSON` library for tracking our experiment metadata and artifacts.

Recently, we encountered three issues with our pipeline:
1. **Broken Dependency**: The vendored `cJSON` library located at `/app/cJSON-1.7.15` fails to build. Someone made a mistake in its `Makefile` and source.
2. **Schema Enforcement & Silent Type Corruption**: Our data ingestion script, `inference_pipeline.c` (located at `/home/user/pipeline/`), reads a dataset `/home/user/data/input.csv`. The dataset contains integer features. However, due to missing values represented as empty strings or "NaN", our naive CSV parser converts these rows to floating-point numbers during the JSON experiment tracking phase, corrupting the schema. 
3. **Inference Performance**: The batch inference loop in `inference_pipeline.c` is unoptimized. It contains redundant memory allocations inside the loop. 

Your tasks are:
1. **Fix the vendored package**: Repair the compilation issues in `/app/cJSON-1.7.15` so that it builds correctly using `make` and outputs the shared library `libcjson.so`.
2. **Fix Data Schema Enforcement**: Modify `/home/user/pipeline/inference_pipeline.c` to properly enforce the schema. If a feature column in the CSV is missing or invalid (e.g., "NaN"), it should be strictly assigned a default integer value of `-1` and logged as an integer in the resulting JSON experiment tracking file, NOT as a float.
3. **Optimize Inference Benchmarking**: Refactor `inference_pipeline.c` to improve the batch inference throughput. You must move the repeated dynamic memory allocations out of the hot loop.
4. **Compile and Run**: Compile your fixed `inference_pipeline.c` against the fixed `cJSON` library. Run the executable. It must read `/home/user/data/input.csv` and generate an experiment tracking log at `/home/user/pipeline/experiment_log.json`.

We will run a benchmark script `/home/user/bench.sh` that times the execution of your compiled pipeline against a reference implementation. You need to achieve a speedup of at least 2.0x compared to the original unoptimized code, and the output `experiment_log.json` must strictly contain only integer types for the feature arrays.