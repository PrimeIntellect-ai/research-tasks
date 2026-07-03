You are a bioinformatics analyst working on a novel sequence optimization project. You have been provided with the source code for a proprietary sequence evaluation tool, but it needs to be compiled and integrated into a Python-based optimization pipeline.

Here is what you need to do:

1. **Environment Setup**: Create a Python virtual environment at `/home/user/venv` and install `numpy` in it.
2. **Compilation**: In `/home/user/motif_project/`, you will find a C source file named `scorer.c`. Compile it using `gcc` into an executable named `scorer` in the same directory. This tool takes a single DNA sequence string as a command-line argument and prints its motif score to standard output.
3. **Sequence Optimization**: Write a Python script at `/home/user/motif_project/optimize.py` that uses a Monte Carlo optimization approach (e.g., simulated annealing or a genetic algorithm) to find a DNA sequence (consisting only of characters 'A', 'C', 'G', 'T') of exactly 50 base pairs in length that achieves a score of **150 or higher** when evaluated by the `./scorer` executable. 
4. **Results**: Once your script finds a sequence that meets or exceeds the score of 150, save the result to `/home/user/motif_project/optimized_sequence.txt`. 

The `optimized_sequence.txt` file must be formatted exactly like this (with your actual sequence and score):
```
Sequence: ATGCGT... [exactly 50 characters]
Score: 165
```

Ensure that you use the Python interpreter from your newly created virtual environment to run your optimization script.