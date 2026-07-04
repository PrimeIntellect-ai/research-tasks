# test_final_state.py

import os
import re
import pytest

def test_clean_report_exists_and_correct():
    raw_data_path = "/home/user/raw_data.txt"
    report_path = "/home/user/clean_report.txt"

    assert os.path.isfile(raw_data_path), f"Input file {raw_data_path} is missing."
    assert os.path.isfile(report_path), f"Output file {report_path} is missing. Did you run the Rust program?"

    # Parse raw data
    records = []
    seen_txids = set()

    pattern = re.compile(r"TxID:\s*(?P<txid>\w+)\s*\|\s*User:\s*(?P<user>[^|]+?)\s*\|\s*Card:\s*(?P<card>\d{16})\s*\|\s*Amount:\s*(?P<amount>[\d.]+)")

    with open(raw_data_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = pattern.search(line)
            if match:
                txid = match.group("txid")
                user = match.group("user").strip()
                card = match.group("card")
                amount = float(match.group("amount"))

                if txid not in seen_txids:
                    seen_txids.add(txid)
                    records.append({
                        "txid": txid,
                        "user": user,
                        "card": card,
                        "amount": amount
                    })

    assert len(records) > 0, "No valid records found in raw data."

    # Compute min and max for normalization
    amounts = [r["amount"] for r in records]
    min_amt = min(amounts)
    max_amt = max(amounts)

    expected_output_lines = []

    for i, r in enumerate(records):
        # Mask card
        masked_card = r["card"][:4] + "********" + r["card"][12:]

        # Rolling average
        start_idx = max(0, i - 2)
        window = amounts[start_idx:i+1]
        rolling_avg = sum(window) / len(window)

        # Normalization
        if max_amt == min_amt:
            norm_amount = 0.0
        else:
            norm_amount = (r["amount"] - min_amt) / (max_amt - min_amt)

        expected_output_lines.append(f"REPORT FOR TX {r['txid']}")
        expected_output_lines.append(f"User: {r['user']}")
        expected_output_lines.append(f"Card: {masked_card}")
        expected_output_lines.append(f"Norm_Amount: {norm_amount:.4f}")
        expected_output_lines.append(f"Rolling_Avg: {rolling_avg:.4f}")
        expected_output_lines.append("---")

    expected_output = "\n".join(expected_output_lines) + "\n"

    with open(report_path, 'r') as f:
        actual_output = f.read()

    assert actual_output.strip() == expected_output.strip(), (
        "The generated report does not match the expected output. "
        "Check deduplication, masking, rolling average, and normalization logic."
    )