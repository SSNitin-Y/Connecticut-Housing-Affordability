# run.py
from pathlib import Path
import sys
import pandas as pd
from glob import glob

from src.load_clean import load_clean
from src.metrics import monthly_by_town, add_deltas
from src.affordability import compute_affordability
from src.config_reader import read_inputs_yaml
from src.viz import line_price_trend, bar_top_towns_by_total_monthly
from src.viz_plotly import line_median_price_plotly, bar_top_towns_plotly, heatmap_yoy_plotly

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT/"data"/"raw"
CLEAN_DIR = ROOT/"data"/"clean"
AN_DIR = ROOT/"data"/"analytics"
REPORTS = ROOT/"reports"
CONFIG = ROOT/"config"/"inputs.yaml"

for d in (RAW_DIR, CLEAN_DIR, AN_DIR, REPORTS):
    d.mkdir(parents=True, exist_ok=True)

def find_raw_csv() -> Path | None:
    candidate = RAW_DIR/"Housing_data.csv"
    if candidate.exists():
        return candidate
    files = sorted(Path(RAW_DIR).glob("*.csv"))
    return files[0] if files else None

def main():
    print(f"[INFO] project root: {ROOT}")
    print(f"[INFO] python: {sys.executable}")
    raw_path = find_raw_csv()
    if not raw_path:
        print(f"[ERROR] No CSV found in {RAW_DIR}. Put your file there (e.g. Housing_data.csv).")
        sys.exit(2)
    print(f"[INFO] raw csv: {raw_path}")

    cfg = read_inputs_yaml(str(CONFIG)) or {}
    print(f"[INFO] config defaults: {cfg if cfg else '(using hardcoded defaults inside code)'}")

    # 1) Load & clean
    clean = load_clean(str(raw_path))
    clean_out = CLEAN_DIR/"clean_housing.csv"
    clean.to_csv(clean_out, index=False)
    print(f"[INFO] wrote {clean_out} ({len(clean)} rows)")

    # 2) Monthly metrics
    if clean["month_key"].isna().all():
        print("[ERROR] All month_key are NaT. Date parsing failed. Fix your date column header or content.")
        sys.exit(3)

    monthly = monthly_by_town(clean)
    monthly_out = AN_DIR/"monthly_by_town.csv"
    monthly.to_csv(monthly_out, index=False)
    print(f"[INFO] wrote {monthly_out} ({len(monthly)} rows)")

    metrics = add_deltas(monthly)
    metrics_out = AN_DIR/"monthly_by_town_with_deltas.csv"
    metrics.to_csv(metrics_out, index=False)
    print(f"[INFO] wrote {metrics_out} ({len(metrics)} rows)")

    # 3) Latest snapshot (prefer latest month with any data)
    last_month = metrics["month_key"].max()
    snap = metrics.loc[metrics["month_key"]==last_month, ["town","median_sale_amount","sales_count"]].dropna()
    if snap.empty:
        # fallback: use overall latest 5 towns by sales_count across all months
        snap = (metrics.sort_values(["month_key","sales_count"], ascending=[False,False])
                      [["town","median_sale_amount","sales_count"]]
                      .dropna()
                      .groupby("town", as_index=False).head(1))
        print("[WARN] latest-month snapshot empty; using fallback top towns overall")
    print(f"[INFO] snapshot rows: {len(snap)}")

    # 4) Affordability
    aff = compute_affordability(snap, cfg)
    aff_out = AN_DIR/"affordability_latest.csv"
    aff.to_csv(aff_out, index=False)
    print(f"[INFO] wrote {aff_out} ({len(aff)} rows)")

    # 5) Charts — always write something (placeholders if needed)
    print(f"[INFO] reports dir: {REPORTS.resolve()}")
    towns_for_trend = []
    if not snap.empty:
        towns_for_trend = snap.sort_values("sales_count", ascending=False)["town"].head(5).tolist()
    else:
        overall = (metrics.groupby("town", as_index=False)["sales_count"].sum()
                          .sort_values("sales_count", ascending=False))
        towns_for_trend = overall["town"].head(5).tolist()
    print(f"[INFO] towns_for_trend: {towns_for_trend[:5]}")

    if towns_for_trend:
        line_price_trend(metrics, towns_for_trend[0], str(REPORTS/"trend_top_town.png"))

    line_median_price_plotly(metrics, towns_for_trend, str(REPORTS/"trend_top_towns.html"))

    dti_pass_ct = int(aff["passes_dti"].sum()) if not aff.empty else 0
    bar_top_towns_plotly(
        aff, 20, str(REPORTS/"top_towns_lowest_total_monthly.html"),
        strict_dti=(dti_pass_ct > 0)
    )

    heatmap_yoy_plotly(metrics, str(REPORTS/"yoy_heatmap.html"))

    # List outputs
    written = sorted(p.name for p in REPORTS.iterdir())
    print("[INFO] report files:", written)
    print("[DONE]")

if __name__ == "__main__":
    main()
