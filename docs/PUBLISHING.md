# Publish Interactive Live Graphs with GitHub Pages

## 1) Copy charts to /docs
```
bash


mkdir -p docs
cp reports/*.html docs/
git add docs
git commit -m "Publish interactive charts to GitHub Pages"
git push
```

---

## 2) Enable Pages

GitHub → Repo → **Settings** → **Pages**

Source: **Deploy from a branch**

Branch: ```main```

Folder: ```/docs```

Save, then wait 1–3 minutes.

---

## 3) URLs

Site root: ```https://<username>.github.io/<repo>/```

Individual charts:
  ```/trend_top_towns.html```
  ```/top_towns_lowest_total_monthly.html```
  ```/yoy_heatmap.html```

---

## 4) Common issues
- 404: Pages needs a minute; refresh. Check filename case.
- Private repo: Pages requires public repo (or paid plan).
- Charts show as code on portfolio sites: never paste HTML; link or embed via ```<iframe>```.


---

### `TROUBLESHOOTING.md`
```md
# Troubleshooting

## Push rejected: file >100MB
Use Git LFS and migrate existing big files.
```bash
git lfs install
git lfs track "*.csv" "data/raw/**" "data/clean/**"
git add .gitattributes
git lfs migrate import --include="*.csv,data/raw/**,data/clean/**"
git push --force-with-lease
```

---

### No reports generated
- Ensure ```data/raw/Housing_data.csv exists```.
- Dates must parse. If your date header is unusual, adjust detection in ```src/load_clean.py```.
- Re-run: ```python run.py```.

---

### Pages not showing charts
- Copy HTMLs to ```/docs``` and enable Pages.
- Wait a couple of minutes; check exact filenames.
- If embedding elsewhere, use an iframe; don’t paste HTML directly.

---

## macOS .DS_Store in repo
```
bash


echo .DS_Store >> .gitignore
git rm --cached .DS_Store
git add .gitignore
git commit -m "Ignore .DS_Store"
git push
```

---

### `docs/index.md`
```md
# Connecticut Housing Affordability — Interactive

Open the charts:

- [Trend: Top Towns](trend_top_towns.html)
- [Top Towns by Total Monthly](top_towns_lowest_total_monthly.html)
- [YoY Heatmap](yoy_heatmap.html)

> Data and methodology: see the main [README](../README.md).
