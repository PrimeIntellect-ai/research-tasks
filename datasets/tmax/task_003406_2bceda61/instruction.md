You are an AI assistant helping a Machine Learning Engineer prepare text training data for an embedding model.

The engineer needs a fast Go pipeline to sanitize HTML from text files, filter out anomalous data, compute a mock embedding to verify data richness, and benchmark the pipeline's inference speed for experiment tracking.

We have pre-vendored the popular HTML sanitizer `bluemonday` at `/app/vendored/bluemonday`. However, a junior developer accidentally broke something in the vendored package's setup, and it refuses to import correctly when you try to use it with a `replace` directive in your Go module. 

Your tasks:
1. **Fix the Vendored Package**: Identify and fix the perturbation in the `bluemonday` package located at `/app/vendored/bluemonday` so it can be imported.
2. **Write the Pipeline**: Create a Go program at `/home/user/prepare_data.go` that takes three command-line flags:
   - `--corpus`: Path to a directory containing `.txt` files.
   - `--out`: Path to an output directory to write accepted files.
   - `--metrics`: Path to a JSON file to write experiment tracking metrics.
3. **Processing Logic**: 
   For each `.txt` file in the `--corpus` directory:
   - Read the file content.
   - Sanitize it using `bluemonday.StrictPolicy()`.
   - **Filter (Adversarial Check)**: Reject the document (do not write it to `--out`) if:
     a) The sanitized string's length is strictly less than 10 bytes, OR
     b) The sanitized string contains the exact uppercase substring `"REJECT_SPAM"`.
   - **Embedding**: For documents that pass the filter, compute a dummy 5-dimensional embedding vector representing the counts of the vowels (a, e, i, o, u) in the sanitized text (case-insensitive). 
   - Write the sanitized text to the `--out` directory using the same filename as the input.
4. **Experiment Tracking / Benchmarking**: 
   - Measure the total time taken to process the entire directory (from starting the first file to finishing the last).
   - Write a JSON file to the path specified by `--metrics` with the following structure:
     `{"processed_count": <total_files_in_corpus>, "accepted_count": <number_written_to_out>, "duration_ms": <time_in_milliseconds>}`

You must ensure your Go program works flawlessly. The automated test will run your program against a clean dataset (`/home/user/corpora/clean/`) and an evil dataset (`/home/user/corpora/evil/`) to verify your filtering logic and benchmarking output.

Initialise your own Go module in `/home/user/pipeline` and place your code there.