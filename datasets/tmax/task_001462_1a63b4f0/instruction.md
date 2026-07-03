You are an MLOps engineer tasked with fixing an experiment tracking pipeline and creating a robust validator for experiment artifacts.

Currently, our pipeline generates statistical reports and plots for similarity search algorithms, but we are facing three major issues:
1. Our visualization script (`/home/user/plot_results.py`) is failing or producing blank plots in our headless CI environment due to a matplotlib backend misconfiguration.
2. We lost the original configuration file containing the baseline similarity threshold. The only remaining artifact is a screenshot of the old dashboard at `/app/experiment_metadata.png`.
3. Our experiment log repository is polluted with corrupted logs. Some contain mathematically impossible statistical values, while others fall below our baseline similarity threshold.

Your tasks:

**Task 1: Recover Baseline Metric**
Use OCR (tesseract is installed) to extract the baseline similarity threshold from `/app/experiment_metadata.png`. The image contains a string like `MIN_SIMILARITY_SCORE=X.XXX`. 

**Task 2: Fix the Plotting Script**
Modify `/home/user/plot_results.py` or your environment so that when `python3 /home/user/plot_results.py` is executed, it successfully saves a valid plot to `/home/user/artifact_plot.png` without trying to open a GUI window.

**Task 3: Build an Adversarial Log Filter**
Write a Python script at `/home/user/filter_logs.py` that acts as a classifier to validate experiment logs. 
The script must take a single command-line argument: the path to a JSON log file.
It must exit with code `0` if the log is "clean" (valid), and exit with code `1` if the log is "evil" (corrupted or failing criteria).

A log file (JSON format) has the following structure:
```json
{
  "run_id": "exp_123",
  "p_value": 0.045,
  "ci_lower": 0.70,
  "ci_upper": 0.85,
  "similarity_score": 0.82
}
```

A log is considered **EVIL** (reject with exit code 1) if ANY of the following are true:
- `p_value` is outside the inclusive range `[0.0, 1.0]`.
- `ci_lower` is strictly greater than `ci_upper`.
- `similarity_score` is strictly less than the `MIN_SIMILARITY_SCORE` you extracted in Task 1.

A log is considered **CLEAN** (accept with exit code 0) if it passes all the above checks.

Ensure your script is robust and correctly implements these statistical and similarity constraints. An automated test suite will run your filter against a hidden corpus of clean and evil logs.