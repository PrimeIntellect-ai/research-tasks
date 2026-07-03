You are an MLOps engineer tasked with validating tracking artifacts from our latest model experiments. We've been receiving corrupted or manipulated experiment logs, and we need a robust, statistically-grounded filter to distinguish valid ("clean") logs from corrupted/adversarial ("evil") ones.

First, you need to retrieve the baseline experiment parameters. The lead researcher left a voice memo detailing the expected baseline metrics. It is located at `/app/experiment_readout.wav`. You must transcribe this audio to find the baseline mean inference time (in milliseconds).

Next, develop a Python CLI tool at `/home/user/artifact_filter.py` that evaluates a single JSON experiment log. 
The script must be invoked as:
`python /home/user/artifact_filter.py <path_to_json_file>`

Each JSON log contains a list of floats under the key `"inference_times"`. 
Your script must output exactly the word `CLEAN` or `EVIL` to standard output (with no other text) based on the following rules:
1. Output `EVIL` if the `"inference_times"` key is missing, empty, or contains non-numeric values.
2. Output `EVIL` if the statistical distribution of the inference times is significantly shifted from the baseline. Specifically, you must perform a 1-sample T-test on the array of inference times against the baseline mean extracted from the audio file. If the two-tailed p-value is strictly less than `0.01`, flag it as `EVIL`.
3. If the file passes these checks, output `CLEAN`.

You have been provided with two directories for local development and testing:
- `/app/corpora/clean/`: Contains known valid experiment logs.
- `/app/corpora/evil/`: Contains logs that are corrupted, manipulated, or statistically divergent.

Ensure your numerical libraries (e.g., `scipy`) are properly configured to run this test reliably. The automated verifier will test your script against all files in both corpora (and potentially hidden holdouts) using the exact CLI invocation specified above.