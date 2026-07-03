You are a data analyst working with a hierarchical dataset of employees. 

A CSV file containing the employee hierarchy is located at `/home/user/employees.csv`. The file has the following columns: `emp_id,manager_id,name,salary`. The top-level executive has an empty `manager_id`.

Your task is to process this data using MongoDB and C++ to find the total salary of the CEO (emp_id: "E1") and all of their direct and indirect subordinates.

Perform the following steps:
1. Start a local MongoDB server using Docker (use the standard `mongo:latest` image, exposed on port 27017).
2. Import the data from `/home/user/employees.csv` into a MongoDB database named `company` and a collection named `employees`.
3. Create a query script (e.g., using `mongosh`) that:
   - Creates an index on the `manager_id` field to optimize hierarchical lookups.
   - Uses the NoSQL aggregation pipeline with `$graphLookup` to retrieve the CEO ("E1") and all recursive subordinates.
   - Outputs the aggregation result to a JSON file at `/home/user/hierarchy.json`.
4. Write a C++ program at `/home/user/aggregate_salary.cpp` that:
   - Parses the `/home/user/hierarchy.json` file.
   - Calculates the total combined salary of the CEO and all recursively found subordinates.
   - Writes the final integer sum to `/home/user/total_salary.txt`.
5. Compile and run your C++ program to generate the final output. You may use `nlohmann/json.hpp` for JSON parsing, which is available on the system.

Provide the exact commands and code you use to accomplish this.