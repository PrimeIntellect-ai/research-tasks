I am a bioinformatics researcher working on a novel microfluidic droplet sequencer. We record the sequencer output as a video, where the brightness of each frame corresponds to a fluorescence signal containing nucleotide distribution data. I have a two-part problem I need your help to solve.

First, I need you to analyze a video of a recent sequencing run located at `/app/sequencer_run.mp4`. Use `ffmpeg` to extract the frames and calculate the average grayscale pixel intensity for each frame. The sequence of frame intensities forms our observed signal array. Save this sequence of floating-point numbers (one per line) to `/home/user/extracted_signal.txt`.

Second, we typically compare these signal arrays against theoretical probability distributions using a custom matrix factorization tool, but our compiled C tool fails with a division-by-zero error on near-singular input (when consecutive signals have exactly zero variance). I need you to bypass this by writing a robust Bash script from scratch that computes a simplified discrete Kullback-Leibler (KL) divergence between two given input distributions.

Please write a pure Bash script at `/home/user/kl_divergence.sh`. 
The script must take exactly two arguments, which are paths to two text files. Each text file contains a sequence of integers (1 to 100), representing frequency counts for discrete bins (bin 1 to N, one per line).
Your script must:
1. Normalize both input sequences so that they sum to 1.0 (creating discrete probability distributions P and Q).
2. Calculate the KL divergence: D(P || Q) = sum( P(i) * log2( P(i) / Q(i) ) ).
3. To handle the "near-singular" equivalent of zero probabilities, apply a strict pseudo-count (add 1 to every raw bin count in both P and Q *before* normalizing).
4. Output ONLY the final KL divergence as a floating-point number formatted to exactly 4 decimal places (e.g., `0.0421`). Do not print any other text. You may use `awk` or `bc` within your Bash script for the math.

Once you have written the script, test it. There is an obfuscated reference binary at `/app/oracle_kl` that implements this exact pseudo-count KL divergence logic. An automated verification system will extensively test your `/home/user/kl_divergence.sh` script against the `/app/oracle_kl` binary using hundreds of randomly generated frequency files to ensure bit-exact equivalence.