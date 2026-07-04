You are a data scientist working on an anomaly detection system for a high-energy particle accelerator. We have a set of sensor telemetry readings, and we need to filter out anomalous beam events ("evil" corpus) from normal operations ("clean" corpus).

We have an old legacy simulator, provided as a stripped binary at `/app/telemetry_oracle`. This black-box simulator generates ideal baseline sensor readings for the beam. You can generate a reference sample by running:
`/app/telemetry_oracle --generate <number_of_samples> <output_file.npy>`

We have collected a dataset of experimental sensor readings, stored as 1D numpy float64 arrays in two directories:
- `/home/user/data/clean/`: Contains 50 `.npy` files of normal beam events.
- `/home/user/data/evil/`: Contains 50 `.npy` files of anomalous beam events.

Your task is to:
1. Generate a large reference sample (e.g., 50,000 samples) using the `/app/telemetry_oracle` binary.
2. Analyze the experimental datasets by calculating a probability distribution distance metric (e.g., Wasserstein distance or Kolmogorov-Smirnov statistic) between each experimental file and the baseline reference sample.
3. Visualize your experimental data by creating a plot at `/home/user/threshold_analysis.png`. This plot should show the density distributions of the calculated distances for both the "clean" and "evil" corpora to help you identify a clear threshold boundary.
4. Implement a classifier script at `/home/user/classifier.py`.

The classifier script must have the following signature:
`python3 /home/user/classifier.py <path_to_npy_file>`

It must:
- Load the specified `.npy` file.
- Compare its probability density to the baseline.
- Exit with code `0` if the file is classified as normal (clean).
- Exit with code `1` if the file is classified as anomalous (evil).

You must ensure that your classifier script accurately rejects 100% of the evil corpus and preserves 100% of the clean corpus.