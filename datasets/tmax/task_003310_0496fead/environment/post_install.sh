apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest pandas numpy scikit-learn

    # Create directories
    mkdir -p /home/user/data
    mkdir -p /app/tiny_ann/tiny_ann

    # Generate tiny_ann package
    cat << 'EOF' > /app/tiny_ann/setup.py
import setuptool

setuptool.setup(
    name="tiny_ann",
    version="0.1.0",
    packages=["tiny_ann"]
)
EOF

    cat << 'EOF' > /app/tiny_ann/tiny_ann/__init__.py
import numpy as np

class TinyIndex:
    def __init__(self, dim):
        self.dim = dim
        self.vectors = None

    def add(self, vectors):
        self.vectors = np.array(vectors)

    def search(self, queries, k=5):
        queries = np.atleast_2d(queries)
        norm_q = np.linalg.norm(queries, axis=1, keepdims=True)
        norm_v = np.linalg.norm(self.vectors, axis=1, keepdims=True)
        q_norm = queries / np.where(norm_q == 0, 1, norm_q)
        v_norm = self.vectors / np.where(norm_v == 0, 1, norm_v)
        sim = np.dot(q_norm, v_norm.T)
        return np.argsort(sim, axis=1)[:, ::-1][:, :k]
EOF

    # Generate dataset and golden recommendations
    cat << 'EOF' > /tmp/generate_data.py
import os
import random
import string
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

random.seed(42)
np.random.seed(42)

# Create a vocabulary of 1000 words
vocab = [''.join(random.choices(string.ascii_lowercase, k=6)) for _ in range(1000)]

def make_text(n_words):
    return ' '.join(random.choices(vocab, k=n_words))

items = [{"item_id": f"item_{i}", "description": make_text(30)} for i in range(5000)]
items_df = pd.DataFrame(items)
items_df.to_csv('/home/user/data/items.csv', index=False)

queries = [{"query_id": f"query_{i}", "description": make_text(30)} for i in range(200)]
queries_df = pd.DataFrame(queries)
queries_df.to_csv('/home/user/data/queries.csv', index=False)

# Compute golden recommendations
vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
X_items = vectorizer.fit_transform(items_df['description'])
svd = TruncatedSVD(n_components=50, random_state=42)
X_items_svd = svd.fit_transform(X_items)

X_queries = vectorizer.transform(queries_df['description'])
X_queries_svd = svd.transform(X_queries)

sim = cosine_similarity(X_queries_svd, X_items_svd)
golden = []
for i in range(200):
    top5_idx = np.argsort(sim[i])[::-1][:5]
    top5_items = [items_df.iloc[idx]['item_id'] for idx in top5_idx]
    golden.append({
        "query_id": queries_df.iloc[i]['query_id'],
        "recommended_item_ids": " ".join(top5_items)
    })

pd.DataFrame(golden).to_csv('/home/user/data/golden_recommendations.csv', index=False)
EOF

    python3 /tmp/generate_data.py
    rm /tmp/generate_data.py

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user
    chmod -R 777 /app