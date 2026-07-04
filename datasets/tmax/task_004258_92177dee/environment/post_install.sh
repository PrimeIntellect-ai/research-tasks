apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest pandas numpy scikit-learn

    mkdir -p /home/user/data

    cat << 'EOF' > /home/user/generate_data.py
import pandas as pd
import numpy as np

np.random.seed(42)
n_train = 1000
n_test = 200

def generate_df(n):
    # Base ID is 2^53 = 9007199254740992
    base = 9007199254740992

    # Generate offsets 0, 1, 2, 3...
    offsets = np.random.randint(0, 10, size=n)
    device_ids = base + offsets

    # Target is perfectly correlated with whether the offset is odd or even
    targets = offsets % 2

    val1 = np.random.randn(n)

    df = pd.DataFrame({
        'device_id': device_ids,
        'val1': val1,
        'target': targets
    })

    # Introduce missing values to force float64 cast if not handled
    missing_idx = np.random.choice(n, size=int(n*0.1), replace=False)
    df.loc[missing_idx, 'device_id'] = np.nan

    # For missing values, we assign a random target. 
    # But the remaining 90% are perfectly predictive.
    return df

train_df = generate_df(n_train)
test_df = generate_df(n_test)

train_df.to_csv('/home/user/data/train.csv', index=False)
# drop target for test
test_df.drop(columns=['target']).to_csv('/home/user/data/test.csv', index=False)
test_df[['target']].to_csv('/home/user/data/test_labels.csv', index=False)
EOF

    python3 /home/user/generate_data.py

    cat << 'EOF' > /home/user/pipeline.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
import numpy as np

def main():
    # BUG: read_csv reads device_id as float64 due to NaNs, losing precision on large integers!
    train = pd.read_csv('/home/user/data/train.csv')
    test = pd.read_csv('/home/user/data/test.csv')

    # Impute missing values
    train['device_id'] = train['device_id'].fillna(0)
    test['device_id'] = test['device_id'].fillna(0)

    # Convert to string for categorical encoding
    train['device_id'] = train['device_id'].astype(str)
    test['device_id'] = test['device_id'].astype(str)

    # Combine to fit LabelEncoder
    le = LabelEncoder()
    le.fit(pd.concat([train['device_id'], test['device_id']]))

    train['device_id_enc'] = le.transform(train['device_id'])
    test['device_id_enc'] = le.transform(test['device_id'])

    features = ['device_id_enc', 'val1']
    X = train[features]
    y = train['target']

    model = RandomForestClassifier(n_estimators=50, random_state=42)

    # Cross validation
    cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
    print(f"Cross-validation accuracy: {np.mean(cv_scores):.4f}")

    # Final train and predict
    model.fit(X, y)
    preds = model.predict(test[features])

    pred_df = pd.DataFrame({'prediction': preds})
    pred_df.to_csv('/home/user/predictions.csv', index=False)
    print("Predictions saved to /home/user/predictions.csv")

if __name__ == "__main__":
    main()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user