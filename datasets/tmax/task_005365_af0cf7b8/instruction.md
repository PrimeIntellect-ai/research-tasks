As a machine learning engineer, I am preparing training data for a predictive maintenance model. The data comes from spectral analysis of machine vibrations. To ensure the model trains only on representative data, I need to filter out machines whose vibration spectrum significantly deviates from a known healthy baseline.

We will use the Total Variation Distance (TVD) as our probability distribution distance metric to compare the normalized frequency spectra (which act as probability mass functions). The null hypothesis is that a machine's spectral distribution matches the healthy baseline. If the TVD between a candidate machine's spectrum and the baseline spectrum is greater than `0.15`, we reject the null hypothesis and exclude that machine from the training set.

The TVD between two discrete probability distributions $P$ and $Q$ is calculated as:
$TVD(P, Q) = \frac{1}{2} \sum_{i} |P(i) - Q(i)|$

Here is the setup:
- The healthy baseline spectrum is located at: `/home/user/baseline_spectrum.txt`
- The candidate machines' spectra are located in the directory: `/home/user/candidates/` (e.g., `machine_A.txt`, `machine_B.txt`)
- All files have the same format: two tab-separated columns. The first column is the frequency bin (e.g., `10Hz`), and the second column is the normalized amplitude (probability), ranging from 0.0 to 1.0. All frequency bins align perfectly across all files.

Your task:
Write and execute a Bash-only pipeline or script (using standard CLI tools like `awk`, `join`, `bash` built-ins) to calculate the TVD for each candidate machine.
Determine which machines have a TVD $\le 0.15$.
Write the base names of the accepted machines (e.g., `machine_A`, without the `.txt` extension) to `/home/user/accepted_machines.log`.
The names in the log file must be sorted alphabetically, with one machine name per line.