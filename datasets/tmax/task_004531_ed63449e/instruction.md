You are a release manager preparing a new deployment. The backend routing configuration has been dictated in an audio memo located at `/app/deployment_weights.wav`. This memo contains the integer load-balancing weights for our new API routes.

Your task:
1. Transcribe the audio file `/app/deployment_weights.wav`. You may use the `whisper` CLI tool (which is installed in the environment) to generate the transcription.
2. Read the transcription and identify the numerical integer weights dictated for the servers.
3. Treat these weights as an unnormalized probability distribution. Implement a short script (in Python, awk, or bash) to normalize these weights so they sum to 1.0, and then calculate the Shannon entropy of this distribution in nats (using the natural logarithm).
4. Output the final entropy value as a single floating-point number to a file named `/home/user/entropy_result.txt`.

For example, if the audio says "Route A gets weight twenty, route B gets weight thirty, route C gets weight fifty", the weights are 20, 30, 50. The normalized probabilities are 0.2, 0.3, 0.5. The entropy would be calculated as: -(0.2 * ln(0.2) + 0.3 * ln(0.3) + 0.5 * ln(0.5)).

Write only the final numerical float value into `/home/user/entropy_result.txt`.