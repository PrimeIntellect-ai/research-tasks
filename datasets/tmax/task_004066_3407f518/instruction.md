You are a performance engineer tasked with optimizing and profiling a Monte Carlo simulation pipeline. 

Your goals are to transcribe an audio directive, compile and profile a mathematical simulation, and serve the profiling results via a custom Bash HTTP server.

Step 1: Extract the Configuration from Audio
You have been provided an audio file at `/app/directive.wav`. This file contains spoken instructions detailing the integer "seed" value you must use for the Monte Carlo simulation. Transcribe this audio (you may install tools locally in your environment, such as `ffmpeg` or Python audio libraries, to accomplish this) and extract the integer seed.

Step 2: Compile the Simulation
In `/home/user/mc_sim.c`, there is a C program that estimates Pi using a Monte Carlo method. It accepts two arguments: the random seed, and the number of threads.
Compile this program from source, enabling OpenMP support. Name the compiled executable `/home/user/mc_sim`.

Step 3: Profile the Simulation (Observational Data Reshaping)
Write a Bash script, `/home/user/profiler.sh`, that runs `/home/user/mc_sim` using the seed extracted from the audio, for thread counts 1, 2, and 4. 
For each run, capture the estimated Pi value (printed to stdout) and the wall-clock execution time. 
Identify which thread count resulted in the lowest wall-clock time.

Step 4: Serve the Results (Integration)
Create a Bash-based HTTP server (e.g., using `nc` or `socat` in a loop) listening exactly on `127.0.0.1:8000`. 
When a client sends an `HTTP GET` request to the `/data` endpoint, your server must respond with a valid `HTTP/1.1 200 OK` header followed by a JSON payload in this exact format:
`{"seed": <extracted_seed_integer>, "pi": <pi_estimation_result_from_4_threads>, "fastest_thread_count": <int>}`

Ensure your server runs continuously in the background so it can be verified.