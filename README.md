# Connecticut Housing Affordability — Town-by-Town Monthly Cost & DTI

[![Pages](https://img.shields.io/badge/GitHub%20Pages-Live-2ea44f)](https://ssnitin-y.github.io/Connecticut-Housing-Affordability/)
[![Python](https://img.shields.io/badge/Python-3.13.5%2B-blue.svg)](https://www.python.org/downloads/release/python-3135/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458)](https://pandas.pydata.org/docs/getting_started/index.html#getting-started)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3f4f75)]([https://plotly.com/](https://plotly.com/python/getting-started/))
[![Git LFS](https://img.shields.io/badge/Git%20LFS-Data%20Tracked-ff6f61)](https://git-lfs.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)

**Live charts**
- Trend — Top Towns: https://ssnitin-y.github.io/Connecticut-Housing-Affordability/trend_top_towns.html  
- Top Towns by Total Monthly: https://ssnitin-y.github.io/Connecticut-Housing-Affordability/top_towns_lowest_total_monthly.html  
- YoY Heatmap: https://ssnitin-y.github.io/Connecticut-Housing-Affordability/yoy_heatmap.html

> This project turns raw home sales into decisions for first-time buyers. It cleans transactions, builds monthly median prices by town, converts those into **all-in monthly cost** and **cash-to-close** using buyer inputs, and flags **DTI** pass/fail. Results are ranked and visualized with interactive Plotly charts.

---

## Why this exists
Listing prices don’t answer “can I actually afford this?”  
Here you get:
- All-in **monthly payment** (P&I + taxes + insurance + HOA)
- **Cash to close** (down payment + closing costs)
- **DTI** check against your income
- Clear **ranked towns** and interactive **trends/momentum**

All assumptions live in one config file so you can tune them and re-run.

---

## Project structure
```buyer_affordability_project/```
  - ```|config/```
    - ```inputs.yaml``` # your assumptions (rate, taxes, HOA, income, etc.)
  - ```|data/```
  - ```|raw/``` # put Housing_data.csv here
  - ```|clean/``` # cleaned rows (generated)
  - ```|analytics/``` # monthly metrics, deltas, affordability (generated)
  - ```|reports/``` # interactive HTML + PNG charts (generated)
  - ```|src/```
    - ```load_clean.py``` # parse money/dates, detect month_key
    - ```metrics.py``` # monthly medians + MoM/YoY
    - ```affordability.py``` # P&I, taxes, insurance, HOA, DTI
    - ```viz.py``` # quick PNG sanity charts
    - ```viz_plotly.py``` # interactive Plotly charts
  - ```|run.py``` # orchestrates the pipeline
  - ```|requirements.txt```
  - ```|README.md```

---

## Quickstart
```
bash


# clone with large files
brew install git-lfs   # macOS; Windows: winget/choco
git lfs install
git clone https://github.com/SSNitin-Y/Connecticut-Housing-Affordability.git
cd Connecticut-Housing-Affordability
git lfs pull

# python env + deps
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt  # or: pandas numpy matplotlib plotly pyyaml

# data
# put your CSV at:
# data/raw/Housing_data.csv

# run
python run.py
open reports/top_towns_lowest_total_monthly.html
```

## Configure buyer assumptions
**Edit config/inputs.yaml and re-run.**
```
yaml


defaults:
  down_payment_pct: 0.15
  interest_rate_apy: 0.0675
  term_years: 30
  closing_cost_pct: 0.03
  property_tax_rate: 0.012
  insurance_annual_usd: 1500
  hoa_monthly_usd_sfh: 0
  hoa_monthly_usd_condo: 250
  gross_monthly_income: 7500
  dti_frontend_max: 0.28
  dti_backend_max: 0.36
```
---

## Outputs:

- ```data/```
  - ```clean/```
    - ```clean_housing.csv```
  - ```analytics/```
    - ```monthly_by_town.csv```
    - ```monthly_by_town_with_deltas.csv```
    - ```affordability_latest.csv```
- ```reports/```
  - ```trend_top_towns.html```
  - ```top_towns_lowest_total_monthly.html```
  - ```yoy_heatmap.html```
  - ```trend_top_town.png```

**Open the HTML files in your browser.**

_**Note:** Place your source files in ```Data/Raw``` (e.g., ```Data/Raw/Housing_data.csv```). The pipeline reads only from this folder. Outputs in ```data/clean```, ```data/analytics```, and reports are generated after a valid raw file exists in ```Data/Raw```._

---

### What the pipeline does:
**Clean & standardize**
  1. Detect the date column
  2. build month_key
  3. parse money/percent text into numbers.

**Town-level metrics**
  1. Monthly median sale amount
  2. sales_count
  3. MoM/YoY deltas.

**Affordability math**
  1. Loan = price − down payment
  2. P&I via amortization
  3. add taxes/insurance/HOA → total monthly
  4. compute cash-to-close
  5. mark DTI pass at your income.

**Interactive visuals**
  1. Ranked towns by total monthly (DTI-passing first)
  2. trend lines for active towns
  3. YoY heatmap for market momentum.

---

### Publishing Interactive Visuals to GitHub Pages (optional)

```
bash


mkdir -p docs
cp reports/*.html docs/
git add docs
git commit -m "Publish interactive charts to GitHub Pages"
git push
```

**Then enable Pages: Repo → Settings → Pages → Source: Deploy from a branch** 
Branch: ```main```, Folder: ```/docs```.

Your site: https://**USERNAME**.github.io/Connecticut-Housing-Affordability/

---

### Troubleshooting:

**Push rejected (>100MB)**: large files must use LFS.
```
bash


git lfs track "*.csv" "data/raw/**" "data/clean/**"
git add .gitattributes
git lfs migrate import --include="*.csv,data/raw/**,data/clean/**"
git push --force-with-lease
```

**No reports generated**: ensure ```data/raw/Housing_data.csv``` exists and dates parse; ```tweak src/load_clean.py``` if your header is unusual.

**Pages 404**: wait 1–3 minutes after enabling Pages; check filename case.

**macOS junk in git**:

```
bash


echo .DS_Store >> .gitignore
git rm --cached .DS_Store
git add .gitignore
git commit -m "Ignore .DS_Store"
git push
```

---

### Roadmap
1. PMI when down payment < 20%
2. Per-town tax/insurance/HOA tables
3. Property-type split (SFH vs condo)
4. Sensitivity grid (rate × down payment)

### License
MIT — see ```LICENSE```.

### Credits

Author: **SS Nitin**

Repo: https://github.com/SSNitin-Y/Connecticut-Housing-Affordability

Live charts: https://ssnitin-y.github.io/Connecticut-Housing-Affordability/


---

### `LICENSE.md`
```md
MIT License

Copyright (c) 2025 SS Nitin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in  
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN  
THE SOFTWARE.
```
