You are an AI assistant helping a researcher debug a molecular dynamics simulation component. 

The researcher has a C program `/home/user/sim/sum_potentials.c` that reads a list of floating-point potential energy values from a text file and computes the total energy. 
However, they noticed a critical issue: the simulation produces non-reproducible results. Specifically, when the order of the molecules (and thus the order of the values in the input file) is randomly shuffled, the final computed sum changes due to floating-point reduction order issues (precision loss).

Your task is to:
1. Modify `/home/user/sim/sum_potentials.c` to use **Kahan summation** instead of a naive sum. This algorithmic change will preserve floating-point precision and ensure the sum is reproducible regardless of the input order. Keep the output format exactly as `printf("%.6f\n", sum);`.
2. Write a bash orchestration script `/home/user/sim/orchestrate.sh` that does the following:
   - Compiles `sum_potentials.c` to an executable named `sum_potentials` in the same directory.
   - Uses `shuf` to create a shuffled version of `/home/user/sim/data.txt` named `/home/user/sim/data_shuffled.txt`.
   - Runs `./sum_potentials` on both `data.txt` and `data_shuffled.txt`.
   - Compares the two outputs. If they are exactly identical, write the string `REPRODUCIBLE` to `/home/user/sim/result.log`. If they differ, write `NON-REPRODUCIBLE`.

Make sure `/home/user/sim/orchestrate.sh` is executable. You may run tests in the terminal to ensure your Kahan summation implementation correctly mitigates the precision loss.