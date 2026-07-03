You are acting as a bioinformatics analyst. We need to implement a Python tool that predicts the steady-state expression level of a synthetic promoter sequence using a specific Ordinary Differential Equation (ODE) model. 

Part of our lab notes containing the model parameters was scanned and saved as an image at `/app/model_params.png`. 

Your task is to:
1. Extract the parameters `alpha`, `beta`, and `n` from the image `/app/model_params.png`. You can use `tesseract` to read the image.
2. Write a Python script at `/home/user/simulate_gene.py` that takes a single DNA sequence string as its first command-line argument.
3. The script must calculate the initial concentration $X_0$ as the GC-content of the sequence: $X_0 = \frac{\text{count}(G) + \text{count}(C)}{\text{length}(\text{sequence})}$. If the sequence is empty, output `0.0000` and exit.
4. Simulate the gene expression $X$ using the Euler method to solve the ODE:
   $$ \frac{dX}{dt} = \alpha \cdot \frac{1}{1 + X^n} - \beta \cdot X $$
   - Use exactly 100 steps.
   - Use a time step `dt = 0.1`.
   - Update rule: `X = X + dt * (alpha * (1.0 / (1.0 + X**n)) - beta * X)`
5. After the 100 steps, print the final value of $X$ to standard output, formatted to exactly 4 decimal places (e.g., `1.2345`). Do not print any other text.

Ensure your script is robust and exactly matches this mathematical specification. The script will be tested against thousands of random DNA sequences to verify bit-exact output equivalence with our reference model.