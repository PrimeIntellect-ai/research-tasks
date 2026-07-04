You are acting as a Machine Learning Engineer preparing a dataset for an edge-device model that requires highly reproducible data pipelines. You need to write a C program that reads a dataset of floating-point numbers, tokenizes (quantizes) them into integer bins, and performs bootstrap sampling to generate a new training set.

Write a C program at `/home/user/prepare_data.c` that does the following:
1. Accepts two command-line arguments: the input file path and the output file path.
   Usage: `./prepare_data <input_file> <output_file>`
2. Reads floating-point numbers from the input file (one per line). Let the total number of values be $N$.
3. Finds the minimum ($min$) and maximum ($max$) values in the dataset.
4. Tokenizes each float $x$ into an integer token $T$ in the range [0, 255] using Min-Max quantization:
   $T = \lfloor \frac{x - min}{max - min} \times 255 \rfloor$
   (If $x = max$, $T$ should be exactly 255).
5. To test pipeline reproducibility, you must use a fixed custom pseudo-random number generator (PRNG) to perform bootstrap sampling. Implement this exact PRNG:
   ```c
   unsigned int state = 42; // Initial seed
   unsigned int my_rand() {
       state = (state * 1103515245 + 12345) & 0x7FFFFFFF;
       return state;
   }
   ```
6. Create a bootstrapped dataset of size $N$ by sampling with replacement from the tokenized dataset. The index for each sample (from 0 to $N-1$) should be chosen using `my_rand() % N`. Do this $N$ times.
7. Write the resulting bootstrapped integer tokens to the output file, one per line.

The input file is located at `/home/user/raw_data.txt`.
Once you have written the C program, compile it into an executable named `prepare_data` in `/home/user/` and run it to produce `/home/user/bootstrapped_tokens.txt`.