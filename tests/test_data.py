import json

from ts_lab.data import daily_spending, load_prices, load_transactions

# Fake export with the quirks we must handle: BOM, non-padded day, cash row without balance, voided row.
CSV = (
    "﻿\"Thời gian\",\"Nội dung\",\"Danh mục\",\"Tài khoản\",\"Số dư sau giao dịch\",\"Số tiền\",\"Mã tham chiếu\"\r\n"
    "\"07:47:35 19/11/26\",\"coffee\",\"Ăn uống\",\"TPBank ····0000\",\"5.496.356 đ\",\"-19.000 đ\",\"R1\"\r\n"
    "\"09:22:40 5/11/26\",\"cash lunch\",\"Ăn uống\",\"Ví ····0000\",\"\",\"-50.000 đ\",\"\"\r\n"
    "\"10:00:00 6/11/26\",\"[Đã hủy] typo\",\"\",\"Ví ····0000\",\"\",\"-1.000.000 đ\",\"\"\r\n"
)


def test_load_transactions(tmp_path):
    path = tmp_path / "t.csv"
    path.write_text(CSV, encoding="utf-8")
    df = load_transactions(path)

    assert list(df.index.astype(str)) == ["2026-11-05 09:22:40", "2026-11-19 07:47:35"]  # day/month order, sorted, voided dropped
    assert df["amount"].tolist() == [-50000, -19000]
    assert df["balance_after"].isna().tolist() == [True, False]  # cash has no bank balance


def test_daily_spending(tmp_path):
    path = tmp_path / "t.csv"
    path.write_text(CSV, encoding="utf-8")
    daily = daily_spending(load_transactions(path))

    assert len(daily) == 15  # 5/11..19/11, empty days included
    assert daily.loc["2026-11-05"] == 50000 and daily.loc["2026-11-19"] == 19000  # positive spending
    assert daily.loc["2026-11-10"] == 0  # no spending that day -> 0, not NaN


def test_load_prices(tmp_path):
    def page(*dates):
        candles = [{"open": 1.0, "high": 2.0, "low": 0.5, "close": 1.5, "volume": 10, "tradingDate": f"{d}T00:00:00.000Z"} for d in dates]
        return json.dumps({"body": {"ticker": "X", "data": candles, "dataT1": None}})

    path = tmp_path / "x.jsonl"
    # Newer page first, and the two pages overlap on 2026-01-05.
    path.write_text(page("2026-01-05", "2026-01-06") + "\n" + page("2026-01-02", "2026-01-05") + "\n", encoding="utf-8")
    df = load_prices(path)

    assert list(df.index.astype(str)) == ["2026-01-02", "2026-01-05", "2026-01-06"]  # sorted, deduped, no timezone
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
