apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest pandas

    mkdir -p /app
    cat << 'EOF' > /app/legacy_pipeline
#!/usr/bin/env python3
import sys
import pandas as pd
import json
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('users_csv')
    parser.add_argument('txns_csv')
    parser.add_argument('--track', type=str, default=None)
    args, unknown = parser.parse_known_args()

    # Read CSVs using Int64 to prevent precision loss on missing values
    users = pd.read_csv(args.users_csv, dtype={'user_id': 'Int64', 'age': 'Int64', 'risk_score': float})
    txns = pd.read_csv(args.txns_csv, dtype={'txn_id': 'Int64', 'user_id': 'Int64', 'amount': 'Int64', 'status': str})

    # Handle missing ages
    ages_imputed = users['age'].isna().sum()
    users['age'] = users['age'].fillna(99)

    # Handle missing amounts
    txns['amount'] = txns['amount'].fillna(0)

    # Drop outliers
    outliers_mask = (txns['amount'] > 1000000) | (txns['amount'] < -1000000)
    outliers_dropped = outliers_mask.sum()
    txns = txns[~outliers_mask]

    # Aggregate
    agg = txns.groupby('user_id').agg(total_amount=('amount', 'sum'), txn_count=('amount', 'count')).reset_index()

    # Join
    merged = pd.merge(users, agg, on='user_id', how='left')
    merged['total_amount'] = merged['total_amount'].fillna(0).astype('Int64')
    merged['txn_count'] = merged['txn_count'].fillna(0).astype('Int64')

    # Sort for deterministic output
    merged = merged.sort_values('user_id')

    # Output to stdout
    merged.to_csv(sys.stdout, index=False)

    # Optional experiment tracking
    if args.track:
        with open(args.track, 'w') as f:
            json.dump({"outliers_dropped": int(outliers_dropped), "ages_imputed": int(ages_imputed)}, f)

if __name__ == '__main__':
    main()
EOF
    chmod +x /app/legacy_pipeline

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user