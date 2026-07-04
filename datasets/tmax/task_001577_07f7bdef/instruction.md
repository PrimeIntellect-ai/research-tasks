You are a scientific researcher working with a small, highly collinear observational dataset. You need to estimate the parameters of a linear model, but standard ordinary least squares (OLS) matrix factorization fails or is highly unstable due to the near-singular design matrix.

To resolve this, you have decided to use a Bayesian approach with a Gaussian prior, which acts as a ridge regularization and ensures the posterior distribution is proper and the equations are well-conditioned.

Your tasks are:
1. Reshape and read the observational data provided in `/home/user/observations.txt`. The file uses a custom format where each line is `y;x1;x2`.
2. The model is $y_i = \beta_1 x_{i1} + \beta_2 x_{i2} + \epsilon_i$, where $\epsilon_i \sim \mathcal{N}(0, 1)$.
3. The prior on the parameters is an independent Gaussian $\boldsymbol{\beta} \sim \mathcal{N}(0, 10\mathbf{I})$. This implies a prior precision matrix $\Lambda_0 = 0.1\mathbf{I}$.
4. Write a C program at `/home/user/posterior.c` that parses this dataset and analytically computes the exact mean of the posterior distribution for $\boldsymbol{\beta}$. The analytical posterior mean for this Bayesian linear regression is given by:
   $\boldsymbol{\mu} = (X^T X + 0.1\mathbf{I})^{-1} X^T \mathbf{y}$
5. Your C program should print the computed posterior means for $\beta_1$ and $\beta_2$ and also save them to `/home/user/posterior_result.txt` in exactly this format:
   `beta1=X.XXX, beta2=X.XXX`
   (Round the values to exactly 3 decimal places).

Ensure your C code compiles cleanly (e.g., using `gcc -o posterior posterior.c`) and runs without errors. Use standard C libraries.