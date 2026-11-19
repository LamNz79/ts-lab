# ts-lab

Học time series qua thực hành, theo sách [Forecasting: Principles and Practice](https://otexts.com/fpp3/) (Hyndman).

Dữ liệu: chi tiêu cá nhân (Money-Tracker) và giá/khối lượng cổ phiếu Việt Nam (`vnstock`).

## Cấu trúc
- `notebooks/` — mỗi chặng một notebook (`01_...ipynb`, `02_...ipynb`, ...)
- `src/ts_lab/` — code tái sử dụng (load dữ liệu, metrics, mô hình)
- `data/` — dữ liệu thô/đã xử lý, không commit

## Chạy
```bash
uv sync
uv run jupyter lab
```

Lộ trình và tiến độ: xem `CLAUDE.md`.
"# ts-lab" 
