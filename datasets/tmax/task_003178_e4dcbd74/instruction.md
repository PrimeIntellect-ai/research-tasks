You are a performance engineer and bioinformatician working on an optimization and data analysis pipeline. 

In `/home/user/`, you will find:
1. `fasta_stats.cpp`: A C++ source file for a tool that parses FASTA files and calculates the GC content of each sequence.
2. `groupA.fasta`: Observational sequence data for condition A.
3. `groupB.fasta`: Observational sequence data for condition B.

Your task is to:
1. Compile the C++ tool from source into an executable named `/home/user/fasta_stats`. Since performance is important, compile it using `g++` with the `-O3` optimization flag.
2. Run the compiled tool on both `groupA.fasta` and `groupB.fasta`. The tool prints data in the format: `SequenceID \t GC_Percentage`.
3. Reshape and process the output using standard shell tools (like `awk`) to calculate the mean GC percentage for both groups.
4. Compare the means to establish a basic statistical hypothesis (whether group A has a higher mean GC content than group B).

Finally, write the results to `/home/user/analysis_report.txt` in exactly the following format (round all floating-point numbers to exactly 2 decimal places):

```
Mean_GroupA: <mean_gc_A>
Mean_GroupB: <mean_gc_B>
Absolute_Difference: <absolute_difference_between_means>
Higher_Group: <"GroupA" or "GroupB">
```

For example:
```
Mean_GroupA: 45.12
Mean_GroupB: 48.33
Absolute_Difference: 3.21
Higher_Group: GroupB
```