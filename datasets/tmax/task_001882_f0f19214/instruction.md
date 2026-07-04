I am an ML engineer preparing a training dataset for our next pipeline. We need to filter out anomalous "evil" data samples that could poison the model. 

I've been given an image of a handwritten note containing the parameters of a simple anomaly-detection perceptron model. The image is located at `/app/architecture.png`.

I need you to:
1. Extract the model architecture, weights, and anomaly condition from `/app/architecture.png` (using OCR or other tools).
2. Reconstruct this model inference logic purely in a Bash script located at `/home/user/detect_anomaly.sh`. 
   - The script must take a single argument: the path to a JSON file.
   - The JSON file will have the format `{"x": <float>, "y": <float>}`.
   - The script should parse the JSON, run the perceptron math, and exit with `0` if the sample is clean, or exit with `1` if the sample is an anomaly.
3. Write a second Bash script `/home/user/bootstrap_bench.sh` that takes a directory path as an argument.
   - This script should perform a bootstrap sampling procedure: randomly select 50 files (with replacement) from the given directory.
   - For each sampled file, run `./detect_anomaly.sh`.
   - Measure the total inference time for running these 50 samples and write the total time (in milliseconds) to `/home/user/bench.log`.

You can test your anomaly detector against the sample corpora provided in `/app/corpus/clean/` and `/app/corpus/evil/`. 
Ensure your detector is 100% accurate on this dataset before concluding. Your `detect_anomaly.sh` script must output NO text to standard output unless for your own debugging (only the exit code matters).