You are an engineer working on porting a critical internal data-processing tool to run inside a minimal "scratch" container (which has no glibc or external libraries). 

The tool currently consists of two components:
1. A data generator written in C (`/home/user/project/generator.c`).
2. A data processor written in Go (`/home/user/project/processor.go`).

Your task is to write a CI/CD orchestration script in Bash (`/home/user/project/ci_pipeline.sh`) that automates the build, packaging, and performance benchmarking of this polyglot application.

The script must do the following when executed:
1. **Deserialization**: Parse `/home/user/project/config.json` to extract two integer values: `runs` and `count`. You may use `jq`.
2. **Polyglot Build Orchestration**: 
   - Compile `generator.c` into an executable named `generator`. It **must** be 100% statically linked so it can run in a scratch container.
   - Compile `processor.go` into an executable named `processor`. It **must** also be 100% statically linked.
   - Package both resulting binaries into a tarball named `/home/user/project/release.tar.gz`.
3. **Performance Benchmarking**:
   - Execute the data pipeline by piping the generator into the processor: `./generator <count> | ./processor`
   - Run this pipeline exactly `runs` times.
   - Measure the execution time of the pipeline for each run.
   - Calculate the average execution time across all runs in **milliseconds** (integer arithmetic is fine).
4. **Serialization**: 
   - Output the benchmark results into a valid JSON file at `/home/user/project/benchmark_result.json`.
   - The JSON file must have exactly this structure: `{"average_ms": <calculated_average>, "status": "success"}`

Requirements:
- Ensure your bash script has executable permissions.
- Do not modify the source code of the C or Go files.
- You must use Bash built-ins, `jq`, and standard coreutils to handle the execution time measurement and JSON generation.