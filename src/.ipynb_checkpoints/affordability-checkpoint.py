import pandas as pd

def mortgage_pmt(principal: float, annual_rate: float, years: int) -> float:
    r = annual_rate / 12.0
    n = years * 12
    if r == 0 or n == 0:
        return principal / n if n else 0.0
    return principal * (r * (1 + r)**n) / ((1 + r)**n - 1)

def compute_affordability(latest_prices: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    # Expect columns: town, median_sale_amount, sales_count
    d = latest_prices.rename(columns={"median_price":"median_sale_amount"}).dropna(subset=["median_sale_amount"]).copy()

    dp_pct   = float(cfg.get("down_payment_pct", 0.10))
    rate     = float(cfg.get("interest_rate_apy", 0.065))
    term     = int(cfg.get("term_years", 30))
    cc_pct   = float(cfg.get("closing_cost_pct", 0.03))
    tax_rate = float(cfg.get("property_tax_rate", 0.012))
    ins_y    = float(cfg.get("insurance_annual_usd", 1500))
    hoa_condo= float(cfg.get("hoa_monthly_usd_condo", 250))
    hoa_sfh  = float(cfg.get("hoa_monthly_usd_sfh", 0))
    gmi      = float(cfg.get("gross_monthly_income", 8000))
    fe_cap   = float(cfg.get("dti_frontend_max", 0.28))
    be_cap   = float(cfg.get("dti_backend_max", 0.36))

    default_hoa = min(hoa_condo, hoa_sfh)

    out = []
    for _, row in d.iterrows():
        price = float(row["median_sale_amount"])
        dp = dp_pct * price
        loan = max(price - dp, 0.0)
        pmt_pi = mortgage_pmt(loan, rate, term)
        taxes_mo = price * tax_rate / 12.0
        ins_mo = ins_y / 12.0
        hoa_mo = default_hoa

        total_mo = pmt_pi + taxes_mo + ins_mo + hoa_mo
        cash_to_close = dp + cc_pct * price

        fe_ratio = total_mo / gmi if gmi else None
        be_ratio = fe_ratio
        pass_dti = (fe_ratio is not None and fe_ratio <= fe_cap) and (be_ratio is not None and be_ratio <= be_cap)

        out.append({
            "town": row["town"],
            "median_price": price,
            "sales_count": int(row.get("sales_count", 0) or 0),
            "pmt_pi": pmt_pi,
            "taxes_monthly": taxes_mo,
            "insurance_monthly": ins_mo,
            "hoa_monthly": hoa_mo,
            "total_monthly": total_mo,
            "cash_to_close": cash_to_close,
            "front_end_ratio": fe_ratio,
            "back_end_ratio": be_ratio,
            "passes_dti": pass_dti
        })

    return pd.DataFrame(out).sort_values(
        ["passes_dti","total_monthly","median_price"], ascending=[False, True, True]
    )
