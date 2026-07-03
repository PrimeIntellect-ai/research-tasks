You are a data scientist tasked with cleaning and joining two messy datasets into a clean SQLite database.

You have two raw datasets located in `/home/user/`:
1. `/home/user/employees.csv`
2. `/home/user/projects.json`

Your goal is to write and execute a Python script that performs the following steps:
1. **Load the data** using `pandas` (you may need to install it).
2. **Clean the employees dataset**:
   - Strip any leading or trailing whitespace from the `Name` column.
   - For missing values in the `Salary` column, impute them using the median salary of that employee's `Department`.
3. **Clean the projects dataset**:
   - Standardize the `Start_Date` column to the `YYYY-MM-DD` string format. (You may use libraries like `dateutil` to parse dates).
   - If a date is completely invalid and cannot be parsed, drop that entire row from the projects dataset.
4. **Join the datasets**:
   - Perform an inner join between the cleaned employees and projects datasets on the employee ID (`ID` from employees, `Employee_ID` from projects).
5. **Enforce the schema**:
   Ensure the final joined DataFrame has exactly the following columns and types before saving:
   - `ID` (integer)
   - `Name` (string)
   - `Department` (string)
   - `Salary` (float)
   - `Project_Name` (string)
   - `Start_Date` (string, format YYYY-MM-DD)
6. **Save to SQLite**:
   - Save the resulting DataFrame to an SQLite database at `/home/user/cleaned_data.db` in a table named `employee_projects`. Do not include the pandas DataFrame index.

You may install any required Python packages (e.g., `pandas`, `python-dateutil`, `sqlalchemy`) using `pip`. Provide the necessary commands and run them to complete this end-to-end task.