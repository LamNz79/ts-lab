"""Data loaders. Pure functions returning pandas objects, so notebooks and the future bot can share them."""
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
