from datetime import datetime
import pandas as pd
from pathlib import Path

INPUT_FILE = "competitors.csv"
OUTPUT_FILE = "monitor_log.csv"

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df = pd.read_csv(INPUT_FILE)

    rows = []
    for _, row in df.iterrows():
        rows.append({
            "timestamp": now,
            "space_name": row.get("name", ""),
            "url": row.get("url", ""),
            "status": "test_run"
        })

    out_df = pd.DataFrame(rows)

    output_path = Path(OUTPUT_FILE)
    if output_path.exists():
        old_df = pd.read_csv(output_path)
        out_df = pd.concat([old_df, out_df], ignore_index=True)

    out_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print("saved")

if __name__ == "__main__":
    main()
