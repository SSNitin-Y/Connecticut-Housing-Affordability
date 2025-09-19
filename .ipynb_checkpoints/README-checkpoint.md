# Buyer Affordability Analysis (Python-only)

Goal: Help first-time buyers decide where to buy and what it will cost, by town.

What’s inside
- config/inputs.yaml — editable buyer assumptions and filters
- data/raw/ — original CSVs (read-only)
- data/clean/ — cleaned tables after parsing/typing
- data/analytics/ — monthly metrics + deltas for charts
- notebooks/ — thin EDA and report assembly (optional entry point)
- src/ — load/clean, metrics, affordability, visuals
- reports/ — interactive Plotly HTML charts and a short summary

Workflow
1) Intake & profiling → parse dates, coerce currency/percent, QA
2) Price layer → monthly median price by town (and by property type)
3) Affordability engine → P&I, taxes, insurance, HOA; DTI guardrails
4) Ranking & sensitivity → top towns under your inputs; sliders for rate/down payment
5) Packaging → CSVs + HTML charts + summary
