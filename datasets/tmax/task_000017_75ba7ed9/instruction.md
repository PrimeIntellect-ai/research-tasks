You are an MLOps engineer tasked with building a stateful experiment tracking script for a continuous training pipeline. Our pipeline evaluates new models and streams their metrics. We need a script that processes these metrics, applies Bayesian updates, and finds similar past experiments.

First, you have been provided an audio memo from the lead researcher at `/app/experiment_prior.wav`. You must transcribe or listen to this file to obtain the **prior mean** and **prior variance** for the model scores. 

Next, write a Python script at `/home/user/tracker.py` that reads an arbitrary number of JSON lines from standard input (`sys.stdin`). Each input line represents a model evaluation and has the following schema:
`{"id": "<string>", "score": <float>, "loss": <float>}`

For every model evaluation received, your script must sequentially:
1. **Bayesian Inference:** Calculate the posterior mean of the model's score. Use the prior mean and variance extracted from the audio file. Assume the incoming observation (`score`) has a known observation variance of exactly `0.01`. Calculate the posterior mean using the standard conjugate normal update formula.
2. **Similarity Search:** Find the *previously processed* model from the current stream that is most similar to the current model. Similarity is defined as the minimum Euclidean distance in the 2D `(score, loss)` feature space. If this is the first model processed, the closest past model ID is the string `"NONE"`. If there is a tie in distance, choose the model that appeared first in the stream.
3. **Tabular State Tracking:** Store the current model in the script's internal state so it can be queried by subsequent models.
4. **Output:** Print exactly one JSON line to `sys.stdout` for each input line, containing:
`{"id": "<string>", "posterior_mean": <float_rounded_to_4_decimal_places>, "similar_id": "<string>"}`

*Numerical Accuracy:* The `posterior_mean` must be rounded to exactly 4 decimal places using standard Python `round(val, 4)`.

Your script must perfectly match a hidden reference implementation. An automated verifier will pass a continuous stream of random models to your script's standard input and compare its standard output, bit-for-bit, against the oracle.