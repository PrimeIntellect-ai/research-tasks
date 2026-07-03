You are a bioinformatics analyst studying sequence state transitions. You have been provided with an image file at `/app/transition_matrix.png` that contains a table representing the transition probability matrix of a Markov chain between four sequence states (S1, S2, S3, and S4). 

Your task is to:
1. Extract the transition probabilities from the image (you may use `tesseract` or any other tool available to you).
2. Create a Bash script at `/home/user/simulate.sh` that performs a Monte Carlo simulation of a random walk on this state network.

The script must meet the following requirements:
- The script must be executable (`chmod +x`).
- The first argument to the script will be the initial state (e.g., `S1`).
- The subsequent arguments will be a series of random floating-point numbers between 0 and 1.
- For each random number, determine the next state based on the current state's transition probabilities.
- The cumulative probability intervals must be evaluated in the exact order: S1, S2, S3, S4. 
- An interval is defined as `[lower, upper)`. A random number `r` triggers the transition if `lower <= r < upper`. (Test inputs will avoid exact boundary collisions to prevent floating-point precision issues).
- The script must output a single space-separated line containing the sequence of visited states, starting with the initial state and followed by the subsequent states for each random number provided.

Example invocation:
`/home/user/simulate.sh S1 0.05 0.45 0.8`

Example output (if S1->S1 was 0.1, S1->S2 was 0.4, etc.):
`S1 S1 S2 S4`

Ensure your script is robust and correctly applies the transition logic for any sequence of inputs.