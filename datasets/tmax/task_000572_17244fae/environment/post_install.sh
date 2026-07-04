apt-get update && apt-get install -y python3 python3-pip tesseract-ocr
pip3 install pytest pandas scikit-learn pillow pyarrow joblib pytesseract

mkdir -p /app/data

cat << 'EOF' > /tmp/setup.py
import os
import pandas as pd
from sklearn.datasets import make_classification
from PIL import Image, ImageDraw, ImageFont

os.makedirs('/app/data', exist_ok=True)

# Generate dataset
X, y = make_classification(n_samples=50000, n_features=20, n_informative=15, random_state=123)
df = pd.DataFrame(X, columns=[f'f_{i}' for i in range(20)])
df['target'] = y
df.to_parquet('/app/data/dataset.parquet')

# Generate hidden test set
X_h, y_h = make_classification(n_samples=10000, n_features=20, n_informative=15, random_state=999)
df_h = pd.DataFrame(X_h, columns=[f'f_{i}' for i in range(20)])
df_h['target'] = y_h
df_h.to_parquet('/app/data/hidden_test.parquet')

# Create image fixture
img = Image.new('RGB', (800, 200), color=(255, 255, 255))
d = ImageDraw.Draw(img)
text = "Use GridSearchCV with cv=5.\nTune RidgeClassifier with alpha values: [0.1, 1.0, 10.0].\nSet random_state=42 for train_test_split."
d.text((10,10), text, fill=(0,0,0))
img.save('/app/data/instructions.png')

# Create flawed pipeline script
with open('/app/model_pipeline.py', 'w') as f:
    f.write('''import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeClassifier
from sklearn.metrics import roc_auc_score

df = pd.read_parquet('/app/data/dataset.parquet')
X = df.drop('target', axis=1)
y = df['target']

# DATA LEAKAGE HERE
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=1)

clf = RidgeClassifier()
clf.fit(X_train, y_train)

auc = roc_auc_score(y_test, clf.decision_function(X_test))
print(f"Test AUC: {auc}")
''')
EOF

python3 /tmp/setup.py
rm /tmp/setup.py

useradd -m -s /bin/bash user || true
chmod -R 777 /app
chmod -R 777 /home/user