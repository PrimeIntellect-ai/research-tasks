You are a performance engineer analyzing parallel computing scalability (MPI/OpenMP). You have received a scanned fragment of an old performance tuning manual that specifies a custom metric called the Profiling Index (PI).

The image is located at `/app/spec.png`.

Your task:
1. Read the image to extract the exact formula for the Profiling Index (PI).
2. Write a Bash script at `/home/user/calc_pi.sh` that implements this formula.
3. The script must take exactly four positional arguments in this order: `T_seq`, `T_par`, `N`, `C_penalty`.
4. Use standard Bash integer arithmetic (or tools like `awk`/`bc` configured for integers) as required by the spec.
5. The script must print ONLY the final computed integer value to standard output.
6. Ensure your script is executable.

We will verify your script by testing it against thousands of randomly generated performance profiles.