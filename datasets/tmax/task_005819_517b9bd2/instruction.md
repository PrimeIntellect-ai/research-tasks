You are a data analyst tasked with processing an organization's internal structure and project dependencies. You have been provided with three CSV files located in `/home/user/data/`. 

Your goal is to write a **C++** program that ingests these CSV files, reconstructs the underlying knowledge graph in-memory, and performs a specific hierarchical query.

The CSV files (comma-separated with headers) are:
1. `employees.csv` - Contains `emp_id`, `name`, and `manager_id`. (If a person has no manager, `manager_id` is empty).
2. `projects.csv` - Contains `proj_id`, `proj_name`, and `owner_emp_id`.
3. `proj_deps.csv` - Contains `proj_id` and `depends_on_proj_id`, representing which project depends on another.

**The Query Requirement:**
We are doing an impact analysis for a specific project: **"PRJ-Omega"**. 
You must find all employees who could be affected by changes to the upstream dependencies of "PRJ-Omega".

Specifically, your C++ program must:
1. Find all **transitive dependencies** of "PRJ-Omega" (i.e., projects that PRJ-Omega depends on, projects those projects depend on, recursively). Do *not* include "PRJ-Omega" itself.
2. Find the **owners** of all those discovered projects.
3. Find all **direct and indirect reports** (recursively down the management chain) of those project owners.
4. The final set of affected employees includes the project owners found in step 2 AND all their recursive reports found in step 3.

**Data Processing & Output Requirements:**
1. Sort the final unique set of affected employees alphabetically by their `name`.
2. Implement pagination for the results. We want **Page 2**, where the **Page Size is 3** (Assume 1-indexed pages. Page 1 has items 1-3, Page 2 has items 4-6, etc.).
3. Your C++ program must output the result strictly as a JSON file to `/home/user/result.json`.

**JSON Schema Requirement:**
```json
{
  "page": 2,
  "total_results": <total_number_of_affected_employees_before_pagination>,
  "results": [
    {
      "emp_id": "<employee_id>",
      "name": "<employee_name>"
    },
    ...
  ]
}
```

**Constraints:**
- You must write the solution in C++. 
- You can compile it using `g++`.
- You may use a third-party JSON library like `nlohmann/json`. Since you do not have root access to use `apt-get`, you should download single-header libraries (like `wget https://github.com/nlohmann/json/releases/download/v3.11.2/json.hpp`) directly into your working directory and include them.
- Save your source code in `/home/user/solution.cpp` and compile it to `/home/user/solution`. Then run it to generate the `/home/user/result.json` file.