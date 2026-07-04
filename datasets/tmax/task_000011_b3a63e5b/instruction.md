You are tasked with recovering an experiment's lost target variables from an audio dictation and performing a statistical bootstrap analysis in C++.

We have a dataset with a single feature `X` for 50 samples located at `/home/user/data/features.csv`. 
The target variable `Y` was lost due to a database corruption, but a researcher recorded an audio log dictating the 50 `Y` values in their exact sequence. This audio file is available at `/app/experiment_targets.wav`.

Your goals are:
1. **Environment Setup & Transcription:** Set up the necessary tools (e.g., `whisper` via Python, or any other method) to transcribe the audio file. Extract the 50 numerical values spoken in the audio and pair them with the corresponding `X` values from the CSV.
2. **C++ Implementation:** Write a C++ program (`/home/user/analysis.cpp`) that reads your recovered (X, Y) dataset. Your program must:
   - Implement Pearson correlation calculation from scratch (no external math libraries other than standard C++ library).
   - Implement a Bootstrap resampling method to estimate the 95% Confidence Interval (CI) of the Pearson correlation coefficient between X and Y. Use $B=10,000$ bootstrap iterations. 
   - Use the percentile method to determine the lower (2.5th percentile) and upper (97.5th percentile) bounds of the correlation CI. Seed your random number generator with `42` (`std::mt19937 gen(42);`) to ensure reproducible sampling.
3. **Tracking & Reporting:** Output the results to a JSON file located at `/home/user/metrics.json` with exactly this format:
```json
{
  "ci_lower": -0.1234,
  "ci_upper": 0.5678
}
```

Constraints:
- You must write the analysis logic in C++. You can use bash or Python to handle the transcription and data preparation.
- Ensure the C++ program correctly handles random index sampling with replacement.

Once you have generated the `/home/user/metrics.json` file, the task is complete.