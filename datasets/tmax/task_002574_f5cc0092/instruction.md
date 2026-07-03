You are an AI assistant acting as a technical compliance officer auditing internal systems for a severe security breach. 

We have recovered a screen recording of a hacker's surveillance dashboard (`/app/dashboard_leak.mp4`). This video shows a scrolling log of real-time physical access events within our secure facility over a 10-minute window. Unfortunately, the raw text logs were wiped by the attacker, leaving this video as our only record of physical access.

Additionally, you have access to a local SQLite database (`/app/company_data.db`) containing the relational schema for our facility's layout and personnel records. It contains two tables:
1. `employees` (EmpID, Department, ClearanceLevel)
2. `rooms` (RoomID, RequiredClearance)

Your objective is to reconstruct the access graph, map it against the relational schema, and compute a Compliance Risk Score for every employee.

**Workflow Requirements:**
1. **Video Data Extraction:** Extract the access events from `/app/dashboard_leak.mp4`. The video displays frames of text in the format: `ACCESS: [EmpID] -> [RoomID]`. You will need to use a tool like `ffmpeg` and OCR (e.g., `tesseract`, which you may need to install) to extract these logs.
2. **Schema & Graph Construction:** Build a graph representation of the facility and personnel. Using the SQLite database, map each employee to the rooms they accessed based on your extracted video data.
3. **Risk Analysis:** Compute a `RiskScore` for each employee found in the database. Start each employee with a score of 0. 
   - Add **1.0 point** for every distinct room accessed by the employee where their `ClearanceLevel` is strictly less than the room's `RequiredClearance`.
   - Add **0.5 points** for every distinct room accessed by the employee that is valid (ClearanceLevel >= RequiredClearance).
4. **Export:** Export your findings to `/home/user/employee_risk_scores.csv`. The CSV must have exactly two columns: `EmpID` and `RiskScore`. Include all employees present in the `employees` table, even if their score is 0. Sort by `EmpID` ascending.

**Evaluation:**
Your output will be evaluated using an automated test that calculates the Mean Absolute Error (MAE) between your computed risk scores and the ground-truth scores derived from the raw logs (before they were rendered to video). 
You must achieve an **MAE of <= 0.15** to pass this compliance audit.