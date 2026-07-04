You are a machine learning engineer preparing a high-quality training dataset for a new probabilistic model. We have received two batches of historical training data, but one batch is heavily contaminated with synthetically generated adversarial examples (the "evil" data). Your objective is to build a high-performance Rust-based data sanitizer that filters out these adversarial examples while preserving the clean data.

Here are the specific steps you must follow:

1. **Parameter Extraction:** 
   We have an image of a whiteboard containing the prior distribution parameters for our baseline Bayesian model. The image is located at `/app/model_params.png`. Use `tesseract` to extract the text from this image. The image contains a set of Gaussian prior parameters (Means and Covariances) for three primary features: `alpha_signal`, `beta_flux`, and `gamma_resonance`.

2. **Multi-source Data Joining:**
   The raw data is split across multiple CSV files. For each data instance, the features are spread across `signals.csv`, `fluxes.csv`, and `resonances.csv` inside specific directories. You need to join these files on the `instance_id` column to reconstruct the full feature set.

3. **Sanitizer Implementation (Rust):**
   Write a Rust command-line tool located at `/home/user/sanitizer`. The tool should take a directory path as its single argument. 
   For each joined instance in the provided directory, use the baseline parameters extracted in step 1 to compute the log-likelihood of the observation under the Bayesian prior. If the probability falls outside the expected confidence interval (which you will derive to maximize separation), classify it as corrupted.
   The tool must output a single line per `instance_id` to `stdout` in the format: `instance_id: ACCEPT` or `instance_id: REJECT`.

4. **Inference Benchmarking:**
   Adversarial filtering must be fast. Write a short bash script `/home/user/benchmark.sh` that measures the total execution time of your Rust sanitizer on a given directory.

5. **Validation:**
   Test your Rust sanitizer against our two evaluation corpora:
   - `/app/corpus/clean/`
   - `/app/corpus/evil/`
   Your tool must accept all data in the clean corpus and reject all data in the evil corpus based on your probabilistic thresholding. Save the final output of your tool running on both directories to `/home/user/clean_results.txt` and `/home/user/evil_results.txt`.