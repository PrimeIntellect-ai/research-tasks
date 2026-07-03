You are an automation specialist tasked with building a robust C++ log processing workflow. 

You have been given a raw log file located at `/home/user/system_events.txt`. This file contains millions of system events, but some lines are corrupted due to network transmission errors.

Your objective is to write a C++ program that reads this file, validates the entries, groups the data, detects sudden drops in activity (anomalies/changepoints), and writes the results to an output file.

**Step 1: Write the C++ Program**
Create a C++ program at `/home/user/process_logs.cpp`. The program must take two command-line arguments: the input file path and the output file path.
`./process_logs <input_file> <output_file>`

**Log Format & Validation (Constraint-based validation)**
Each valid line in the log file follows exactly this format (space-separated):
`YYYY-MM-DDTHH:MM:SS <IPV4_ADDRESS> <EVENT_NAME> <STATUS_CODE>`

Your C++ program must discard any line that does NOT meet ALL the following constraints:
1. The timestamp must be exactly 19 characters (e.g., `2023-10-01T10:15:30`).
2. The `<IPV4_ADDRESS>` must contain exactly three periods (`.`).
3. The `<STATUS_CODE>` must be exactly 3 digits long.
Ignore all invalid lines.

**Grouping & Aggregation (Large-scale sorting and grouping)**
For all valid lines, extract the **Hour** (`YYYY-MM-DDTHH`) and the **IP Subnet** (the first three octets of the IPv4 address, e.g., if IP is `192.168.1.55`, the subnet is `192.168.1`).
Count the total number of valid events for each `(Subnet, Hour)` pair.

**Changepoint Detection (Anomaly detection)**
Analyze the aggregated event counts to find sudden drops in activity. 
A sudden drop anomaly is defined as:
- A subnet has an event count $C_{prev}$ in hour $H-1$ such that $C_{prev} \ge 50$.
- The same subnet has an event count $C_{curr}$ in the strictly following hour $H$ such that $C_{curr} < (0.20 \times C_{prev})$. (i.e., less than 20% of the previous hour's traffic).
*Note: Hour $H-1$ and Hour $H$ must be consecutive hours on the same day.*

**Step 2: Output Format**
The program must write detected anomalies to the output file (e.g., `/home/user/alerts.tsv`) as tab-separated values.
The file must have a header exactly as follows:
`Subnet	Hour	PreviousCount	CurrentCount`
Following the header, print the anomalies ordered alphabetically by Subnet, and then chronologically by Hour. (The `Hour` column should represent the hour of the drop, i.e., $H$, not $H-1$).

**Step 3: Compilation and Execution**
Compile your program using:
`g++ -O3 -std=c++17 /home/user/process_logs.cpp -o /home/user/process_logs`
Then execute it to process `/home/user/system_events.txt` and generate `/home/user/alerts.tsv`.