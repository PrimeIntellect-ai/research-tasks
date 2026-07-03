You are a data scientist cleaning a large dataset of sensor readings. You have been given a binary file `/home/user/sensor_data.bin` containing millions of sensor records. 

Unfortunately, the sensors periodically experience hardware glitches that corrupt the readings. Your task is to write a C program that processes this binary file, evaluates the probability that each record is a glitch using a Naive Bayes model, and filters out the corrupted data.

**Data Format**
The file `/home/user/sensor_data.bin` is a packed binary file consisting of sequential records. Each record is 16 bytes and corresponds to the following C struct:
```c
#include <stdint.h>
struct Record {
    int32_t id;
    float temp;
    float humidity;
    int32_t status;
};
```

**Bayesian Glitch Model**
Through prior evaluation, we have established the following probabilistic model for glitches ($G$ represents a glitch, $\sim G$ represents a clean record):

1. **Prior Probabilities:**
   * $P(G) = 0.10$
   * $P(\sim G) = 0.90$

2. **Evidence 1 ($E_1$): Temperature Extreme**
   A temperature extreme is defined as `temp < 0.0` or `temp > 50.0`.
   * $P(E_1 | G) = 0.80$
   * $P(E_1 | \sim G) = 0.05$
   * $P(\sim E_1 | G) = 0.20$
   * $P(\sim E_1 | \sim G) = 0.95$

3. **Evidence 2 ($E_2$): Status Flag**
   A status flag anomaly is defined as `status != 0`.
   * $P(E_2 | G) = 0.70$
   * $P(E_2 | \sim G) = 0.10$
   * $P(\sim E_2 | G) = 0.30$
   * $P(\sim E_2 | \sim G) = 0.90$

Assume $E_1$ and $E_2$ are conditionally independent given $G$. 

**Requirements**
1. Write a C program (e.g., `cleaner.c`) and compile it.
2. The program must iterate through `/home/user/sensor_data.bin`.
3. For each record, calculate the posterior probability of a glitch: $P(G | E_1, E_2)$. 
4. If $P(G | E_1, E_2) \ge 0.5$, consider the record corrupted. Otherwise, it is clean.
5. Write all **clean** records (in the same binary struct format) to a new file at `/home/user/clean_data.bin`.
6. Count the total number of clean records and write this integer (just the number, no other text) to `/home/user/summary.txt`.