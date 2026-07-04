You are a data engineer tasked with building an ETL pipeline to process audio transcripts containing field telemetry measurements. 

Your workflow has two parts:
1. **Audio Analysis**: You have been provided an audio file at `/app/telemetry.wav`. It contains spoken measurements from a field operative. A transcription utility is available at `/app/transcribe.sh`. Use it to transcribe the audio and understand the general format of the data you are dealing with.

2. **Pipeline Implementation (Go)**:
You must write a Go program that processes transcript text (read from `stdin`) and outputs a structured JSON summary. The verifier will rigorously test your compiled binary against a reference oracle to ensure absolute bit-exact equivalence on thousands of random inputs.

Create a Go source file at `/home/user/main.go` and compile it to `/home/user/pipeline`.

**Data Processing Specifications for the Go Program:**
- Read the entire standard input as a single string.
- **Tokenization**: Split the input text into tokens strictly by whitespace (spaces, tabs, newlines).
- **Feature Extraction**: Iterate through the tokens and attempt to parse each as a 64-bit float. Discard any tokens that cannot be parsed as a float.
- **Statistical Modeling (Hypothesis Testing & Confidence Intervals)**:
  - Count the number of valid float measurements ($N$).
  - If $N < 2$, print strictly: `{"error": "insufficient data"}` and exit with code 0.
  - Calculate the sample mean.
  - Calculate the sample standard deviation using Bessel's correction (divide by $N-1$).
  - Calculate the 95% Confidence Interval for the mean using the normal approximation: $CI = \text{mean} \pm 1.96 \times \left(\frac{\text{stddev}}{\sqrt{N}}\right)$.
- **Classification**:
  - If the lower bound of the 95% CI is strictly greater than `10.0`, the classification is `"CRITICAL"`.
  - Otherwise, it is `"NORMAL"`.
- **Output Format**:
  Print a JSON object to `stdout` (no trailing newline required, but standard JSON serialization is expected) with exactly these keys:
  `{"mean": 12.3456, "stddev": 1.2345, "ci_lower": 11.1234, "ci_upper": 13.5678, "class": "NORMAL"}`
  *All floating-point numbers in the output JSON must be rounded to exactly 4 decimal places before serialization.*

You can test your logic by comparing your binary's output against the reference binary at `/app/oracle_pipeline` using echo/stdin. Once your binary perfectly matches the oracle's specifications, your task is complete.