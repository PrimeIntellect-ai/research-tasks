You are an Machine Learning Engineer preparing a data pipeline to process MCMC (Markov Chain Monte Carlo) training traces. We need a highly optimized, parallelized Go program to filter and summarize these trace files before they are fed into our downstream models.

First, you need to extract the pre-processing hyper-parameters. The lead scientist dictated the parameters for the current batch in an audio recording located at `/app/data/trace_params.wav`. You will need to transcribe this audio file (you can use `ffmpeg` or any standard audio inspection tool available, or simply listen to/transcribe it using an available local utility like `whisper-cli` if installed, or base64 encode it to your local machine to hear it) to discover two integer parameters: the `burn_in` length and the `thinning` factor.

Second, write a Go program at `/home/user/trace_processor.go` and compile it to `/home/user/trace_processor`. 

The program must do the following:
1. Hardcode the `burn_in` and `thinning` factors extracted from the audio.
2. Read data from `stdin`. The first line contains two integers separated by a space: `C` (number of parallel chains) and `L` (length of each chain before filtering).
3. The following `C` lines each contain `L` space-separated integers representing the raw MCMC samples for that chain.
4. Process each chain concurrently using Go routines (parallel computing setup). For each chain:
   - Discard the first `burn_in` samples.
   - From the remaining samples, keep only every `thinning`-th sample (i.e., keep index 0, index `thinning`, index `2*thinning`, etc., relative to the start of the post-burn-in sequence).
   - Compute the sum of the retained samples for this chain.
5. Wait for all Go routines to finish, sum the individual chain totals into a single grand total, and print this final integer to `stdout` followed by a newline.

We will run a strict regression test against a trusted oracle implementation using thousands of fuzzed inputs to ensure your concurrent implementation is bit-exact, race-free, and correctly applies the audio-dictated parameters. 

**Constraints:**
- Use standard Go libraries only.
- Output exactly one integer (the grand total) and a newline. Do not print any debug information to standard out.
- Ensure your concurrency model handles up to `C=100` chains efficiently.