You are acting as a Database Administrator. We have a daily report that relies on a very slow SQL query involving a recursive CTE (to traverse an employee reporting graph) combined with window functions (to rank employees within departments based on aggregated hierarchical data). The database is struggling with this query, so we have decided to export the raw data and build a highly optimized C++ pipeline to process it.

I have exported two files into your home directory:
1. `/home/user/employees.csv` - Contains `id,department,salary`
2. `/home/user/hierarchy.csv` - Contains `manager_id,employee_id` (representing directed edges in our hierarchy graph).

Your task is to write a C++ program at `/home/user/graph_optimizer.cpp` that reads these CSV files and computes the following for every employee:
1. **`subtree_avg_salary`**: The average salary of the employee's entire reporting subtree (this includes the employee themselves, all of their direct reports, and all indirect reports further down the chain). Use standard integer division (truncate decimals) for the average.
2. **`dept_rank`**: The dense rank (1-based) of the employee *within their department* based on their `subtree_avg_salary` in descending order. (i.e., the highest average salary in a department gets rank 1. If two employees tie, they get the same rank, and the next lower salary gets rank + 1).

Your C++ program must output the results to `/home/user/results.csv` with the following requirements:
- Include a header row: `id,department,subtree_avg_salary,dept_rank`
- Sort the output first by `department` (alphabetically, A-Z), then by `dept_rank` (ascending), and finally by `id` (ascending) to break any ties.
- Only use standard C++ libraries (`<iostream>`, `<fstream>`, `<vector>`, `<unordered_map>`, etc.). No external libraries.

Please write the C++ code, compile it using `g++ -O3 -std=c++17 /home/user/graph_optimizer.cpp -o /home/user/graph_optimizer`, and execute it so that `/home/user/results.csv` is generated.