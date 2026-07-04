You are an MLOps engineer tasked with tracking and reproducing experiment artifacts using shell tools. A previous engineer built an audio-based energy prediction model but introduced a data leak during the normalization phase of their pipeline. Your job is to reconstruct the inference pipeline correctly and estimate the confidence of the predictions using bootstrap sampling—entirely in Bash.

You have been provided with:
1. An audio recording: `/app/recording.wav`
2. A linear model's weights: `/app/weights.csv` (format: `intercept,w_max,w_mean`)

Perform the following steps:

**1. Data Processing & Schema Enforcement**
Create a directory `/home/user/segments/`. Split `/app/recording.wav` into 1-second non-overlapping segments using `ffmpeg` (e.g., `out000.wav`, `out001.wav`, etc.).
For every segment, use the `volumedetect` audio filter in `ffmpeg` to extract the `max_volume` and `mean_volume` (in dB). 
Create a well-formed CSV file at `/home/user/features.csv` with the exact header: `segment_name,max_volume,mean_volume`. Ignore any segments where `volumedetect` fails to produce a `mean_volume` value. Ensure strict schema enforcement (e.g., `-5.4`, not `-5.4 dB`).

**2. Model Architecture Reconstruction & Inference**
Using the weights from `/app/weights.csv`, perform inference for each segment. 
The model is a simple linear regression:
`prediction = intercept + (w_max * max_volume) + (w_mean * mean_volume)`
Calculate the prediction for each segment using standard Bash tools like `awk` or `bc`. Save the results to `/home/user/predictions.csv` with the header `segment_name,prediction`.

**3. Sampling and Bootstrap Estimation**
To estimate the stability of the mean prediction without data leakage, implement a bootstrap sampler in Bash.
- Draw 500 bootstrap samples (with replacement) from your set of predictions. Each bootstrap sample should have the same size $N$ as your number of valid segments.
- Calculate the mean prediction for each of the 500 samples.
- Calculate the overall average of these 500 bootstrap means.
- Save this final single numeric value to `/home/user/final_result.txt`.

Your final output will be verified against a hidden target metric based on the true sample mean. Ensure your extraction and math logic is precise.