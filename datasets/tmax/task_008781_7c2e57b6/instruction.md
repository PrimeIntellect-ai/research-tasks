You are an ETL data engineer building a lightweight streaming inference pipeline. We need to deploy a probabilistic anomaly detection step that reconstructs a pre-trained linear model and updates probabilities using Bayesian inference. 

You have been provided with raw system metrics, pre-trained model weights, and historical prior probabilities in `/home/user/pipeline/`.

Your task is to write a script (in any language) to process the raw metrics, perform inference, and identify the most anomalous requests.

Here is the specification for the inference pipeline:
1. Read `/home/user/pipeline/raw_metrics.csv`.
2. **Feature Engineering**: For each row, calculate two features:
   - `X1` = `payload_size / 1024`
   - `X2` = `compute_cycles / 1000000`
3. **Model Reconstruction (Linear Algebra)**: Read weights from `/home/user/pipeline/model_weights.json`. Calculate the logit `z` for each request:
   `z = (w1 * X1) + (w2 * X2) + bias`
4. **Probabilistic Modeling**: Transform the logit into an anomaly likelihood `L(Anomaly)` using the sigmoid function: `1 / (1 + e^-z)`. Assume the normal likelihood `L(Normal)` is `1 - L(Anomaly)`.
5. **Bayesian Inference**: Read the prior probabilities from `/home/user/pipeline/priors.json` (`P_Anomaly` and `P_Normal`). Calculate the posterior probability of each request being an anomaly using Bayes' theorem:
   `Posterior(Anomaly) = (L(Anomaly) * P_Anomaly) / (L(Anomaly) * P_Anomaly + L(Normal) * P_Normal)`
6. **Inference Benchmarking**: Time how long it takes to process the entire dataset (steps 2-5) for a single batch run. Write the elapsed time (in milliseconds, as a float) to `/home/user/pipeline/benchmark.txt`.
7. **Extraction**: Identify the top 3 `request_id`s with the highest `Posterior(Anomaly)`. 

Write the top 3 `request_id`s, one per line, sorted in descending order of their posterior anomaly probability, to `/home/user/pipeline/anomalies.txt`.