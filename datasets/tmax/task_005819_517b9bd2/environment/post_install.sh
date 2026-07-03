apt-get update && apt-get install -y python3 python3-pip g++ wget
pip3 install pytest

mkdir -p /home/user/data

cat << 'EOF' > /home/user/data/employees.csv
emp_id,name,manager_id
E01,Alice,
E02,Bob,
E03,Charlie,
E04,Diana,E01
E05,Eve,E04
E06,Frank,E02
E07,Grace,E03
E08,Heidi,
E09,Ivan,E08
EOF

cat << 'EOF' > /home/user/data/projects.csv
proj_id,proj_name,owner_emp_id
PRJ-Omega,Project Omega,E08
PRJ-Alpha,Project Alpha,E01
PRJ-Beta,Project Beta,E02
PRJ-Gamma,Project Gamma,E03
PRJ-Delta,Project Delta,E09
EOF

cat << 'EOF' > /home/user/data/proj_deps.csv
proj_id,depends_on_proj_id
PRJ-Omega,PRJ-Alpha
PRJ-Omega,PRJ-Beta
PRJ-Beta,PRJ-Gamma
PRJ-Delta,PRJ-Alpha
EOF

cat << 'EOF' > /home/user/expected_result.json
{
  "page": 2,
  "total_results": 7,
  "results": [
    {
      "emp_id": "E04",
      "name": "Diana"
    },
    {
      "emp_id": "E05",
      "name": "Eve"
    },
    {
      "emp_id": "E06",
      "name": "Frank"
    }
  ]
}
EOF

cat << 'EOF' > /home/user/verify.py
import json
import sys

try:
    with open('/home/user/result.json', 'r') as f:
        actual = json.load(f)

    with open('/home/user/expected_result.json', 'r') as f:
        expected = json.load(f)

    if actual.get('page') != expected.get('page'):
        print("Page mismatch")
        sys.exit(1)

    if actual.get('total_results') != expected.get('total_results'):
        print("Total results mismatch")
        sys.exit(1)

    if len(actual.get('results', [])) != len(expected.get('results', [])):
        print("Results length mismatch")
        sys.exit(1)

    for i in range(len(expected['results'])):
        if actual['results'][i]['emp_id'] != expected['results'][i]['emp_id']:
            print(f"emp_id mismatch at index {i}")
            sys.exit(1)
        if actual['results'][i]['name'] != expected['results'][i]['name']:
            print(f"name mismatch at index {i}")
            sys.exit(1)

    print("Success")
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user