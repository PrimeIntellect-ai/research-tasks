apt-get update && apt-get install -y python3 python3-pip sqlite3 tesseract-ocr
    pip3 install pytest pandas scikit-learn networkx Pillow pytesseract

    mkdir -p /app
    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup_data.py
import os
import sqlite3
import random
import pandas as pd
import networkx as nx
from PIL import Image, ImageDraw, ImageFont

# 1. Create Image
img = Image.new('RGB', (400, 200), color = (255, 255, 255))
d = ImageDraw.Draw(img)
text = """Graph Analytics Parameters
Damping Factor: 0.85
Decay Rules:
Difference > 10 years: weight 0.5
Difference <= 10 years: weight 1.0"""
d.text((10,10), text, fill=(0,0,0))
img.save('/app/weight_params.png')

# 2. Create Database
db_path = '/home/user/citation_data.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('CREATE TABLE papers (id INTEGER PRIMARY KEY, year INTEGER, venue TEXT)')
c.execute('CREATE TABLE citations (source_id INTEGER, target_id INTEGER)')

papers = []
for i in range(1, 1001):
    year = random.randint(1990, 2023)
    papers.append((i, year, f"Venue_{random.randint(1, 10)}"))
c.executemany('INSERT INTO papers VALUES (?, ?, ?)', papers)

paper_years = {p[0]: p[1] for p in papers}
citations = []
for _ in range(5000):
    src = random.randint(1, 1000)
    tgt = random.randint(1, 1000)
    if src != tgt and paper_years[src] >= paper_years[tgt]:
        citations.append((src, tgt))
# Remove duplicates
citations = list(set(citations))
c.executemany('INSERT INTO citations VALUES (?, ?)', citations)
conn.commit()

# 3. Compute Golden PageRank
# Extract subgraph: top 5 most recent outgoing citations per paper
query = """
WITH RankedCitations AS (
    SELECT c.source_id, c.target_id, p.year as target_year,
           ROW_NUMBER() OVER(PARTITION BY c.source_id ORDER BY p.year DESC) as rn
    FROM citations c
    JOIN papers p ON c.target_id = p.id
)
SELECT source_id, target_id FROM RankedCitations WHERE rn <= 5
"""
subgraph_edges = pd.read_sql_query(query, conn)

G = nx.DiGraph()
for _, row in subgraph_edges.iterrows():
    src = row['source_id']
    tgt = row['target_id']
    src_year = paper_years[src]
    tgt_year = paper_years[tgt]
    diff = abs(src_year - tgt_year)
    weight = 0.5 if diff > 10 else 1.0
    G.add_edge(src, tgt, weight=weight)

pr = nx.pagerank(G, alpha=0.85, weight='weight')
pr_df = pd.DataFrame(list(pr.items()), columns=['node_id', 'pagerank_score'])
pr_df.to_csv('/app/golden_pagerank.csv', index=False)

conn.close()
EOF

    python3 /tmp/setup_data.py
    chmod -R 777 /home/user
    chmod -R 777 /app