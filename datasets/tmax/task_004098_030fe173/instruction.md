You are an MLOps engineer tasked with fixing a broken pipeline that tracks experiment artifacts. Recently, several large-scale data storage shards containing tokenization metrics have been corrupted, causing downstream numerical libraries (like matplotlib) to produce blank plots due to anomalous covariance bounds. 

The chief engineer left a voice note explaining the exact statistical threshold for the anomaly. 
1. Transcribe or listen to the audio file located at `/app/voicenote.wav` to discover the filtering rule.
2. Write a Go command-line tool at `/home/user/detect_anomaly.go` that reads a tabular TSV dataset.
3. The TSV datasets have a header and three columns: `shard_id`, `token_count`, and `latency_ms`.
4. Your Go script must parse the TSV, perform the statistical correlation analysis specified in the audio file between `token_count` and `latency_ms`, and determine if the dataset is corrupted.
5. If the file violates the condition (i.e., it is a corrupted/anomalous run), your script must exit with status code `1` (reject). If the file is valid, it must exit with status code `0` (accept).

The system will verify your script against a hidden suite of datasets. Your script must accept the file path as its first positional argument, like so:
`go run /home/user/detect_anomaly.go <path_to_tsv_file>`

Ensure your Go code correctly handles standard TSV parsing and computes the required numerical correlation accurately without using external statistical libraries (use standard library math).