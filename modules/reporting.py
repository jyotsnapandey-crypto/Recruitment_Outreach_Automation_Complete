import io
import pandas as pd

def build_csv_bytes(rows):
    if not rows:
        return b""
    return pd.DataFrame(rows).to_csv(index=False).encode("utf-8")
