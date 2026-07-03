You are tasked with fixing and completing an ETL processing pipeline for a data engineering team. We have a stream of numerical pairs that occasionally contains missing values (a silent data corruption issue where values were dropped), and we need to compute a rolling Pearson correlation coefficient over this stream to identify feature similarity over time.

First, you must determine the pipeline's configuration parameters. They were left by a former engineer in an audio voice memo located at `/app/memo.wav`. 
Transcribe the audio file to discover two crucial configuration values:
1. `W`: The rolling window size (an integer).
2. `V`: The imputation value for missing data (a float).

Once you have these parameters, write a Go program at `/home/user/pipeline.go` and compile it to `/home/user/pipeline`. 

**Pipeline Program Specifications:**
- Read a CSV stream from `stdin`. Each line contains two columns: `X,Y`. 
- The values are floats. Occasionally, a value might be missing (represented by an empty string, e.g., `1.2,`, `,3.4`, or `,`).
- Whenever `X` or `Y` is missing, impute (replace) the missing value with the constant `V` obtained from the audio memo.
- Maintain a rolling window of the most recent `W` rows (after imputation).
- For each new row, starting only when you have exactly `W` rows in your window (i.e., from the `W`-th row onwards), compute the Pearson correlation coefficient between the `X` values and `Y` values currently in the window.
- If the variance of either `X` or `Y` in the current window is 0 (making correlation undefined), output `0.0000`.
- Print the computed correlation coefficient for each valid window to `stdout`, one per line, formatted exactly to 4 decimal places (e.g., `0.1234`, `-0.9876`). Do not print anything else.

Compile your program so that it can be executed as `/home/user/pipeline`. The automated verification suite will pipe thousands of randomized CSV lines into your binary and compare its output bit-for-bit against a reference implementation.

You may use any tools (like `whisper`, `ffmpeg`, or Python libraries like `SpeechRecognition`) to process the audio file.