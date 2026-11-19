"""Data loaders. Pure functions returning pandas objects, so notebooks and the future bot can share them."""
import json
from pathlib import Path

import pandas as pd

from ts_lab import DATA_DIR

# Money-Tracker CSV header (Vietnamese) -> short English names.
COLUMNS = {
    "Thời gian": "time",
    "Nội dung": "description",
    "Danh mục": "category",
    "Tài khoản": "account",
    "Số dư sau giao dịch": "balance_after",
    "Số tiền": "amount",
    "Mã tham chiếu": "reference",
}


def load_transactions(path: Path = DATA_DIR / "transactions.csv") -> pd.DataFrame:
    """Load the Money-Tracker export as a clean, time-indexed DataFrame.

    Expected result:
      - index: DatetimeIndex named "time", sorted oldest -> newest
      - columns: description, category, account, balance_after, amount, reference
      - amount / balance_after: integer VND (negative amount = money out)
      - voided rows ("[Đã hủy] ..." in description) removed
    """
    # TODO 1: read the CSV. Hint: the file starts with a BOM -> which encoding?
    df = pd.read_csv(path,encoding="utf-8-sig")  
  # TODO 2: rename columns with COLUMNS.
    df = df.rename(columns=COLUMNS)
  # TODO 3: parse "time". Raw looks like "07:47:35 19/11/26" (day not zero-padded: "5/11/26").
  # Hint: pd.to_datetime(..., format=...). Why is passing `format` safer than letting pandas guess?
    df["time"].head()
    df["time"] = pd.to_datetime(df["time"],format="%H:%M:%S %d/%m/%y")
  # TODO 4: turn "-19.000 đ" into -19000 for amount and balance_after.
  #         Hint: .str.replace(...) then .astype("int64"). Careful: "." is a thousands separator here.
    for col  in ["amount","balance_after"]:
      df[col] = (
        df[col]
        .str.replace(".", "")   # remove the thousands separator
        .str.replace(" đ", "")   # remove the currency suffix (mind the space)
        .astype("Int64")
    )
  # TODO 5: drop voided rows.
    voided = df["description"].str.startswith("[Đã hủy]")
    df = df[~voided]
  # TODO 6: set "time" as index and sort it.
  # raise NotImplementedError
    df = df.set_index("time").sort_index()
    return df

def daily_spending(df: pd.DataFrame, freq: str = "D") -> pd.Series:
    """Total spending per period (positive VND), using our spending definition."""
    # Spending = money out in consumption categories. "Chuyển khoản" included:
    # non-QR payments and transfers to partner for shared spending.
    is_spend_category = df["category"].isin(["Khác", "Ăn uống", "Hóa đơn", "Chuyển khoản"])
    is_money_out = df["amount"] < 0
    spend = df[is_spend_category & is_money_out]

    daily = -spend["amount"].resample(freq).sum()
    # daily.plot(kind="bar")
    return daily


def load_prices(path: Path) -> pd.DataFrame:
    """Load daily OHLCV saved by `vnstock-oapi ohlc tcbs ... -o file.jsonl`.

    One JSON envelope per line; candles live in body["data"]. Prices are in VND.
    Returns a DataFrame indexed by trading date (sorted, unique): open, high, low, close, volume.
    """
    with open(path, encoding="utf-8") as f:
        rows = [row for line in f for row in json.loads(line)["body"]["data"]]
    df = pd.DataFrame(rows)
    # tradingDate is midnight UTC of the trading day -> keep the calendar date, drop the timezone.
    df["date"] = pd.to_datetime(df["tradingDate"]).dt.tz_localize(None)
    # Pages overlap at their edges, so the same day can appear twice.
    df = df.drop_duplicates("date").set_index("date").sort_index()
    return df[["open", "high", "low", "close", "volume"]]
