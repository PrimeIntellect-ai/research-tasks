You are an assistant helping a computational chemist analyze molecular simulation logs. 

I ran a network simulation of molecular collisions, and the output is stored in `/home/user/collisions.log`. 
Each line represents a single collision event in the format:
`event_id|molecule_A|molecule_B|collision_energy`

Your task is to analyze this interaction network using pure Bash tools (like `awk`, `sed`, `grep`, `sort`, `uniq`, etc.). 

Please perform the following steps:
1. **Calculate Node Degrees:** Calculate the degree of each molecule in the collision network. A collision between `molecule_A` and `molecule_B` adds 1 to the degree of `molecule_A` and 1 to the degree of `molecule_B`. 
2. **Rank the Molecules:** Create a file named `/home/user/degree_ranking.txt` containing the molecules ranked by their degree in descending order. If there is a tie in degree, sort the tied molecules alphabetically in ascending order. The format of each line should be `MoleculeName Degree` (separated by a single space).
3. **Visualize the Top 5:** Create a text-based bar chart for the top 5 molecules with the highest degrees (using the same sorting rules as above). Save this to `/home/user/top5_bar.txt`. The format for each line must be exactly `MoleculeName: ###...` where the number of `#` characters is equal to the molecule's degree. There should be exactly one space after the colon.

Do not use Python, R, or any other programming language. You must accomplish this using shell commands/scripts.