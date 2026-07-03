You are acting as a bioinformatics analyst working on a sequence processing pipeline. 

We have received a plot of a target sequence length distribution from a collaborator, but we only have it as an image file located at `/app/target_distribution.png`. Your first objective is to extract the target mean and standard deviation printed on this plot.

We also have a raw dataset of DNA sequences in FASTA format located at `/home/user/raw_sequences.fasta`. 

Your task is to:
1. Extract the target mean and standard deviation from the image at `/app/target_distribution.png`.
2. Process the `/home/user/raw_sequences.fasta` file using Bash standard tools (awk, grep, sed, etc.) to filter out all sequences whose length falls outside the range of `[mean - standard_deviation, mean + standard_deviation]`.
3. Calculate the new empirical mean length of the filtered sequences.
4. Because our downstream pipeline expects to query these results dynamically, you must write a pure Bash HTTP server (using `nc` or bash built-ins) that listens on `127.0.0.1:8080`.
5. The server must respond to `GET /stats HTTP/1.1` with a `200 OK` status and a JSON payload: `{"empirical_mean": <value>, "sequence_count": <count>}`. 
6. The server must run continuously in the background.

Please ensure the HTTP server strictly handles the request and returns the correct headers and body. You are restricted to standard Bash CLI tools.