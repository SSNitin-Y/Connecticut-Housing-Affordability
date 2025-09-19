# src/viz_plotly.py
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def _placeholder(out_html: str, title: str):
    go.Figure().update_layout(title=title).write_html(out_html, include_plotlyjs="cdn")
    return out_html

def line_median_price_plotly(metrics: pd.DataFrame, towns, out_html: str):
    if not isinstance(towns,(list,tuple,set)):
        towns = [towns]
    d = metrics[metrics["town"].isin(towns)].sort_values(["town","month_key"])
    if d.empty:
        return _placeholder(out_html, "No data for selected towns")
    fig = px.line(d, x="month_key", y="median_sale_amount", color="town",
                  title="Median sale amount by town")
    fig.update_layout(hovermode="x unified", yaxis_tickprefix="$")
    fig.write_html(out_html, include_plotlyjs="cdn")
    return out_html

def bar_top_towns_plotly(aff: pd.DataFrame, k: int, out_html: str, strict_dti: bool=True):
    d = aff[aff["passes_dti"]] if strict_dti else aff
    d = d.sort_values("total_monthly").head(k)
    if d.empty:
        return _placeholder(out_html, "No towns to display")
    title = f"Top {k} towns by lowest total monthly" + (" (DTI-compliant)" if strict_dti else " (no DTI filter)")
    fig = px.bar(d, x="total_monthly", y="town", orientation="h", title=title)
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_tickprefix="$")
    fig.write_html(out_html, include_plotlyjs="cdn")
    return out_html

def heatmap_yoy_plotly(metrics: pd.DataFrame, out_html: str):
    p = metrics.pivot_table(index="town", columns="month_key", values="yoy").dropna(how="all")
    if p.empty:
        return _placeholder(out_html, "No YoY data to show")
    z = p.values.astype(float)
    x = [str(c) for c in p.columns]
    y = [str(i) for i in p.index]
    fig = go.Figure(data=go.Heatmap(z=z, x=x, y=y, colorbar=dict(title="YoY")))
    fig.update_layout(title="YoY change heatmap (town × month)")
    fig.write_html(out_html, include_plotlyjs="cdn")
    return out_html
