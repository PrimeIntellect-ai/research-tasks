You are acting as an MLOps engineer maintaining a C++ artifact tracking service. We have a pipeline that tracks model experiment outcomes and model embeddings. 

Currently, the C++ tracker `artifact_tracker.cpp` located in `/home/user/tracker/` is failing to compile and, even when we bypassed the build issue previously, it produced a "silent failure" where the combined model scores all evaluated to zero (similar to a plot returning blank due to a backend misconfiguration).

Your goal is to fix the environment, fix the numerical bug, compile the tracker, and run it to produce the correct artifact metrics.

The tracker performs the following operations:
1. **Multi-source Data Joining**: Reads `/home/user/data/models.csv` (contains `model_id,prior_alpha,prior_beta` for a Beta distribution prior) and `/home/user/data/trials.csv` (contains `model_id,successes,failures,embedding_vector` separated by semicolons). It joins these on `model_id`.
2. **Bayesian Inference**: Computes the posterior Beta distribution parameters for each model's success rate: `post_alpha = prior_alpha + successes`, `post_beta = prior_beta + failures`.
3. **Numerical Accuracy Test**: Computes the MAP (Maximum A Posteriori) estimate for the model's success probability.
4. **Embedding Retrieval**: Reads a target query embedding from `/home/user/data/query.txt` and computes the Cosine Similarity between the model's embedding and the query.
5. **Output**: Writes the results to `/home/user/tracker/output.csv` with columns `model_id,post_alpha,post_beta,map_estimate,similarity,final_score`, where `final_score = map_estimate * similarity`.

**Task Instructions:**
1. Fix the missing dependencies. The tracker uses `<boost/math/distributions/beta.hpp>`. You will need to install the appropriate boost math development packages and C++ build tools (like `g++` and `make`) using `apt-get` (you have passwordless sudo).
2. Inspect `/home/user/tracker/artifact_tracker.cpp`. There is a numerical bug in the MAP calculation causing integer division, which artificially zeroes out the probability estimates. Fix this bug so it uses proper floating-point arithmetic. The formula for the MAP of a Beta distribution is `(alpha - 1.0) / (alpha + beta - 2.0)`.
3. Build the program using the provided `Makefile` in `/home/user/tracker/`.
4. Run the program from the tracker directory: `./artifact_tracker /home/user/data/query.txt`.
5. Ensure the file `/home/user/tracker/output.csv` is correctly generated. All floating-point values should be printed with at least 4 decimal places of precision.

The CSV files and initial buggy code have already been placed in the appropriate directories.