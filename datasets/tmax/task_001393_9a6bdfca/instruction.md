You are tasked with building a parameter estimation tool in C++. 

We have received a voice memo from the senior data scientist at `/app/instructions.wav` detailing the exact model fitting procedure we need to implement. The memo describes a non-linear equation that relates the sample mean of our data to a parameter $\theta$, and specifies the exact numerical method and parameters to use to find $\theta$.

Your tasks are:
1. Listen to or transcribe the audio file located at `/app/instructions.wav` to understand the mathematical model and the specific solver instructions.
2. Write a C++ program at `/home/user/fitter.cpp`.
3. The program should read an arbitrary number of whitespace-separated floating-point numbers from standard input until EOF.
4. It must compute the required parameter $\theta$ exactly as instructed in the audio, without using any external root-finding libraries (implement the numerical method yourself).
5. Compile your program to an executable named `/home/user/fitter`.
6. The program must print the final estimated parameter to standard output, formatted to exactly 6 decimal places (e.g., `1.234567`), followed by a newline.

Ensure your program is robust and exactly matches the requested number of iterations and initial conditions, as it will be rigorously tested against a reference implementation with thousands of random inputs.