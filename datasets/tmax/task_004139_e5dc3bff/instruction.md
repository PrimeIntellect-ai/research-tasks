You are a bioinformatics analyst working on a legacy sequence processing pipeline. We have a compiled proprietary binary located at `/app/seq_scorer` that processes nucleotide sequences. The original source code was lost. 

This tool performs a form of discrete numerical integration over a sequence (mapping nucleotides to specific numerical weights, calculating the cumulative sum, and then integrating that sum over the length of the sequence). 

Your task is to reverse-engineer the `/app/seq_scorer` binary and implement a bit-exact equivalent in pure Bash or Awk. 

Requirements:
1. Create your solution at `/home/user/my_scorer.sh`.
2. The script must accept a DNA sequence string via standard input (stdin) and output a single integer followed by a newline, matching the binary's output exactly.
3. Make sure `/home/user/my_scorer.sh` is executable.
4. You may use tools like `objdump`, `strings`, `ltrace`, `strace`, or test inputs to deduce the scoring algorithm used by `/app/seq_scorer`.

Hint: The nucleotide weights are small integers (some positive, some negative). Unrecognized characters are ignored or treated as 0 weight.