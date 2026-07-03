You are acting as a research assistant helping to run a 2D fluid/thermal simulation. We need to solve the steady-state 2D heat equation (Laplace's equation, $\nabla^2 u = 0$) on a rectangular domain. 

However, the specific domain dimensions and the non-zero boundary condition for the top edge were given to me in a screenshot by my PI, located at `/app/domain_specs.png`. 

Your task is to:
1. Extract the text from the image `/app/domain_specs.png` (you can use `tesseract /app/domain_specs.png stdout` to read it). It contains the width (`W`), height (`H`), and the boundary condition function for the top edge $u(x, H)$. The other three edges (left, right, bottom) are held at $u=0$.
2. Write a C program from scratch (`/home/user/poisson.c`) that solves this boundary value problem using the finite difference method (e.g., Jacobi or Gauss-Seidel iteration). 
3. Implement a sufficiently fine mesh (domain decomposition) and run your iterative solver until the maximum change between iterations falls below $10^{-6}$. 
4. Extract the computed value of $u(x,y)$ at the exact center of the domain ($x = W/2, y = H/2$). 
5. Write ONLY this single floating-point value to a file named `/home/user/center_value.txt`.

Ensure your C program only uses standard libraries (`stdio.h`, `stdlib.h`, `math.h`) and compiles successfully with standard `gcc`. Do not use external linear algebra libraries. Your mesh must be fine enough (e.g., at least 100x100 points) to accurately capture the analytical physics.