apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest scipy networkx pandas

    mkdir -p /home/user
    mkdir -p /app/tinygraph/tinygraph

    # Create employees.csv
    cat << 'EOF' > /home/user/employees.csv
id,name,department
1,Alice,Engineering
2,Bob,Engineering
3,Charlie,Engineering
4,David,Sales
5,Eve,Sales
EOF

    # Create reporting.csv
    cat << 'EOF' > /home/user/reporting.csv
emp_id,manager_id
2,1
3,2
5,4
EOF

    # Create tinygraph setup.py with typo
    cat << 'EOF' > /app/tinygraph/setup.py
from setuptools import setup, find_packages

setup(
    name='tinygraph',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['networx'],
)
EOF

    # Create tinygraph/__init__.py
    cat << 'EOF' > /app/tinygraph/tinygraph/__init__.py
import networkx as nx

class Graph:
    def __init__(self, edges):
        self.G = nx.DiGraph()
        self.G.add_edges_from(edges)

    def pagerank(self):
        return nx.pagerank(self.G)
EOF

    # Create bad build_graph.sql
    cat << 'EOF' > /home/user/build_graph.sql
SELECT e1.id AS source, e2.id AS target
FROM employees e1, employees e2
WHERE e1.department = e2.department AND e1.id != e2.id;
EOF

    # Create pipeline.py
    cat << 'EOF' > /home/user/pipeline.py
import sqlite3
import json
import csv
import tinygraph

conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('CREATE TABLE employees (id INTEGER, name TEXT, department TEXT)')
with open('/home/user/employees.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    cursor.executemany('INSERT INTO employees VALUES (?, ?, ?)', reader)

cursor.execute('CREATE TABLE reporting (emp_id INTEGER, manager_id INTEGER)')
with open('/home/user/reporting.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    cursor.executemany('INSERT INTO reporting VALUES (?, ?)', reader)

with open('/home/user/build_graph.sql', 'r') as f:
    query = f.read()

cursor.execute(query)
edges = cursor.fetchall()

G = tinygraph.Graph(edges)
pr = G.pagerank()

with open('/home/user/pagerank.json', 'w') as f:
    json.dump({str(k): v for k, v in pr.items()}, f)
EOF

    # Generate reference pagerank
    cat << 'EOF' > /tmp/generate_reference.py
import sqlite3
import networkx as nx
import json
import pandas as pd

conn = sqlite3.connect(':memory:')
pd.read_csv('/home/user/employees.csv').to_sql('employees', conn, index=False)
pd.read_csv('/home/user/reporting.csv').to_sql('reporting', conn, index=False)

query = """
WITH RECURSIVE hierarchy AS (
    SELECT emp_id AS source, manager_id AS target
    FROM reporting
    UNION ALL
    SELECT h.source, r.manager_id AS target
    FROM hierarchy h
    JOIN reporting r ON h.target = r.emp_id
)
SELECT source, target FROM hierarchy;
"""
edges = pd.read_sql_query(query, conn)
G = nx.DiGraph()
G.add_edges_from(zip(edges['source'], edges['target']))
pr = nx.pagerank(G)
with open('/tmp/reference_pagerank.json', 'w') as f:
    json.dump({str(k): v for k, v in pr.items()}, f)
EOF
    python3 /tmp/generate_reference.py
    rm /tmp/generate_reference.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app