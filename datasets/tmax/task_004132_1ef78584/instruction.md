You are a data engineer tasked with building an efficient ETL pipeline in Bash.

We have a legacy audio recording left by the previous senior data engineer that contains the specific configuration parameters for a mathematical transformation pipeline. The recording is located at `/app/pipeline_specs.wav`.

Your task is to:
1. Transcribe or listen to `/app/pipeline_specs.wav` to retrieve the hidden configuration parameters (weights for 3 different streams, and a sampling modulus). You may install any necessary transcription tools (like `openai-whisper` via pip or `ffmpeg`).
2. Write a highly efficient Bash script at `/home/user/etl_transform.sh`.

### Script Requirements:
- The script will receive exactly three positional arguments, which are the file paths for Stream Alpha, Stream Beta, and Stream Gamma respectively: 
  `./etl_transform.sh <alpha.csv> <beta.csv> <gamma.csv>`
- Each input CSV file has no header and contains three comma-separated columns: `id,val1,val2`. `id` is an integer; `val1` and `val2` are floating-point numbers.
- **Transform**: For each stream, multiply `val1` by the first stream-specific weight and `val2` by the second stream-specific weight (as dictated in the audio), then sum these two products to get the `stream_score`.
  *You must process the three streams in parallel* using Bash background jobs (`&` and `wait`) or GNU `parallel`/`xargs` to maximize throughput.
- **Join**: Perform an inner join across all three processed streams on the `id` column.
- **Aggregate**: For each joined row, sum the `stream_score` from Alpha, Beta, and Gamma to calculate the `Total_Score`.
- **Sample/Stratify**: Filter the results to only include rows where the `id` is evenly divisible by the sampling modulus dictated in the audio.
- **Output**: Print the final dataset to standard output in the format `id,Total_Score`. 
  - The `Total_Score` must be formatted to exactly 2 decimal places (e.g., `45.50`).
  - The output must be sorted by `id` in descending numerical order.

Ensure your script is executable (`chmod +x /home/user/etl_transform.sh`). Your script will be tested against a high-volume stream of random CSV files to verify bit-exact outputs.