# src/load_clean.py
import pandas as pd
import numpy as np
from pathlib import Path

KNOWN_DATE_NAMES = {
    "date recorded", "recording date", "sale date", "date", "transfer date"
}

def _to_num(x):
    if pd.isna(x): return np.nan
    if isinstance(x, (int, float, np.number)): return float(x)
    s = str(x).replace(",", "").replace("$", "").strip()
    try: return float(s)
    except: return np.nan

def _ratio(v):
    if pd.isna(v): return np.nan
    s = str(v).strip()
    if s.endswith("%"):
        try: return float(s[:-1]) / 100.0
        except: return np.nan
    try:
        f = float(s)
        return f/100.0 if f > 1.2 else f
    except:
        return np.nan

def detect_date_column(df: pd.DataFrame) -> str | None:
    # 1) prefer known names
    lower = {c.lower(): c for c in df.columns}
    for name in KNOWN_DATE_NAMES:
        if name in lower:
            c = lower[name]
            s = pd.to_datetime(df[c], errors="coerce")
            if s.notna().sum() > max(50, 0.01*len(df)):
                return c
    # 2) any column containing "date"
    candidates = [c for c in df.columns if "date" in c.lower()]
    best = None; best_count = 0
    for c in candidates:
        s = pd.to_datetime(df[c], errors="coerce")
        cnt = int(s.notna().sum())
        if cnt > best_count:
            best, best_count = c, cnt
    if best and best_count > max(50, 0.01*len(df)):
        return best
    # 3) last resort: try everything
    for c in df.columns:
        try:
            s = pd.to_datetime(df[c], errors="coerce")
            if s.notna().sum() > max(50, 0.02*len(df)):
                return c
        except Exception:
            pass
    return None

def load_clean(raw_path: str) -> pd.DataFrame:
    print(f"[INFO] load_clean: reading {raw_path}")
    df = pd.read_csv(raw_path, low_memory=False)
    print(f"[INFO] raw shape: {df.shape}")
    df.columns = [c.strip() for c in df.columns]
    df.columns = [c.lower() for c in df.columns]

    # Coerce numerics
    if "assessed value" in df.columns:
        df["assessed_value"] = df["assessed value"].map(_to_num)
    if "sale amount" in df.columns:
        df["sale_amount"] = df["sale amount"].map(_to_num)
    if "sales ratio" in df.columns:
        df["sales_ratio_num"] = df["sales ratio"].map(_ratio)

    # Dates
    date_col = detect_date_column(df)
    if date_col:
        print(f"[INFO] detected date column: {date_col!r}")
        s = pd.to_datetime(df[date_col], errors="coerce")
        df["date_recorded"] = s
        df["month_key"] = s.values.astype("datetime64[M]")
        print(f"[INFO] non-null dates: {s.notna().sum()}")
    else:
        print("[WARN] no date column detected; month_key will be NaT")
        df["date_recorded"] = pd.NaT
        df["month_key"] = pd.NaT

    keep = [
        "serial number","list year","date_recorded","month_key","town","address",
        "assessed_value","sale_amount","sales_ratio_num","property type","residential type"
    ]
    present = [c for c in keep if c in df.columns]
    out = df[present].copy()
    print(f"[INFO] cleaned shape: {out.shape} | columns: {present}")
    # minimal sanity
    if "town" in out.columns:
        print(f"[INFO] unique towns: {out['town'].nunique()}")
    if "sale_amount" in out.columns:
        print(f"[INFO] sale_amount non-null: {out['sale_amount'].notna().sum()}")
    return out
