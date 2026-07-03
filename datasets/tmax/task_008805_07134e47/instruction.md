You are a performance engineer tasked with debugging a mathematical processing pipeline. 

The pipeline code is located in `/home/user/perf_test`. You have a build script (`/home/user/perf_test/build.sh`), a C program (`/home/user/perf_test/cruncher.c`), a data generator (`/home/user/perf_test/generator.sh`), and a master script (`/home/user/perf_test/run_pipeline.sh`).

Currently, the pipeline is failing for two reasons:
1. The C program fails to build due to a compilation/linker error. 
2. Once the program compiles, the pipeline experiences a significant performance bottleneck during execution. One specific data payload causes the processing to hang for several seconds.

Your tasks are:
1. Identify and fix the build error by modifying `/home/user/perf_test/build.sh`. Do not modify `cruncher.c` to fix the build.
2. Run `/home/user/perf_test/run_pipeline.sh`. This will generate two log files: `/home/user/perf_test/gen.log` (from the generator) and `/home/user/perf_test/crunch.log` (from the C program).
3. Analyze the timeline of intermediate states in the logs to find the exact `ID` of the payload that takes more than 1 second for the cruncher to process.
4. Create a file `/home/user/solution.txt` with exactly two lines:
   - Line 1: The missing compiler/linker flag you added to fix the build (e.g., `-lpthread`, `-lm`, `-O3`).
   - Line 2: The ID of the bottleneck payload.

Format for `/home/user/solution.txt`:
```
Flag: <your_flag_here>
Bottleneck ID: <id_here>
```