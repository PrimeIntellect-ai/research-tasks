You are assisting a performance engineer who is profiling server cooling systems by analyzing the acoustic emissions (audio recordings) of server fans. 

Your task consists of two parts:

Part 1: Audio Artifact Profiling
We have an audio recording of a server fan under load located at `/app/fan_profile.wav`.
Determine the exact duration of this audio file in seconds (using standard CLI tools like `sox`), and write the duration to `/home/user/audio_duration.txt`.

Part 2: Total Variation Distance Tool
To analyze the convergence of an MCMC (Markov Chain Monte Carlo) sampler used for spectral analysis of the fan's sound profile, we need a fast shell tool to compute the Total Variation (TV) distance between two discrete distributions.
Write a bash script at `/home/user/tv_distance.sh` that takes exactly two arguments. 
Each argument is a comma-separated list of non-negative integers (representing unnormalized bin counts from two histograms). The lists will always have the same number of elements (between 2 and 10 elements).
Your script must:
1. Parse the two comma-separated lists.
2. Normalize each list so that the sum of its elements equals 1 (creating probability distributions $P$ and $Q$). If a list sums to 0, output an error message `Invalid input` and exit with code 1.
3. Compute the Total Variation distance: $TV(P, Q) = \frac{1}{2} \sum_{i} |P_i - Q_i|$.
4. Print the resulting TV distance formatted to exactly 4 decimal places.

Ensure your script is executable. You may use `awk` inside your bash script to handle the floating-point math.

Example of expected behavior for Part 2:
`./tv_distance.sh "10,20,10" "5,10,5"` should output `0.0000` (since both normalize to 0.25, 0.5, 0.25).
`./tv_distance.sh "1,0" "0,1"` should output `1.0000`.