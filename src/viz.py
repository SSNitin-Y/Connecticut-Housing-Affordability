# src/viz.py
import matplotlib.pyplot as plt
import pandas as pd

def line_price_trend(metrics: pd.DataFrame, town: str, out_path: str):
    d = metrics[metrics["town"]==town].sort_values("month_key")
    if len(d) < 3:
        return None
    plt.figure()
    plt.plot(d["month_key"], d["median_sale_amount"])
    plt.title(f"Median sale amount — {town}")
    plt.xlabel("Month"); plt.ylabel("Median sale amount")
    plt.tight_layout(); plt.savefig(out_path); plt.close()
    return out_path

def bar_top_towns_by_total_monthly(aff: pd.DataFrame, out_path: str, k:int=20):
    d = aff[aff["passes_dti"]].sort_values("total_monthly").head(k)
    if d.empty:
        return None
    plt.figure(figsize=(8,6))
    plt.barh(d["town"], d["total_monthly"])
    plt.title("Top towns by lowest total monthly (DTI-compliant)")
    plt.xlabel("Total monthly (USD)")
    plt.gca().invert_yaxis()
    plt.tight_layout(); plt.savefig(out_path); plt.close()
    return out_path
