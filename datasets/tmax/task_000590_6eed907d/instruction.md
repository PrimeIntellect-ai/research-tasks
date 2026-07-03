You have inherited a legacy C++ codebase located at `/home/user/prng_project`. This repository builds a custom pseudo-random number generator (PRNG) executable used by several of our internal simulation microservices. 

Recently, downstream services began logging statistical anomalies—the generated sequences are failing randomness tests. We suspect a regression was introduced somewhere in the git history during a recent refactoring effort.

Unfortunately, the original author is no longer with the company. However, we have two critical pieces of information:
1. A photo of the author's whiteboard notes at `/app/whiteboard_notes.png`, which details the original mathematical recurrence relation, including the specific bitwise operations and magic constants used.
2. A stripped, legacy oracle binary at `/app/oracle_prng` that was compiled before the bug was introduced. This binary is known to be correct.

The PRNG executable always takes exactly two arguments:
`./prng <seed> <iterations>`
It outputs a single unsigned 64-bit integer (the final state after N iterations) to standard output.

Your task is to:
1. Analyze the whiteboard image (`/app/whiteboard_notes.png`) to understand the correct mathematical formula.
2. Reconstruct the timeline of the bug by building a regression test (using the oracle binary as a baseline) and using git bisection on `/home/user/prng_project` to identify the faulty commit.
3. Fix the C++ source code in the repository so that it correctly implements the mathematical logic shown in the whiteboard image and perfectly matches the behavior of the oracle binary.
4. Compile your corrected C++ code and output the final executable to exactly `/home/user/fixed_prng`.

Make sure your fixed executable is perfectly bit-exact with the oracle for any given 64-bit seed and iteration count. Do not change the CLI argument parsing logic, only the mathematical core.