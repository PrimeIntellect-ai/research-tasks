You are an artifact manager responsible for curating binary repositories. We have received a new raw audio artifact located at `/app/artifact_raw.wav`. To optimize storage in our repository, we need to extract the raw audio payload, stripping away the metadata, and compress it using standard stream processing.

Your task is to:
1. Write a Python script that opens `/app/artifact_raw.wav` and uses memory-mapped I/O (`mmap`) to efficiently access the file contents.
2. The script must skip the standard 44-byte WAV header and write the remaining raw audio bytes directly to standard output (`sys.stdout.buffer`) in a streaming fashion.
3. Use a shell command to execute your Python script and pipe its standard output directly into `gzip`, redirecting the compressed stream to a new file at `/home/user/artifact_payload.gz`.

Ensure your Python script reads and outputs the data reliably. The automated test will evaluate the operation by decompressing `/home/user/artifact_payload.gz`, comparing it against the original WAV file's data chunk, and measuring the Mean Squared Error (MSE) of the reconstructed audio. The final compressed archive must strictly contain only the gzipped raw audio bytes.