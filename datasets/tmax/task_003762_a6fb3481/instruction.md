You are a bioinformatics analyst tasked with calculating the theoretical isoelectric point (pI) of several proteins from their amino acid sequences and statistically comparing these theoretical values to experimentally measured pI values.

The pI is the pH at which a protein's net charge is exactly zero. You will need to calculate the net charge of a protein sequence as a function of pH, and then solve for the root of this non-linear equation (e.g., using `scipy.optimize`). 

**1. The Net Charge Formula:**
The net charge $Q$ at a given $pH$ is calculated by summing the contributions of the basic and acidic groups:
$Q(pH) = \sum_{i \in \text{Basic}} \frac{N_i}{1 + 10^{pH - pKa_i}} - \sum_{j \in \text{Acidic}} \frac{N_j}{1 + 10^{pKa_j - pH}}$

Where:
* $N$ is the count of a specific group in the sequence.
* Every sequence has exactly one N-terminus (Basic) and one C-terminus (Acidic).
* **Basic groups (and their pKa values):** N-terminus (8.6), K (10.8), R (12.5), H (6.5)
* **Acidic groups (and their pKa values):** C-terminus (3.6), D (3.9), E (4.1), C (8.5), Y (10.1)

*(Note: Ignore any other amino acids for charge calculations, as they are neutral. Assume every sequence is linear and unmodified).*

**2. Input Data:**
* You have a FASTA file at `/home/user/proteins.fasta` containing several protein sequences.
* You have a CSV file at `/home/user/experimental_pi.csv` containing two columns: `Protein_ID` and `Experimental_pI`.

**3. Tasks:**
1. Parse the FASTA file and count the relevant basic and acidic groups for each sequence.
2. For each sequence, define the charge function $Q(pH)$ and use a non-linear root-finding algorithm (e.g., `scipy.optimize.brentq`) to find the pH value between 0.0 and 14.0 where $Q(pH) = 0$. This is the calculated theoretical pI.
3. Match the calculated theoretical pIs with the experimental pIs from the CSV using the Protein IDs.
4. Perform a paired t-test (two-sided) comparing the calculated theoretical pIs against the experimental pIs using `scipy.stats.ttest_rel`.
5. Write the results to a JSON file at `/home/user/pi_results.json` matching exactly this structure:
```json
{
  "calculated_pis": {
    "SEQ1": 6.12,
    "SEQ2": 5.43
  },
  "t_statistic": 1.2345,
  "p_value": 0.0456
}
```
*Constraints for JSON output:*
* Round the calculated pI values in the dictionary to exactly 2 decimal places.
* Round the `t_statistic` and `p_value` to exactly 4 decimal places.
* Ensure the keys in `calculated_pis` match the FASTA headers (without the `>`).