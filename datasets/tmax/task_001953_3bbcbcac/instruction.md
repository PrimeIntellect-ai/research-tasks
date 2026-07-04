Hello, I am a researcher working on simulating protein folding energies. I need you to implement a command-line script that calculates a numerical energy score for a given amino acid sequence and a set of structural optimization parameters. 

We are optimizing weights using a simplex algorithm, so the inputs to your script can be quite extreme (up to +/- 1000.0).

Here is what you need to do:
1. First, listen to the voice note left by my postdoctoral researcher at `/app/voicenote.wav`. She explains the updated amino acid groupings we are using for this specific simulation, as well as a required "baseline shift" constant. You will need to transcribe or listen to this audio to get the correct rules.
2. Write a Python script at `/home/user/evaluator.py`.
3. The script must accept exactly four positional arguments:
   `python3 /home/user/evaluator.py <sequence> <x> <y> <z>`
   - `<sequence>`: A string of uppercase amino acid characters (e.g., `ACDEFGHIKLMNPQRSTVWY`).
   - `<x>`: Float weight for Hydrophobic residues.
   - `<y>`: Float weight for Polar residues.
   - `<z>`: Float weight for Charged residues.
4. The script should compute the energy function:
   `Energy = (x * H_count) + (y * P_count) + (z * C_count) + ln(e^x + e^y + e^z) + baseline_shift`
   Where `H_count`, `P_count`, and `C_count` are the number of hydrophobic, polar, and charged residues in the sequence respectively, according to the rules in the voice note. If an amino acid does not fall into one of these three categories (as defined in the voice note and standard remaining assignments), it contributes to none of the counts. Standard charged are R, H, K, D, E. Standard polar are S, T, N, Q. 
5. **Numerical Stability Warning:** Since `x`, `y`, and `z` can be large positive numbers (up to 1000.0), a naive implementation of `ln(e^x + e^y + e^z)` will cause a floating-point overflow error in Python (`math.exp` raises an `OverflowError`). You must implement a numerically stable version of this log-sum-exp calculation.
6. The script should print ONLY the final energy score to standard output, rounded to exactly 4 decimal places (e.g., `1425.1234`).

Once you have written and tested `/home/user/evaluator.py` to ensure it correctly handles large inputs without crashing and uses the rules from the audio file, you are done. An automated fuzzer will test your script against my reference binary with hundreds of random inputs to ensure it is perfectly equivalent.