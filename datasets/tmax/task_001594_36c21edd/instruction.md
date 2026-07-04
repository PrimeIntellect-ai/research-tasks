You are a Machine Learning Engineer preparing a dataset of physical simulation features for a neural network. You are using a proprietary fluid dynamics solver, provided as a stripped binary at `/app/sim_engine`. 

We have discovered a critical issue: due to a floating-point reduction order bug in the binary's multi-threading routine, certain input configurations produce chaotic, non-reproducible results across runs. If we train our neural network on these unstable configurations, it will fail to converge.

Your task is to build a robust data sanitization pipeline that can classify and filter out these unstable parameter files.

**Resources Provided:**
1. **The Binary:** `/app/sim_engine`. It takes a single parameter file as an argument (e.g., `/app/sim_engine config.txt`) and outputs a log to `stdout` containing the line `final_energy: <value>`.
2. **Adversarial Corpus:**
   - `/app/corpus/clean/`: Contains 50 parameter files that are known to be perfectly stable and reproducible.
   - `/app/corpus/evil/`: Contains 50 parameter files known to trigger the floating-point non-determinism.

**Requirements:**
1. Create an executable script at `/home/user/filter_sims` (you may use any language, e.g., Python, Bash+Awk, etc.).
2. The script must take exactly one argument: a path to a directory containing parameter files.
3. For each file in the directory, your script must invoke the `/app/sim_engine` multiple times (convergence testing) and extract the `final_energy`.
4. You must implement a **bootstrap confidence interval** (95% CI) over the empirical distribution of `final_energy` for each file. 
5. Use the width of this confidence interval to determine if the simulation is stable. Files with wide intervals are non-reproducible and must be rejected.
6. The script must print the **absolute paths** of the preserved ("clean") files to standard output, one per line. It must output nothing else.

Your script will be verified against the provided clean and evil corpora. It must preserve 100% of the clean corpus and reject 100% of the evil corpus.