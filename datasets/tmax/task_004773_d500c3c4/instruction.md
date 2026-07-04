You are acting as a support engineer investigating a hanging batch job. 

We have a Go program located at `/home/user/collatz/main.go` that is supposed to read a list of integers from `/home/user/collatz/inputs.txt` and calculate the number of steps required to reach 1 according to the Collatz conjecture. 

Recently, the input data source was corrupted, and it occasionally includes zero or negative numbers. When the program encounters these, it hangs in an infinite loop because the standard Collatz sequence does not terminate at 1 for non-positive integers. 

Your task:
1. Diagnose and fix the infinite loop issue in `/home/user/collatz/main.go`.
2. Modify the `collatzSteps` function so that if the input is `<= 0`, it immediately returns `-1`.
3. Ensure the main loop writes `Input: <N>, Steps: Invalid` to `/home/user/collatz/output.txt` if the steps returned is `-1`. Otherwise, it should write `Input: <N>, Steps: <S>`.
4. Compile and run the fixed program so that `/home/user/collatz/output.txt` is successfully generated with the correct evaluations for all inputs in `inputs.txt`.

Do not change the file paths. Ensure the program handles the exact inputs gracefully and completes successfully.