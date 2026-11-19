from ts_lab.data import load_transactions

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
