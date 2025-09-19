# src/metrics.py
import pandas as pd

def monthly_by_town(clean: pd.DataFrame) -> pd.DataFrame:
    if "month_key" not in clean.columns or "town" not in clean.columns:
        raise ValueError("monthly_by_town: required columns missing (month_key, town)")
    if "sale_amount" not in clean.columns:
        raise ValueError("monthly_by_town: required column missing (sale_amount)")
    df = clean.dropna(subset=["month_key","town"])
    m = (df.groupby(["month_key","town"], as_index=False)
           .agg(
               sales_count=("sale_amount","count"),
               median_sale_amount=("sale_amount","median"),
               avg_assessed_value=("assessed_value","mean"),
               avg_sales_ratio=("sales_ratio_num","mean"),
           )
           .sort_values(["town","month_key"]))
    print(f"[INFO] monthly rows: {len(m)}  | months: {m['month_key'].nunique()} | towns: {m['town'].nunique()}")
    return m

def add_deltas(df: pd.DataFrame, group="town", date="month_key", val="median_sale_amount") -> pd.DataFrame:
    if df.empty:
        print("[WARN] add_deltas: empty dataframe")
        return df.copy()
    d = df.sort_values([group, date]).copy()
    d["mom"] = d.groupby(group)[val].pct_change(1)
    d["yoy"] = d.groupby(group)[val].pct_change(12)
    return d
