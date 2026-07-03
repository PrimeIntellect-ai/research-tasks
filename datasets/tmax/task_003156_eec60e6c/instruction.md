You are an MLOps engineer tasked with automating an experiment tracking pipeline. An existing Python analysis script performs linear algebra operations on tokenized data to compute term embeddings and generates a visualization, but it currently fails to run in our headless CI/CD environment because of matplotlib backend misconfigurations (it tries to open a GUI window). 

Additionally, the raw data needs to be tokenized before the Python script can run, and the execution environment must be built dynamically.

Write a Bash orchestration script at `/home/user/run_pipeline.sh` that performs the following steps:

1. **Tokenization (Dataset Preparation):**
   Read the raw text file located at `/home/user/data/raw.txt`. Convert all text to lowercase, remove all punctuation (except spaces), and split the text so that each word is on its own line. Save the resulting tokens to `/home/user/data/tokens.txt`.

2. **Analysis Environment Setup:**
   Create a Python virtual environment at `/home/user/venv`. Activate it, and install `numpy` and `matplotlib`. 

3. **Execution and Artifact Generation:**
   Run the provided Python script located at `/home/user/scripts/analyze.py`. 
   You must ensure that the script does not attempt to open a graphical display (which causes it to crash in this headless environment) by setting the appropriate environment variable for the Matplotlib backend before executing the Python script.

4. **Artifact Tracking:**
   The Python script will output two files: `/home/user/artifacts/plot.png` and `/home/user/artifacts/eigen_metrics.txt`. Make sure these directories exist before running the script. Your bash script should print "Pipeline completed successfully" at the very end.

Ensure `/home/user/run_pipeline.sh` is executable. You can assume `python3` and `pip` are available on the system.